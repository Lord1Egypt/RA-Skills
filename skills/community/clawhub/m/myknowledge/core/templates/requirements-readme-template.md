# 需求列表

> 本文档是需求索引页，列出所有活跃需求的状态和最后更新时间。
> **注意**：本文档仅做索引，不包含需求详情。详情请进入各需求的 README.md。

## 活跃需求

| 需求ID | 标题 | 状态 | 最后更新 | 负责人 |
|--------|------|------|----------|--------|
{{#active_requirements}}
| [{{id}}](./{{id}}/README.md) | {{title}} | {{status}} | {{updated_at}} | {{owner}} |
{{/active_requirements}}

{{^active_requirements}}
*暂无活跃需求*
{{/active_requirements}}

## 已完成需求

| 需求ID | 标题 | 完成时间 |
|--------|------|----------|
{{#completed_requirements}}
| [{{id}}](../archive/{{id}}/README.md) | {{title}} | {{completed_at}} |
{{/completed_requirements}}

{{^completed_requirements}}
*暂无已完成需求*
{{/completed_requirements}}

---

> **职责说明**：本文档是需求目录的索引，列出所有需求的概要信息（ID、标题、状态、时间）。
> **不负责**：需求详情、项目整体状态、数据资产索引 —— 这些分别在需求 README.md 和 PROJECT-STATUS.md 中。
