# Skill 上报协议规范（Value Report Spec）

**版本**：v1.0  
**状态**：正式发布  
**适用范围**：所有接入 multi-role-governance 的 Skill  
**维护方**：CTO 角色 / 大管家  

---

## 一、目标

每个 Skill 任务完成后，向**共享指标文件**追加一条结构化记录。

multi-role-governance 的聚合层（大管家）在任务结束时读取这些记录，过滤并渲染摘要。

**核心原则**：
- 各 Skill 只需**追加写入**，无需了解聚合逻辑
- multi-role-governance 只需**读取过滤**，无需感知各 Skill 实现细节
- 新 Skill 接入**零改造**：不修改 SKILL.md，不修改大管家代码

---

## 二、共享指标文件

### 路径

```
{项目根目录}/sessions/.skill-metrics.jsonl
```

> **说明**：`{项目根目录}` 即 multi-role-governance Skill 所在目录，默认为：
> `/Users/{user}/Documents/Skill/multi-role-governance/`

### 格式

JSONL（JSON Lines）格式：**每行一条独立的 JSON 记录**，行尾无逗号，文件整体不加 `[` `]` 包裹。

```jsonl
{"skill":"coding-agent","task_id":"2026-03-19T11:50:00Z","token_saved":800,...}
{"skill":"feishu-doc","task_id":"2026-03-19T12:10:00Z","token_saved":200,...}
```

### 文件管理

- 文件不存在时，Skill **自动创建**，无需手动初始化
- 文件只追加，**不覆盖、不清空**（历史记录永久保留）
- 大文件时聚合层只读取当前 task_id 对应的记录，不全量加载

---

## 三、上报字段规范

### 完整字段定义

```json
{
  "skill": "skill名称",
  "task_id": "任务ID或时间戳",
  "token_saved": 800,
  "token_baseline": 1200,
  "token_actual": 400,
  "reason": "一句话说明节省原因",
  "timestamp": "ISO8601时间戳",
  "should_display": true
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill` | string | ✅ | Skill 的唯一标识名称（建议与目录名一致） |
| `task_id` | string | ✅ | 任务唯一标识，推荐使用 ISO8601 时间戳，同一任务的多条记录须使用相同 task_id |
| `token_saved` | number | ✅ | 本次任务节省的 Token 数（估算值，可为负数） |
| `token_baseline` | number | ✅ | 基准值：不使用多角色架构完成同等任务的预估 Token 消耗 |
| `token_actual` | number | ✅ | 实际值：本次任务实际消耗的 Token 数（从上下文推算） |
| `reason` | string | ✅ | 一句话说明节省原因，供摘要渲染使用 |
| `timestamp` | string | ✅ | 记录写入时间，ISO8601 格式（含时区），例：`2026-03-19T11:50:00+08:00` |
| `should_display` | boolean | ✅ | `true`=聚合层渲染此条记录；`false`=聚合层跳过此条记录 |

### `should_display` 判断规则

由各 Skill **自行判断**，参考以下标准：

| 情形 | 推荐值 |
|------|--------|
| 任务复杂，节省显著（`token_saved > 0`） | `true` |
| 任务简单，节省为负或接近零 | `false` |
| 单轮问答，未触发任何协作增益 | `false` |
| 多角色协作，有明确节省 | `true` |

---

## 四、聚合层行为（multi-role-governance 负责）

大管家在任务结束时执行以下聚合逻辑：

```
1. 读取 sessions/.skill-metrics.jsonl
2. 筛选出当前 task_id 对应的所有记录
3. 过滤掉 should_display == false 的记录
4. 若过滤后无任何记录 → 跳过摘要输出（不渲染）
5. 若过滤后有记录 → 按以下格式渲染输出摘要
```

### 渲染格式参考

```
✅ 任务完成
📊 本次执行摘要：
  • 调度角色：[角色A → 做了什么；角色B → 做了什么]
  • 本次任务节省预估：
    - [skill名] 节省约 800 Token（原因：跳过冗余上下文加载）
    - [skill名] 节省约 200 Token（原因：语义路由避免全量扫描）
  • 合计节省：~1000 Token（基准 1500 Token → 实际 500 Token）
  • 本月累计节省：~X Token
```

---

## 五、新 Skill 接入规则

### 接入步骤

1. 在 Skill 的任务完成逻辑末尾，追加写入一条 JSON 到指标文件
2. 无需修改 `SKILL.md`（multi-role-governance）
3. 无需修改大管家代码
4. 向大管家汇报接入完成，大管家验收

### 写入示例（伪代码）

```python
import json, os
from datetime import datetime, timezone

metrics_path = "/Users/.../multi-role-governance/sessions/.skill-metrics.jsonl"
os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

record = {
    "skill": "my-new-skill",
    "task_id": "2026-03-19T11:50:00+08:00",
    "token_saved": 600,
    "token_baseline": 1000,
    "token_actual": 400,
    "reason": "专项角色加载避免了全量系统提示词注入",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "should_display": True
}

with open(metrics_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
```

### Shell 写入示例

```bash
METRICS_FILE="/Users/.../multi-role-governance/sessions/.skill-metrics.jsonl"
mkdir -p "$(dirname "$METRICS_FILE")"
echo '{"skill":"my-skill","task_id":"2026-03-19T11:50:00Z","token_saved":600,"token_baseline":1000,"token_actual":400,"reason":"角色专项加载减少冗余","timestamp":"2026-03-19T11:50:00Z","should_display":true}' >> "$METRICS_FILE"
```

---

## 六、版本与兼容性

| 版本 | 变更说明 |
|------|---------|
| v1.0 | 初始版本，定义基础字段与聚合逻辑 |

### 兼容原则

- 规范版本 **v1.0**，未来字段变更**向后兼容**
- 聚合层**忽略未知字段**，新字段不影响旧版本 Skill 的正常上报
- 废弃字段在规范中标注 `deprecated`，保留至少两个版本后移除
- `task_id` + `skill` 联合唯一，不做强制去重（允许重复追加，聚合层取最后一条）

---

## 七、设计决策说明

### 为什么用 JSONL 而非 JSON？

追加写入更高效，无需加锁读取整个文件再序列化。JSONL 每行独立，局部损坏不影响其他记录。

### 为什么 `should_display` 由各 Skill 自判断？

各 Skill 最了解自身任务的复杂度。聚合层不应猜测，责任明确在写入方。

### 为什么不直接修改大管家的摘要模板？

解耦。新 Skill 接入不应触碰治理引擎核心文件，降低出错风险，也符合「只追加」的最小侵入原则。

---

*本规范由 CTO 角色起草，大管家负责最终验收与发布。*
