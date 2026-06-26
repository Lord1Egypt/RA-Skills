# 防套娃三保险 — 详解

## 问题

Cron session 产生的记忆整理行为，本身不应该再被当作"用户对话"来处理。否则：

```
cron 扫描 session → 产生整理记录 → 整理记录进入下次扫描 → 无限循环
```

这叫"套娃污染"，会让 A′ 区充满 cron 自己的处理日志。

## 三保险详解

### 第一保险：Prompt 前缀（检测级）

**规则：** 所有 cron prompt 第一行必须是 `[cron:memory-xxx]` 格式。

```
[cron:memory-daily] 请扫描今天 23:30 以来的 session JSONL，提炼...
[cron:memory-weekly] 请执行本周分类治理，提炼...
```

**作用：** 让 LLM 在生成回复时就知道这是 cron 请求，天然不会把结果写成用户意图。

### 第二保险：扫描器忽略规则（过滤级）

**规则：** 扫描 session JSONL 时，忽略以下内容：

| 忽略条件 | 示例 |
|---------|------|
| session 首条 user 消息以 `[cron:` 开头 | `[cron:memory-daily] 请扫描...` |
| 消息内容含 `memory-daily ok` | `memory-daily ok` |
| 消息内容含 `memory-weekly ok` | `memory-weekly ok` |
| 消息内容含 `NO_REPLY` | `NO_REPLY` |
| role 为 `tool` | `{"role":"tool"...}` |
| role 为 `system` | `{"role":"system"...}` |

**实现伪代码：**

```python
def should_ignore_message(msg):
    content = msg.get("content", "")
    role = msg.get("role", "")

    # 角色过滤
    if role in ("tool", "system"):
        return True

    # 通知文本过滤
    if content in ("memory-daily ok", "memory-weekly ok", "NO_REPLY"):
        return True

    # cron session 过滤（session 级别，在此处提前退出）
    if is_cron_session(session) and role == "user":
        return True

    return False

def is_cron_session(session):
    first_msg = get_first_message(session)
    return first_msg.get("content", "").startswith("[cron:")
```

### 第三保险：收敛验证（验证级）

**规则：** 重复执行 L1 hourly，最终应收敛到 `events: 0`。

```bash
# 连续执行两次 L1，检查是否有新条目产生
$ openclaw memory-fusion-lite hourly --force
events: 5   ← 第一次，有内容
$ openclaw memory-fusion-lite hourly --force
events: 0   ← 第二次，0 说明无新内容，防套娃生效
```

如果第二次仍 >0，说明有漏网的 cron 内容在自我循环。

## 快速验证

```bash
# 验证防套娃是否生效
openclaw memory-fusion-lite verify
```

预期输出：`PASS - no recursion detected`

## 与 Dreaming 的关系

Dreaming 有自己的防套娃机制（`memory/dreaming/` 目录不参与扫描）。

memory-fusion-lite 的防套娃针对的是：
- cron session 的 prompt/response
- `memory-daily ok` / `memory-weekly ok` 通知文本
- 增量扫描时的字节偏移记录

两者互补，Dreaming 的 `memory/dreaming/` 目录本身已被 Dreaming 系统排除。
