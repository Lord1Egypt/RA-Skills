---
name: Mi-MemoryStack
description: 个性化记忆框架，提供用户记忆的自动存储和检索。CRITICAL:每轮对话必须执行检索和保存，不可跳过。Use when:(1) 用户对话需要历史上下文, (2) 需要记住用户偏好/身份, (3) 多轮对话需要连续性。
allowed-tools: Bash(python3:*)
---

# 🧠 Memory MI

⚠️ **CRITICAL - 必须执行的流程**

每轮对话必须按以下顺序执行，**不可跳过任何步骤**：

```
[用户输入]
    ↓
Step 1: [MUST] 执行 memory_search.py 检索记忆
    ↓
Step 2: 生成回复（融入记忆）
    ↓
Step 3: [MUST] 执行 memory_daemon.py queue 保存记忆（后台）
    ↓
Step 4: 显示回复给用户
```

**自检清单**（每轮对话后确认）：
- [ ] 是否执行了 `memory_search.py`？
- [ ] 是否执行了 `memory_daemon.py queue`？
- [ ] 是否看到 "已加入保存队列"？

---

## 🚀 快速使用

### 1. 确保守护进程已启动

```bash
# 检查状态
python3 scripts/memory_daemon.py status

# 如未启动，执行
python3 scripts/memory_daemon.py start
```

### 2. 检索记忆（同步，必须等待）

```bash
python3 scripts/memory_search.py --user-id "<USER_ID>" --query "<用户输入>"
```

**示例**:
```bash
python3 scripts/memory_search.py \
  --user-id "ou_c4f3245c6fca9" \
  --query "我想喝奶茶"
```

**输出**:
```json
{
  "success": true,
  "memories": {
    "l0": "用户喜欢少糖奶茶",
    "l1": "用户是比亚迪车主"
  }
}
```

### 3. 保存记忆（后台异步，立即返回）

```bash
python3 scripts/memory_daemon.py queue \
  --user-id "<USER_ID>" \
  --query "<用户输入>" \
  --response "<AI回复>"
```

**示例**:
```bash
python3 scripts/memory_daemon.py queue \
  --user-id "ou_c4f3245c6fca9" \
  --query "我想喝少糖奶茶" \
  --response "好的主人，记得要少糖哦～"
```

**输出**:
```
[OK] 已加入保存队列
```

---

## 👤 用户ID获取

从 `inbound_meta` 中提取：

```python
user_id = inbound_meta.get("sender_id") or inbound_meta.get("user_id")
```

各平台字段：
| 平台 | 字段 | 示例 |
|------|------|------|
| Feishu | `sender_id` | `ou_c4f3245c6fca9` |
| Discord | `sender_id` | `123456789012345678` |
| Telegram | `sender_id` | `123456789` |

---

## 🔄 完整对话示例

### 场景：用户点奶茶

**用户输入**: "我刚点了杯奶茶"

**AI 内部执行**:

```bash
# Step 1: 检索记忆
USER_ID="ou_c4f3245c6fca9"
QUERY="我刚点了杯奶茶"

MEMORIES=$(python3 scripts/memory_search.py \
  --user-id "$USER_ID" \
  --query "$QUERY")
# 返回: {"memories": {"l0": "用户喜欢少糖"}}

# Step 2: 生成回复（融入记忆）
RESPONSE="哈哈，主人你这奶茶频率可以啊！记得要少糖哦～"

# Step 3: 后台保存（立即返回）
python3 scripts/memory_daemon.py queue \
  --user-id "$USER_ID" \
  --query "$QUERY" \
  --response "$RESPONSE"
# 输出: [OK] 已加入保存队列

# Step 4: 显示回复给用户
echo "$RESPONSE"
```

**用户看到**: "哈哈，主人你这奶茶频率可以啊！记得要少糖哦～" ✅

**后台处理**: 守护进程自动将记忆写入文件

---

## 📊 性能对比

| 步骤 | 方式 | 耗时 | 是否阻塞 |
|------|------|------|----------|
| 检索 | `memory_search.py` | 0.1-0.3s | ✅ 必须等待 |
| 保存 | `memory_add.py` (同步) | 0.5-2s | ❌ 不推荐 |
| 保存 | `memory_add_async.py` | 0.08s | ✅ 推荐 |
| 保存 | `memory_daemon.py queue` | **0.05s** | ✅ **最推荐** |

---

## 📋 列出已有记忆（memory_list）

用于查看用户所有的对话记忆，支持按层级统计和限制返回数量。

### 基本用法

```bash
python3 scripts/memory_list.py --user-id "<USER_ID>"
```

**示例**:
```bash
# 列出所有记忆
python3 scripts/memory_list.py \
  --user-id "ou_c4f3245c6fca9"

# 只列出 L2 长期偏好
python3 scripts/memory_list.py \
  --user-id "<USER_ID>" \
  --level l2

# 只列出最近的 5 条 L1 记忆
python3 scripts/memory_list.py \
  --user-id "<USER_ID>" \
  --level l1 \
  --limit 5
```

### 输出格式（JSON）

```json
{
  "success": true,
  "user_id": "ou_c4f3245c6fca9",
  "memories": [
    {
      "line_num": 1,
      "level": "l2",
      "query": "我喜欢喝拿铁",
      "response": "记住了，你喜欢拿铁咖啡～",
      "timestamp": "2026-03-09T10:30:00"
    }
  ],
  "count": 15,
  "by_level": {
    "l0": 5,
    "l1": 3,
    "l2": 7
  },
  "filtered_by_level": "l2",
  "returned": 10
}
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--user-id` | 用户唯一标识（必需） | - |
| `--level` | 记忆层级过滤：`l0`/`l1`/`l2` | 全部 |
| `--limit` | 限制返回的记录数 | 全部 |
| `--format` | 输出格式：`json` 或 `text` | `json` |
| `--data-path` | 记忆数据目录 | `~/.openclaw/workspace/skills/Mi-MemoryStack/data` |

### 层级说明

| 层级 | 含义 | 示例 |
|------|------|------|
| `l0` | 短期事实 | 具体事件、问答记录 |
| `l1` | 用户画像 | 身份、职业、个人信息 |
| `l2` | 长期偏好 | 喜欢/讨厌/习惯/偏好 |

### 文本格式输出

```bash
python3 scripts/memory_list.py --user-id "<USER_ID>" --format text
```

输出示例：
```
============================================================
用户记忆列表 - ou_c4f3245c6fca9
============================================================
总记录数: 15
  - L0 (短期事实): 5 条
  - L1 (用户画像): 3 条
  - L2 (长期偏好): 7 条

[1] [L2] #1
    Q: 我喜欢喝拿铁
    A: 记住了，你喜欢拿铁咖啡～
```

---

## 🔧 故障排查

### 1. 检查守护进程状态
```bash
python3 scripts/memory_daemon.py status
```

### 2. 重启守护进程
```bash
python3 scripts/memory_daemon.py stop
python3 scripts/memory_daemon.py start
```

### 3. 查看日志
```bash
cat ~/.openclaw/memory_daemon.log
```

### 4. 验证保存结果
```bash
cat data/<user_id>.jsonl
```

---

## ⚠️ 重要提醒

1. **守护进程必须先启动**，否则 `queue` 命令会失败
2. **每轮对话必须执行保存**，不可遗漏
3. **用户ID必须正确**，确保多用户隔离
4. **保存后立即返回**，不等待后台完成

---

## 📖 更多信息

- 守护进程: `scripts/memory_daemon.py`
- 搜索记忆: `scripts/memory_search.py`
- 列出记忆: `scripts/memory_list.py`
