# Zhihu AI Search / 知乎 AI 搜索

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖
知乎 AI 搜索（新版流式）—— 围绕"AI 搜索"的流式问答入口。区别于已下线的异步链路（fetch_ai_search / fetch_ai_search_result），本端点为真实提供的流式版本，单次请求返回 AI 生成的搜索结果。

## 端点索引 (Endpoint Index)
| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_fetch_ai_search_stream | ⭐⭐⭐ 首选 | 获取知乎 AI 搜索（新版流式） | GET | /api/v1/zhihu/web/fetch_ai_search_stream | low |

## 链式调用图谱 (Chain Recipes)

| 用户目标 | 链路 | 字段流 | 容错 |
|---------|------|-------|------|
| AI 搜索 → 关键词文章搜索 | web_fetch_ai_search_stream → search.md fetch_article_search_v3 | 提取 message_content 中的关键词 → `keyword` | AI 搜索失败：降级到普通文章搜索 |

## 跨 reference 链路 (In-Chain)
- **流入本文件**：用户直接提供 `message_content`（自然语言问题）
- **流出本文件**：AI 搜索结果可启发关键词，传给 `search.md` 各搜索端点做精确检索

## 错误处理契约

> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 通用规则
- 404/410 → 防臆造自检后 STOP
- 400/422 → 防臆造自检后修正重试 ≤1 次
- 401/402/403 → STOP
- 429 → 退避重试 ≤2 次
- 5xx → 等 3s 重试 ≤1 次
- 业务 code≠0 → 读 message_zh，不重试

---

## 端点详情

### web_fetch_ai_search_stream — 获取知乎 AI 搜索（新版）

**Full path:** `/api/v1/zhihu/web/fetch_ai_search_stream`
**Method:** GET · **Risk:** low

#### 用途
获取知乎 AI 搜索（新版）结果。**流式版本**，与已下线的异步链路（fetch_ai_search / fetch_ai_search_result）不同——本端点为单次 GET 请求，由  真实提供。

> ⚠️ 注意：本端点 id 在白名单中为 `web_fetch_ai_search_stream`（带 `web_` 前缀），与同文件其他端点命名风格不同，调用前需按白名单逐字符核对。

#### 何时使用 / 不使用
- ✅ 用户想用知乎 AI 直答功能获取 AI 生成的搜索结果
- ✅ 自然语言问题需要 AI 总结性回答
- ❌ 想要传统的关键词搜索列表 → 用 `search.md` 的 `fetch_article_search_v3`

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| message_content | string | yes | — | 用户输入的自然语言问题/AI 搜索内容 |
| chat_mode | string | no | — | 聊天模式（如多轮对话模式） |
| session_id | string | no | — | 会话 ID，用于多轮对话上下文关联 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| — | — | AI 生成的搜索结果（流式返回） | 可提取关键词传给 search.md 各搜索端点 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | message_content 缺失 | STOP，提示用户提供问题 | 0 | — |
| 404 | 端点不存在 | 防臆造自检后 STOP | 0 | **降级**：fetch_article_search_v3 关键词搜索 |
| 5xx | 上游故障 | 等 3s 重试 | ≤1 次 | 降级到普通文章搜索 |
