---
name: "dry"
description: "DRY (Don't Repeat Yourself) 不要重复自己 -- 软件设计原则。Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."
url: "https://java-design-patterns.com/principles/#dry"
category: "principles"
tags: [design-principle]
---

# DRY (Don't Repeat Yourself) 不要重复自己原则

> 官方文档: https://java-design-patterns.com/principles/
> 分类: 设计原则 (Principles)

## [Keep things DRY](https://java-design-patterns.com/principles/#keep-things-dry)

Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

Why

- Duplication can lead to maintenance nightmares, poor factoring, and logical contradictions.

How

- Put business rules, long expressions, if statements, math formulas, metadata, etc. in only one place.
- Apply the Rule of three.
