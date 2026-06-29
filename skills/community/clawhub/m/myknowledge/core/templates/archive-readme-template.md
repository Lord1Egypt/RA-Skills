# 归档记录

> 此目录存放已完成或已取消的需求归档。

## 归档列表

| 需求ID | 标题 | 归档原因 | 归档日期 | 原需求链接 |
|--------|------|----------|----------|------------|
{{#archived_requirements}}
| {{id}} | {{title}} | {{archive_reason}} | {{archive_date}} | [查看原需求](../requirements/{{id}}/README.md) |
{{/archived_requirements}}

{{^archived_requirements}}
*暂无归档记录*

需求完成或取消后，会被自动归档到此处。
{{/archived_requirements}}

---

> **归档规则**：
> - 需求状态变为 `Done` 或 `Cancelled` 后，自动移入此目录
> - 归档原因包括：`已完成`、`已取消`、`已合并`、`已废弃`
> - 归档后原需求从 `requirements/` 目录移除
