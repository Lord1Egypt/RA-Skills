---
name: "law-of-demeter"
description: "Law of Demeter 迪米特法则 -- 软件设计原则。Don't talk to strangers."
url: "https://java-design-patterns.com/principles/#lawofdemeter"
category: "principles"
tags: [design-principle]
---

# Law of Demeter 迪米特法则原则

> 官方文档: https://java-design-patterns.com/principles/
> 分类: 设计原则 (Principles)

## [Law of Demeter](https://java-design-patterns.com/principles/#law-of-demeter)

Don't talk to strangers.

How

A method of an object may only call methods of:
1. The object itself.
2. An argument of the method.
3. Any object created within the method.
4. Any direct properties/fields of the object.
