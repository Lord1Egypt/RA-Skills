# Item linking errors

## 何时读取

当用户的问题涉及 n8n 文档 `data/data-mapping/data-item-linking/item-linking-errors.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- In n8n you can reference data from any previous node. This doesn't have to be the node just before: it can be any previous node in the chain. When referencing nodes further back, you use the expression syntax `$(node_name).item`. !A diagram showing the threads linking multiple items back through a workflow Diagram of threads for different items. Due to the item linking, you can get the actor for each movie using `$('Get famous movie actors').item`.

## 快速定位

- Fix for 'Info for expressions missing from previous node'
- Fix for 'Multiple matching items for expression'

