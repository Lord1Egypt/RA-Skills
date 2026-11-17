# Downstream Field Mapping

本文件给出「协作状态卡片 JSON（7 模块）」到主流协作系统的字段映射，用于下游落表/同步。

**边界说明**：本 Skill 默认只读，仅产出映射后的结构化数据与本对照表；实际写入由用户在其 PM 系统或对应连接器中执行，Skill 不代为调用外部写接口。

## action_items（Owner × DDL 待办）

| 卡片字段 | 飞书多维表格 · 字段类型 | Notion Database · 属性类型 |
| --- | --- | --- |
| `task` | 任务名 · 文本 | Title |
| `owner` | 负责人 · 人员 | Person |
| `department` | 部门 · 单选 | Select |
| `ddl` | 截止日期 · 日期 | Date |
| `deliverable` | 交付物 · 文本 | Text |
| `status` | 状态 · 单选 | Status / Select |
| `evidence` | 证据 · 文本 | Text |
| `conflict`（如有） | 冲突标记 · 单选 | Select |

## risks_dependencies（风险 / 阻断 / 依赖）

| 卡片字段 | 飞书多维表格 | Notion |
| --- | --- | --- |
| `type` | 类型（风险/阻断/依赖）· 单选 | Select |
| `description` | 描述 · 文本 | Text |
| `impact` | 影响 · 文本 | Text |
| `mitigation` | 缓解措施 · 文本 | Text |
| `owner` | 负责人 · 人员 | Person |
| `evidence` | 证据 · 文本 | Text |

## confirmed_decisions（已确认决策点）

| 卡片字段 | 飞书多维表格 | Notion |
| --- | --- | --- |
| `decision` | 决策内容 · 文本 | Title |
| `result` | 结论 · 文本 | Text |
| `confirmed_by` | 确认人 · 人员 | Person |
| `evidence` | 证据 · 文本 | Text |

## needs_human_confirmation（需人工确认项）

| 卡片字段 | 飞书多维表格 | Notion |
| --- | --- | --- |
| `item` | 待确认项 · 文本 | Title |
| `reason` | 原因 · 文本 | Text |
| `suggested_confirm_with` | 建议确认对象 · 人员 | Person |
| `evidence` | 证据 · 文本 | Text |

## cross_department_relationships（跨部门协作关系）

| 卡片字段 | 飞书多维表格 | Notion |
| --- | --- | --- |
| `from` | 发起方 · 单选 | Select |
| `to` | 接收方 · 单选 | Select |
| `collaboration_item` | 协作事项 · 文本 | Text |
| `status` | 状态 · 单选 | Select |
| `evidence` | 证据 · 文本 | Text |

## 落表建议

- 一张卡片建议拆为多张表：待办表、风险表、决策表、待确认表，各表以 `evidence` 列保留证据可追溯性。
- `"未提供"` 与 `"存在冲突，需人工确认"` 为保留值，落表时可映射为对应的空态/告警态样式。
- 冲突项（`conflict` 字段非空）建议在下游用醒目颜色标注，并联动 `needs_human_confirmation`。
