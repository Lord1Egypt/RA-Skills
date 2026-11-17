# 定期日程

定期日程（recurring event）指会按规则自动重复的日程，如"每周一 9 点的周会"——创建一次，按规则自动延续。
本文档说明如何修改/删除定期日程的**某一次出现**或**整个系列**，两者的操作对象不同，务必区分。

## 核心概念：单次出现与整个系列

一个定期日程由三部分组成：

| 概念 | 是什么 | 你什么时候会看到它 |
|------|--------|--------------------|
| **主事件** | 整个系列（含规则） | `read` 时输出 🆕 系列主事件ID；`list --from` 展开单次出现；按创建日期查询时可能返回主事件 |
| **某一次**（occurrence） | 系列中的一次实例 | `list` 里每行一个，标记 🔁(系列) |
| **单独改过的那次**（例外） | 被单独修改/取消的一次 | `list` 标记 🔁(已修改) / 🔁(已取消) |

**核心规则**：对"某一次"执行的修改/删除/移动仅影响该次；修改规则、删除整个系列必须操作**主事件**（`read` 输出中的 🆕 系列主事件ID）。

## 结构化重复规则输入

模型先将用户的重复要求转换成 Microsoft Graph 的 `recurrencePattern` 对象，再通过 `--repeat` 传入 JSON。也可将 JSON 保存为 UTF-8 文件，用 `--repeat-file pattern.json` 读取，避免命令行引号转义问题。文件中只放规则对象，不要包裹 `pattern`、`range` 或 `recurrence`。后端不再接受自然语言规则字符串。

| 用户要求 | JSON 规则 |
|----------|-----------|
| 每 2 天 | `{"type":"daily","interval":2}` |
| 每周五 | `{"type":"weekly","interval":1,"daysOfWeek":["friday"],"firstDayOfWeek":"monday"}` |
| 每 2 周的周一、周三 | `{"type":"weekly","interval":2,"daysOfWeek":["monday","wednesday"],"firstDayOfWeek":"monday"}` |
| 每个工作日 | `{"type":"weekly","interval":1,"daysOfWeek":["monday","tuesday","wednesday","thursday","friday"],"firstDayOfWeek":"monday"}` |
| 每 3 个月的 15 日 | `{"type":"absoluteMonthly","interval":3,"dayOfMonth":15}` |
| 每月最后一个周五 | `{"type":"relativeMonthly","interval":1,"index":"last","daysOfWeek":["friday"]}` |
| 每年 9 月 21 日 | `{"type":"absoluteYearly","interval":1,"month":9,"dayOfMonth":21}` |
| 每年 11 月最后一个周三 | `{"type":"relativeYearly","interval":1,"month":11,"index":"last","daysOfWeek":["wednesday"]}` |

规则采用 [Microsoft Graph 的六种重复类型](https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern?view=graph-rest-1.0)。CLI 要求显式传入上表对应类型的全部字段，不会根据开始日期补全间隔、星期、一周起点或序数。

- `interval` 必须是正整数（最大 2,147,483,647）；`dayOfMonth` 范围为 1–31，`month` 范围为 1–12。布尔值、小数和数字字符串都不接受。按年重复的月日组合必须是可能存在的日期，允许 2 月 29 日。
- `daysOfWeek` 是非空且无重复的数组，只接受小写英文星期 `monday` 至 `sunday`。`firstDayOfWeek` 也从这些值中选取，是 `weekly` 的必填字段。
- 相对月度/年度规则必须提供 `index`，值为 `first`、`second`、`third`、`fourth` 或 `last`，不接受 `fifth`。
- 相对月度/年度规则若有多个星期候选，只选该月中最早满足规则的日期，并非每个星期各生成一次。模型应先明确用户意图再选用这种结构。
- 未知字段、重复 JSON 键、属于其他规则类型的字段以及缺失字段都会报错，不会静默丢弃输入。

结束条件可配合 `--repeat` 或 `--repeat-file`。都不提供表示无限重复，否则只能二选一：

- `--repeat-until 2026-12-31`：截止日期含当天，必须是精确的 `YYYY-MM-DD`，不得早于日程开始日期。
- `--repeat-times 5`：共计 5 次，必须是正整数（最大 2,147,483,647）。

更新系列也遵循这些规则：新 pattern 会重建 range。要保留原截止日期或次数，应读取后明确传入对应选项；两个选项都省略表示无截止。

后端从明确的日程开始时间构造 `range.startDate`，并把重复时区设置为日程的有效时区。含糊的重复要求由模型澄清，后端负责校验和提交明确字段。

## 常见操作

| 想做什么 | 怎么做 |
|---------|--------|
| 改某一次的时间（只改这次） | `update <那次ID> --start ... --end ...`（会创建"例外"，其余不变） |
| 删某一次（只删这次） | `delete <那次ID>`，不加 `--series` |
| 改整个系列的规则 | `read` 拿系列主事件ID → `update <主ID> --repeat-file pattern.json` |
| 解除定期（变单次） | `update <主ID> --repeat ""` |
| 删整个系列 | `delete <主ID>`（有警告）或 `delete <那次ID> --series` |
| 下次什么时候 | `next <那次ID或主ID>` |
| 把整个系列挪几天 | `move <主ID> --days N`（有警告） |

## 需要注意

- **修改整个系列的规则会重置**此前单独修改/删除过的出现（有警告，操作前先提醒用户）
- 将某一次调整至**跨越相邻出现**的时间将被拒绝（"相邻出现冲突"）——调整后的时间不得早于前一次出现、也不得晚于后一次出现
- 已删除的某一次**不可再访问**（提示"不存在"），重新执行 `list` 确认即可
- Graph 的六种规则不覆盖按小时重复或按工作日计数的间隔。遇到这些需求时说明限制，不要静默近似为另一种规则。
