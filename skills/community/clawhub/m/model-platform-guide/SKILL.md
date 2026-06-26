---
name: model-platform-guide
description: 查询主流大模型开放平台的 API 文档入口与精简调用要点，适用于月之暗面 Kimi、阿里云百炼、硅基流动、DeepSeek、OpenRouter 等平台。用于回答鉴权方式、base URL、OpenAI 兼容调用、聊天补全、模型名、常见差异、多平台对比与文档入口。当用户提到 Kimi、Moonshot、百炼、DashScope、SiliconFlow、DeepSeek、OpenRouter、模型开放平台、API 文档、SDK 调用、OpenAI 兼容接口、接入示例时触发。
---

# model-platform-guide

这个 skill 用来处理“模型开放平台 API 文档”相关工作。它采用**链接优先、摘要精简、按需访问官方文档**的方式，避免 skill 自身过于臃肿，也减少文档过期风险。

## 当前覆盖平台

- 月之暗面 / Moonshot / Kimi
- 阿里云百炼 / DashScope / Model Studio
- 硅基流动 / SiliconFlow
- DeepSeek
- OpenRouter
- 智谱开放平台 / BigModel
- 火山方舟 / Volcengine Ark
- 腾讯混元
- 百度千帆
- MiniMax

## 主入口

默认先看：`references/index.md`

它现在是整个 skill 的**能力入口总表**，优先用于定位：

- 平台首页
- 模型列表 / 模型概览
- Chat / Responses / Tools / MCP
- Embeddings / Rerank
- Release Notes / 更新入口

## 适用场景

当用户需要以下任一内容时使用：

- 查询某个平台的 API 调用方式
- 对比多个平台的 base URL、鉴权、模型名、SDK 兼容性
- 生成 Python / Node.js / curl 的调用示例
- 解释 OpenAI 兼容接口怎么改造
- 汇总常见错误、流式输出、工具调用、多模态能力
- 编写“模型平台 API 文档”或“接入指南”

## 工作方式

1. 先判断用户要的是：
   - 单个平台文档
   - 多平台对比
   - 接入示例
   - 现有代码迁移
   - 最新模型/能力变化核验
2. 默认先查看 `references/index.md`，定位到对应平台和能力入口。
3. 优先给出：
   - 官方文档入口
   - base URL
   - 认证方式
   - 常用 endpoint
   - 最小可运行示例
4. 只在必要时读取对应 `references/*.md`。
5. 如果 skill 中信息不够或可能过期，优先现场访问官方文档链接，而不是依赖旧摘要。
6. 如果问题涉及“现在是否支持”“最近新增了什么”“某模型是否具备某能力”，默认按 `references/live-check-policy.md` 执行动态核验。
7. 如果问题是“模型 / 联网搜索 / embeddings”这类高变能力问题，优先走 `references/model-search-embedding-checklist.md`。
8. 回复中可以明确说明：skill 内保存的是**精简导航和常用要点**，官方文档才是最终依据。

## 参考文件

### 平台摘要
- 月之暗面：`references/moonshot.md`
- 阿里云百炼：`references/aliyun-bailian.md`
- 硅基流动：`references/siliconflow.md`
- DeepSeek：`references/deepseek.md`
- OpenRouter：`references/openrouter.md`
- 智谱：`references/bigmodel.md`
- 火山方舟：`references/ark.md`
- 腾讯混元：`references/hunyuan.md`
- 百度千帆：`references/qianfan.md`
- MiniMax：`references/minimax.md`

### 横向比较
- 多平台对比：`references/comparison.md`
- 能力矩阵：`references/capability-matrix.md`

### 动态核验
- 文档入口总表：`references/index.md`
- 动态核验策略：`references/live-check-policy.md`
- 模型/联网搜索/Embeddings 核验清单：`references/model-search-embedding-checklist.md`

### 调用模板
- OpenAI 迁移模板：`references/openai-migration.md`
- Python 模板：`references/python-recipes.md`
- Node.js 模板：`references/nodejs-recipes.md`
- curl 模板：`references/curl-recipes.md`

## 输出偏好

默认输出：

- 先给结论
- 再给官方文档链接
- 再给最小可运行示例
- 最后给差异对比或注意事项

如果用户要“写文档/整理文档”，优先输出结构化 Markdown：

- 平台简介
- 官方文档入口
- 鉴权
- Base URL
- 核心接口
- 请求示例
- 响应示例
- 常见坑
- 对比表

如果用户明确要代码模板：

- Python → `references/python-recipes.md`
- Node.js → `references/nodejs-recipes.md`
- curl → `references/curl-recipes.md`
- OpenAI 改造/迁移 → `references/openai-migration.md`

如果用户明确要平台选型、能力横向比较：

- 先读 `references/capability-matrix.md`
- 再按需看 `references/comparison.md`
- 遇到高变能力再结合 `references/live-check-policy.md`

如果用户明确问的是“模型 / 联网搜索 / embeddings”：

- 先读 `references/model-search-embedding-checklist.md`
- 再结合 `references/index.md` 做现场核验

## 维护规则

- 不要把整站原文硬塞进 SKILL.md。
- `references/` 只保留高频字段、最小示例、官方链接和注意事项。
- 当新增平台时，优先新增一个精简 reference 文件，而不是镜像全站文档。
- 如果文档 URL 失效，优先更新 `references/index.md` 和对应平台入口。
- 对于模型能力、最新模型、价格、preview/deprecated 状态等高变信息，不要把本地摘要当成最终依据；优先按 `references/live-check-policy.md` 动态核验。
