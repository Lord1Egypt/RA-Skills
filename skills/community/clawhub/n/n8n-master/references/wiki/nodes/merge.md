# Merge

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Merge` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.merge`
- node group: `core-nodes`

## 核心要点

- Documentation for the Merge node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Keep Matches**: Merge items that match. This is like an inner join.
- **Keep Non-Matches**: Merge items that don't match.
- **Keep Everything**: Merge items together that do match and include items that don't match. This is like an outer join.
- **Enrich Input 1**: Keep all data from Input 1, and add matching data from Input 2. This is like a left join.
- **Enrich Input 2**: Keep all data from Input 2, and add matching data from Input 1. This is like a right join.
- **Clash Handling**: Choose how to merge when data streams clash, or when there are sub-fields. Refer to Clash handling for details.
- **Fuzzy Compare**: Whether to tolerate type differences when comparing fields (enabled), or not (disabled, default). For example, when you enable this, n8n treats `"3"` and `3` as the same.
- **Disable Dot Notation**: This prevents accessing child fields using `parent.child` in the field name.
- **Multiple Matches**: Choose how n8n handles multiple matches when comparing data streams.
- **Include All Matches**: Output multiple items if there are multiple matches, one for each match.
- **Include First Match Only**: Keep the first item per match and discard the remaining multiple matches.
- **Include Any Unpaired Items**: Choose whether to keep or discard unpaired items when merging by position. The default behavior is to leave out the items without a match.
- The **Input 1 Data**
- The **Input 2 Data**
- **A Single, Empty Item**

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

