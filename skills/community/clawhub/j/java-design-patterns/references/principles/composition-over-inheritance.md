---
name: "composition-over-inheritance"
description: "Composition Over Inheritance 组合优于继承 -- 软件设计原则。Why"
url: "https://java-design-patterns.com/principles/#compositionoverinheritance"
category: "principles"
tags: [design-principle]
---

# Composition Over Inheritance 组合优于继承原则

> 官方文档: https://java-design-patterns.com/principles/
> 分类: 设计原则 (Principles)

## [Composition Over Inheritance](https://java-design-patterns.com/principles/#composition-over-inheritance)

Why

- Less coupling between classes.
- Using inheritance, subclasses easily make assumptions, and break LSP.

How

- Compose when there is a "has a" relationship, inherit when "is a".
