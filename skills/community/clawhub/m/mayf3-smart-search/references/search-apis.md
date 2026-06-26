# 搜索 API 升级路径

当前方案（web_fetch + HTML 解析）有天花板：需要解析非结构化文本、受反爬限制、无法精确控制结果。
以下 API 方案可返回结构化数据，是质的飞跃。

## 方案对比（v1.7 更新）

| 方案 | 类型 | 免费额度 | 中文支持 | OpenClaw 集成 | 推荐度 |
|------|------|---------|---------|-------------|--------|
| **searchfree.site** | AI 搜索 API | ✅ **完全免费，无 Key** | ⚠️ 英文优/中文不可用 | ✅ 直接 curl/Python | ⭐⭐⭐⭐ |
| **Jina Reader (r.jina.ai)** | URL→Markdown | ✅ **免费，无 Key** | ✅ | ✅ 直接 curl | ⭐⭐⭐⭐⭐ |
| **TinyFish** | 搜索+抓取 API | ✅ 免费（需注册 Key） | ✅ | ✅ 官方 Skill/MCP | ⭐⭐⭐⭐⭐ |
| **Tavily** | AI 搜索 API | ✅ 1000次/月 | ✅ | ✅ 官方插件 | ⭐⭐⭐⭐ |
| **Exa** | 语义搜索 API | ✅ 1000次/月 | ⚠️ 英文优 | ✅ MCP Server | ⭐⭐⭐⭐ |
| **Parallel.ai** | 搜索+提取 API | ✅ 免费（需 Key） | ✅ | ✅ MCP | ⭐⭐⭐⭐ |
| **Bocha（博查）** | 国内 AI 搜索 API | ✅ 有免费额度 | ⭐⭐⭐⭐⭐ | ✅ ClawHub Skill | ⭐⭐⭐⭐ |
| **Serper.dev** | Google SERP API | ✅ 2500次/月免费，无需信用卡 | ✅ | ✅ 直接 HTTP | ⭐⭐⭐⭐ |
| **Brave Search API** | 独立索引搜索 API | ✅ **$5/月免费积分**（需信用卡验证）| ✅ | ✅ 直接 HTTP + MCP | ⭐⭐⭐⭐ |
| **SearXNG** | 自建元搜索引擎 | 无限（自建） | ✅ | ✅ 原生 web_search provider | ⭐⭐⭐⭐ |
| ~~Bing Web Search API~~ | Azure API | ❌ **已退役(2025-08)** | - | - | ❌ |

---

## Jina Reader（r.jina.ai）— 免费 URL 转 Markdown，无需 Key

> 优先使用 DDGS `extract()` 方法（同库一站式，无日限制）。Jina Reader 作为备选方案保留。

**用法：** 在任何 URL 前加 `https://r.jina.ai/`
```bash
curl -s "https://r.jina.ai/https://example.com/article"
```

**核心特性：**
- 🆓 基础免费，无需 API Key（约 **200 次/天** 限制）
- 🧹 自动去除广告、导航、Cookie 弹窗，只留内容
- ⚡ 响应快速（~1s）
- 📝 返回 clean markdown，直接可用于 LLM

**注意：** `s.jina.ai`（搜索端点）需要 API Key，仅 `r.jina.ai`（Reader）免费无 Key。

---

## TinyFish — 免费 Agent 搜索+抓取

**核心特性（2026-05-17 验证）：**
- 🆓 免费计划：Search 5次/分钟 + Fetch 25次/分钟
- 🤖 搜索返回 rank-stable 结构化 JSON
- 🌐 Fetch 端点运行真实浏览器渲染（处理 JS/反爬）
- 🔌 OpenClaw 官方集成（MCP + Skill + CLI）
- ⚠️ 需要注册免费 Key

---

## searchfree.site（完全免费·无需注册）

一个完全免费、无需 API Key 的 AI 搜索 API。

**核心特性：**
- 🆓 **完全免费，无需注册，无需 API Key**
- 🤖 返回 AI 生成的摘要答案 + 结构化结果
- ⏰ 支持时间过滤
- ⚡ 响应约 2-2.5 秒

**⚠️ 局限性：**
- 中文搜索不可用（`country: cn` 参数导致服务不可用）
- 可能随时变更或下线

**调用方式：**
```bash
curl -X POST "https://searchfree.site/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI agents search API comparison", "max_results": 5, "include_answer": true}'
```

---

## Exa — 语义搜索 API

基于神经嵌入的搜索引擎，按含义而非关键词匹配。

**核心特性：**
- 🧠 语义搜索（理解查询含义）
- 🆓 1000 次/月免费
- 🔌 MCP Server 支持
- 适合研究型搜索、概念关联搜索

---

## Tavily（AI 搜索 API）

专为 AI Agent 设计的搜索引擎 API。2026-02 被 Nebius 收购。免费额度：1000 次搜索/月。

## Bocha（博查）

国内 AI 搜索引擎 API，中文搜索质量优秀，0.15 秒响应。

## SearXNG（自建方案）

开源元搜索引擎，聚合多引擎结果，完全自主可控。

## Serper.dev

Google SERP API，2500次/月免费，无需信用卡。

## Brave Search API

$5/月免费积分（需信用卡验证），独立索引。

---

## 当前配置状态

- ✅ **DDGS v9.14.4 已安装**（最新版），brave/bing/yandex/yahoo 后端可用
- ✅ 搜索脚本 `scripts/ddgs_search.py` v3.1
- ✅ searchfree.site 可用（英文搜索）
- ✅ DDGS extract() 可用（全文提取首选）
- ✅ Jina Reader 可用（~200 次/天，备选）
- ✅ DDGS images(), videos(), books(), news() 全部可用
- ✅ web_fetch + Bing CN/360/Sogou 日常够用
- ❌ TinyFish / Exa / Tavily / Bocha 未配置

## 推荐行动

1. **当前已实现**：DDGS v9.14.4 本地搜索 + Jina Reader 全文提取
2. **立即可用**：searchfree.site（免费英文 API）+ Jina Reader（免费 URL→MD）
3. **高优先级**：注册 TinyFish（免费 Agent 搜索+抓取，OpenClaw 原生支持）
4. **中文专项**：安装 Bocha Skill
5. **语义搜索**：注册 Exa（免费语义搜索，1000次/月）
6. **长期**：DDGS API Server + SearXNG 自建
