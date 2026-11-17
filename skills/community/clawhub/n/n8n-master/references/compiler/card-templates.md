# Compiler Card Templates

## Node Card

```markdown
---
title: Node name
type: node-card
status: draft
updated: YYYY-MM-DD
source: official-doc
tags: [n8n, node]
---

# Node name

## 何时读取

...

## 核心要点

- ...

## 关键参数 / 操作

- ...

## n8n 使用建议

- ...

## 常见坑

- ...

## 来源

- Local: `references/source/...`
```

## API Card

````markdown
---
title: Platform API name
type: api-card
status: draft
updated: YYYY-MM-DD
source: source-doc
tags: [api, platform, n8n]
---

# Platform API name

## Endpoint

- Method:
- URL:

## Auth / Headers

- ...

## Params

- Path:
- Query:

## Body

```json
{}
```

## n8n HTTP Request

- Method:
- URL expression:
- Headers:
- Body Content Type:
- Body:

## Read Response

- ...

## Permissions / Pitfalls

- ...

## Source

- Local: `references/source/...`
````

## Concept Card

```markdown
---
title: Concept
type: concept-card
status: draft
updated: YYYY-MM-DD
source: official-doc
tags: [n8n, concept]
---

# Concept

## 何时读取

...

## 定义

...

## 决策规则

- ...

## 示例

...

## 常见坑

- ...

## 来源

- Local: `references/source/...`
```

## Recipe

````markdown
---
title: Recipe
type: recipe
status: draft
updated: YYYY-MM-DD
source: compiled
tags: [n8n, workflow]
---

# Recipe

## 何时读取

...

## 节点链路

```text
Trigger -> ...
```

## 数据契约

- Input:
- Output:

## 关键配置

- ...

## 错误处理

- ...

## 来源

- Local: `references/wiki/...`
- Local: `references/source/...`
````
