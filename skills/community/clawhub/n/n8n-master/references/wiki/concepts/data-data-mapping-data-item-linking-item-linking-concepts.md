# How items link through workflows

## 何时读取

当用户的问题涉及 n8n 文档 `data/data-mapping/data-item-linking/item-linking-concepts.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- Each output item created by a node includes metadata that links them to the input item (or items) that the node used to generate them. This creates a chain of items that you can work back along to access previous items. This can be complicated to understand, especially if the node splits or merges data. You need to understand item linking when building your own programmatic nodes, or in some scenarios using the Code node. This document provides a conceptual overview of this feature. For usage details, refer to:

## 快速定位

- n8n's automatic item linking
- Item linking example

