---
name: ingest-example-resource
description: 从 example.com 网页处理得到的示例数字资源（title + link）入库记录
metadata: {"clawdbot":{"emoji":"📦","requires":[]}}
---

# ingest-example-resource

数字资源入库记录：源自 https://example.com 的页面抽取内容。

## 资源快照

- 标题：Example Domain
- 参考链接：https://iana.org/domains/example
- 入库时间：2026-08-09 GMT+8

## 串联执行顺序（他人复现）

1. 使用 agent-browser 打开 https://example.com
2. 抓取 @e1 的文本作为标题
3. 抓取 @e2 的 href 作为外链
4. 关闭浏览器
5. 在资源中心创建本 skill 目录并撰写 SKILL.md
6. clawhub publish 将本 skill 发布到 ClawHub 资源中心
