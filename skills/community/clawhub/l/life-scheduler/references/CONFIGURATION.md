# Life Scheduler 配置说明

## 配置文件

Skill 使用两层配置：

1. **默认配置** `skills/life-scheduler/config.default.json` — Skill 自带，不要修改
2. **用户配置** `config/life-scheduler.json` — 你的自定义配置，覆盖默认值

只需要在用户配置中写你要改的字段，其余自动使用默认值。

---

## 配置项详解

### schedule（定时设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `generate_time` | string | `"07:00"` | 每日自动生成时间（24小时制） |
| `timezone` | string | `"Asia/Shanghai"` | 时区（IANA 格式） |
| `time_period_updates` | boolean | `true` | 是否启用时间段更新 |
| `update_times` | string[] | `["12:00","18:00","22:00"]` | 时间段更新的时间点 |

**示例：改为每天 8 点生成，关闭时间段更新**
```json
{
  "schedule": {
    "generate_time": "08:00",
    "time_period_updates": false
  }
}
```

### generation（生成设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `reference_history_days` | int | `3` | 生成时参考的历史日程天数（1-7） |
| `reference_recent_chats` | int | `5` | 参考的近期对话数量，0 = 不参考 |
| `respect_holidays` | boolean | `true` | 是否识别节假日 |
| `holiday_region` | string | `"CN"` | 节假日地区（CN/US/JP 等） |
| `weekday_awareness` | boolean | `true` | 是否区分工作日/周末 |

### persona（角色设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `auto_detect` | boolean | `true` | 自动从 SOUL.md / IDENTITY.md 提取人设 |
| `name` | string | `null` | 角色姓名（手动填写时覆盖自动检测） |
| `age` | int | `null` | 年龄 |
| `gender` | string | `null` | 性别 |
| `job` | string | `null` | 职业 |
| `city` | string | `null` | 所在城市 |
| `lifestyle_notes` | string | `null` | 生活方式补充说明 |

**当 `auto_detect: true` 时：**
- Skill 读取 SOUL.md 和 IDENTITY.md 自动提取信息
- 手动填写的字段会覆盖自动检测的结果
- 未检测到的字段使用通用默认值

### pools（创意池设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `source` | string | `"builtin"` | 创意池来源 |
| `auto_generate_from` | string | `"SOUL.md"` | 自动生成时读取的人设文件 |
| `custom_path` | string | `"config/life-scheduler.json"` | 自定义池的存放路径 |

**`source` 可选值：**
- `"builtin"` — 使用 Skill 内置的通用创意池
- `"auto-generate"` — 让 LLM 根据 SOUL.md 自动生成专属创意池
- `"custom"` — 使用用户手动编写的创意池

#### 自动生成创意池

设置 `source: "auto-generate"` 或直接告诉 Agent "根据我的人设生成专属创意池"。

Agent 会：
1. 读取 SOUL.md + IDENTITY.md
2. 使用 `templates/pools-generate-prompt.md` 模板
3. LLM 生成贴合角色的四个池
4. 写入 `config/life-scheduler.json` 的 `custom_pools` 字段

生成后 `source` 自动切换为 `"custom"`。

#### 自定义创意池格式

在 `config/life-scheduler.json` 中添加 `custom_pools`：

```json
{
  "pools": {
    "source": "custom"
  },
  "custom_pools": {
    "day_types": {
      "weekday": ["普通工作日", "忙碌工作日", "..."],
      "weekend": ["宅家休息", "出门逛街", "..."],
      "special": ["请假在家", "年假出游", "..."]
    },
    "moods": ["元气满满", "慵懒", "..."],
    "outfit_styles": ["干练职业装", "休闲通勤风", "..."],
    "events": ["被领导加了任务", "同事请喝奶茶", "..."]
  }
}
```

每个池建议 8-24 个选项，太少会重复，太多会分散。

### output（输出设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `file` | string | `"HEARTBEAT.md"` | 当日状态输出文件名 |
| `archive` | boolean | `true` | 是否存档历史日程 |
| `archive_path` | string | `"memory/life-history/"` | 存档目录 |
| `inject_to_context` | boolean | `true` | 是否注入 Project Context |

### advanced（高级设置）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `model_override` | string | `null` | 指定生成用的模型（null = 使用默认） |
| `max_tokens` | int | `1500` | 生成最大 token 数 |
| `temperature` | float | `0.9` | 生成温度（越高越随机） |

---

## HEARTBEAT.md 注入

`HEARTBEAT.md` 需要被加入 workspace 注入文件列表，才能在每次对话中自动带上。

方式一：在 gateway 配置中添加：
```json
{
  "agents": {
    "defaults": {
      "bootstrapFiles": ["AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md", "TOOLS.md", "MEMORY.md", "HEARTBEAT.md", "HEARTBEAT.md"]
    }
  }
}
```

方式二：告诉 Agent "把 HEARTBEAT.md 加入注入文件"，Agent 会自动处理。

---

## 时间段更新机制

启用 `time_period_updates` 后，Skill 在指定时间点更新 HEARTBEAT.md 中的"当前时间段"部分。

这是轻量操作，只修改一行文本，不调用 LLM：

| 时间 | 更新内容 |
|---|---|
| 生成时（07:00） | "早晨 — {根据日程描述}" |
| 12:00 | "下午 — {根据日程描述}" |
| 18:00 | "傍晚/下班后 — {根据日程描述}" |
| 22:00 | "深夜 — {根据日程描述}" |

时间段内容从当天日程中自动提取对应时间的活动。

---

## Cron Job 管理

Skill 自动注册的 cron job：

| Job ID | 说明 |
|---|---|
| `life-scheduler-generate` | 每日生成 |
| `life-scheduler-period-1` | 时间段更新 1 |
| `life-scheduler-period-2` | 时间段更新 2 |
| `life-scheduler-period-3` | 时间段更新 3 |

手动管理：
- 暂停：告诉 Agent "暂停日程生成"
- 恢复：告诉 Agent "恢复日程生成"
- 改时间：告诉 Agent "把生成时间改为 8 点"

---

## 历史存档

每天生成后自动存档到 `memory/life-history/YYYY-MM-DD.md`。

存档用途：
1. 下次生成时参考，避免日程重复
2. 用户可以问"昨天/前天做了什么"
3. 长期积累形成角色的"生活记忆"

建议定期清理 30 天以前的存档，或由 memory 管理机制自动归档。
