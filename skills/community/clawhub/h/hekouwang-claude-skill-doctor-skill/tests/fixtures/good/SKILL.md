---
name: example-good-skill
description: >
  生成示例日报。把一段原始数据整理成一页结构化的示例日报。
  当需要演示「合格 skill 长什么样」或要一份 demo 日报时使用；
  use when you need a demo daily report.
allowed-tools:
  - Read
  - Write
---

# Example Good Skill

一个用于演示「合格 skill」的最小夹具：frontmatter 完整、description 写清了
做什么 + 何时用、正文精简、无硬编码密钥、无绝对路径。

## 何时用

当用户要一份示例日报，或想看一个达标 skill 的结构时。

## 怎么做

1. 读取用户给的原始数据。
2. 按「概览 / 明细 / 结论」三段整理。
3. 输出一页 Markdown 日报。

> 正文只放本 skill 私有的约定；通用写法交给模型自己。
