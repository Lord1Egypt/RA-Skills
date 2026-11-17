# 引用: AI-First 架构规则（改编自 AI-Novel-Writing-Assistant）

> 来源二次审查 | 2026-07-02 | 详见 FUTURE_BACKLOG.md

## 核心原则

1. **AI判定优先** — 意图识别、任务分类、规划、路由等决策路径，必须用 AI 结构化理解作为主要实现。不用固定关键词匹配、硬编码正则路由、手动分支表。

2. **确定性代码只允许作为**:
   - 输入验证或安全守卫
   - 确定性的后处理（AI输出已被结构化之后）

3. **Quality Debt 哲学** — 单章质量问题是 local debt，不阻断全局管线：
   - local issue → 记 warn + 继续
   - recoverable failure → 修 + 继续
   - 只有 unrecoverable 失败/运行时数据完整性失败可以阻断全局

## 对 one-novel-skill 的差距

| 规则 | 当前状态 | 改造成本 |
|:-----|:---------|:---------|
| AI判定优先 | 大量正则+关键词检测 | 中 |
| Quality Debt | 一章失败阻断batch | 小 |
| 600行文件阈值 | 3个文件超标 | 中 |
| 架构wiki | 不存在 | 小 |
