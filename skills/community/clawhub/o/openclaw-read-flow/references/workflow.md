# OpenClaw Read Flow Workflow

## 核心定位

这是一个聚合型 skill，用于把整套阅读工作流作为一个技能发布，而不是把多个局部 skill 分散发布。

## 处理链

1. FreshRSS 未读抓取
2. 昨天窗口切片
3. Digest 构建
4. Daily Review 固定栏目整理
5. 人工确认后的知识沉淀

## 核心约束

- 默认处理昨天窗口
- 默认不限制原始未读数
- 默认不回写 FreshRSS 已读
- Digest 必须严格去重
- Daily Review 必须固定为 6 个栏目

## Daily Review 栏目

- 今日大事
- 变更与实践
- 安全与风险
- 开源与工具
- 洞察与数据点
- 主题深挖
