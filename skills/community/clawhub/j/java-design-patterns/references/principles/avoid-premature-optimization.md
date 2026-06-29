---
name: "avoid-premature-optimization"
description: "Avoid Premature Optimization 避免过早优化 -- 软件设计原则。Quoting Donald Knuth: "Premature optimization is the root of all evil.""
url: "https://java-design-patterns.com/principles/#avoidprematureoptimization"
category: "principles"
tags: [design-principle]
---

# Avoid Premature Optimization 避免过早优化原则

> 官方文档: https://java-design-patterns.com/principles/
> 分类: 设计原则 (Principles)

## [Avoid Premature Optimization](https://java-design-patterns.com/principles/#avoid-premature-optimization)

Quoting Donald Knuth: "Premature optimization is the root of all evil."

Why

- It is unknown upfront where the bottlenecks will be.
- After optimization, it might be harder to read and thus maintain.

How

- Make It Work Make It Right Make It Fast
