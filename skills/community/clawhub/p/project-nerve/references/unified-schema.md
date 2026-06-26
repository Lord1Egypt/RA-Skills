# 统一任务模型

project-nerve 将来自不同平台的任务数据映射到统一的任务模型。

---

## 统一任务字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 统一 ID（格式：`{platform}-{source_id}`） |
| `source` | string | 来源平台（trello / github / linear / notion） |
| `source_id` | string | 平台原始 ID（Trello cardId、GitHub issue number、Linear identifier、Notion pageId） |
| `title` | string | 任务标题 |
| `description` | string | 任务描述（最长 500 字符） |
| `status` | string | 统一状态（待办 / 进行中 / 已完成 / 已关闭） |
| `priority` | string | 统一优先级（紧急 / 高 / 中 / 低） |
| `assignee` | string | 负责人 |
| `labels` | list[string] | 标签列表 |
| `due_date` | string | 截止日期（YYYY-MM-DD） |
| `created_at` | string | 创建时间（ISO 格式） |
| `updated_at` | string | 更新时间（ISO 格式） |
| `url` | string | 平台原始链接 |

---

## 状态映射表

| 统一状态 | Trello 列名 | GitHub State | Linear State | Notion Status |
|----------|-------------|-------------|--------------|---------------|
| 待办 | To Do / Backlog | open | Backlog / Todo / Triage | Not Started / To Do |
| 进行中 | Doing / In Progress | open (assigned) | In Progress / Started | In Progress |
| 已完成 | Done / Completed | closed (merged) | Done / Completed | Done / Completed |
| 已关闭 | Archived | closed | Cancelled / Duplicate | Archived |

### 状态标准化规则

输入字符串（不区分大小写）→ 统一状态：

- `todo`, `to do`, `backlog`, `open`, `new`, `not started`, `triage` → **待办**
- `in progress`, `in_progress`, `doing`, `started`, `active`, `in review` → **进行中**
- `done`, `completed`, `resolved`, `merged` → **已完成**
- `closed`, `cancelled`, `canceled`, `archived`, `duplicate` → **已关闭**

---

## 优先级映射表

| 统一优先级 | Trello 标签 | GitHub 标签 | Linear 数值 | Notion Select |
|-----------|-------------|-------------|-------------|---------------|
| 紧急 | urgent / 紧急 | P0 / critical / blocker | 1 (Urgent) | 紧急 / Urgent |
| 高 | high / 高 | P1 / high / important | 2 (High) | 高 / High |
| 中 | medium / 中 | P2 / medium / normal | 3 (Medium) | 中 / Medium |
| 低 | low / 低 | P3 / low / minor | 4 (Low) / 0 (None) | 低 / Low |

### 优先级标准化规则

输入字符串（不区分大小写）→ 统一优先级：

- `urgent`, `critical`, `p0`, `highest`, `blocker`, `紧急` → **紧急**
- `high`, `p1`, `important`, `高` → **高**
- `medium`, `normal`, `p2`, `default`, `中` → **中**
- `low`, `minor`, `p3`, `trivial`, `none`, `低` → **低**
- 无法识别 → 默认 **中**
