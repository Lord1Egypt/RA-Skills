---
name: kaka-cardcrafter
description: 生成小红书爆款图文（标题+正文+多页配图）、公众号/平台多规格封面、知识卡片。分步创作、逐页出图、单页重生，通过卡咔开放平台远程 MCP 或 REST API 完成。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🃏"
    homepage: https://www.cardcrafter.cn/platforms/workbuddy
    primaryEnv: KAKA_API_KEY
    envVars:
      - name: KAKA_API_KEY
        description: 卡咔开放平台 API Key（kc- 开头），在 card.bingotech2022.com「API 接入」页生成
        required: true
      - name: KAKA_BASE_URL
        description: API 地址，默认 https://api.cardcrafter.cn
        required: false
---

# 卡咔 AI 图文生成

通过卡咔开放平台为用户生成三类内容。一篇图文 = 一条 record，三类场景共用 `GET /records/:record_id` 轮询：

| 场景 | 端点前缀 | MCP 工具 | 产物 |
|---|---|---|---|
| 小红书爆款图文 | `/openapi/v1/viral/*` | generate_viral_outline / generate_viral_images | 标题 + 正文 + 3~15 页配图（3:4） |
| 公众号/平台封面 | `/openapi/v1/covers/*` | generate_cover | 一次多规格封面（2.35:1 横版、3:4、9:16） |
| 知识卡片 | `/openapi/v1/cards/*` | generate_card | 文本 → 润色 → 多页卡片（9:16/3:4/1:1） |

计费与网页端同价（按次/按张扣能量），生成失败自动退款，生成记录在卡咔网页端可见。

## 工具面：优先远程 MCP

若环境已连接卡咔远程 MCP（WorkBuddy：插件 → MCP 服务器 → 配置 MCP，端点 `https://api.cardcrafter.cn/mcp`，鉴权 `Authorization: Bearer $KAKA_API_KEY`），**直接用 MCP 工具**：get_me / list_styles / generate_viral_outline / generate_viral_images / generate_cover / generate_card / get_record 等 12 个，与下文 REST 端点一一对应，跳过 curl 写法。

未连接 MCP 时用 REST：Base URL `${KAKA_BASE_URL:-https://api.cardcrafter.cn}`，每个请求带 `Authorization: Bearer $KAKA_API_KEY`。接入教程：https://www.cardcrafter.cn/platforms/workbuddy

## ⚠️ 第一步（必做）：确认有可用的 API Key

调用任何卡咔接口前，先确认环境里有 `KAKA_API_KEY`（以 `kc-` 开头）。**没有、或任何接口返回 401，就停下来引导用户自助创建，不要瞎猜、不要反复重试。** 直接对用户说（可照抄）：

> 你还没配置卡咔 API Key，几步就能拿到：
> 1. 打开 **https://card.bingotech2022.com**，登录你的卡咔账号
> 2. 进入「API 接入」页面（用户中心侧栏 / 移动端「我的」页）
> 3. 点「**生成 API Key**」，复制 `kc-` 开头的 key（明文只显示这一次）
> 4. 回到这里设置环境变量：`export KAKA_API_KEY=kc-你复制的key`
>
> 配好后告诉我，我继续帮你生成。

## 执行规则（必读）

### 1. 场景路由

- 用户说"写小红书 / 小红书图文 / 笔记" → viral；说"公众号封面 / 横版封面" → covers；说"把这些知识点做成卡片" → cards。
- 用户没指定风格就别传 `style` / `style_id` / `visual_style_preset_id`，走服务端默认；用户想挑时先 `GET /styles?scene=viral|cover|card` 列出风格让用户选。
- 封面必须知道规格：先 `GET /covers/platforms` 列出可用平台规格（如 `wechat_article_cover` 2.35:1 横版），让用户挑或按场景推荐。

### 2. 爆款图文默认走「分步模式」，别急着出图

1. `POST /viral/outlines`（**不带** `auto`）先生成大纲；
2. 把返回的**标题、正文、每页配图说明**用 markdown 排版展示给用户，征求意见；
3. 用户提修改意见时，**由你自己改好 pages JSON**，调 `PUT /viral/outlines/:record_id` 整组覆盖更新（不扣能量），再展示；
4. 用户明确确认满意后，才调 `POST /viral/images` 出图。

用户明确说"直接出"时才带 `auto: true`。**封面与卡片没有分步模式**——提交即出图。

### 3. 出图是异步的，靠轮询拿结果

提交出图（viral images / covers / cards）后，**每 15~30 秒**调一次 `GET /records/:record_id`，直到 `status` 进入终态：`completed` / `partial` / `error`。通常需要 2~5 分钟。结果用 markdown 图片列表呈现。

### 4. `partial` 时主动兜底

`status: partial` 表示部分页失败。明确告诉用户哪几页失败，并询问是否单页重生成：viral 用 `POST /viral/images/regenerate`，封面用 `POST /covers/regenerate`，卡片用 `POST /cards/regenerate`。重生成异步，继续轮询。

## 接口速查（REST）

### GET /openapi/v1/me — 账户与能量余额

```bash
curl -sS "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/me" \
  -H "Authorization: Bearer $KAKA_API_KEY"
```

### 爆款图文：大纲 → 出图

```bash
# 1) 生成大纲（同步，30 秒~2 分钟，curl 必须带 --max-time 300）
curl -sS --max-time 300 -X POST "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/viral/outlines" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{"topic": "三伏天养生茶推荐", "page_count": 6}'

# 2) 编辑大纲（整组覆盖 1~15 页，不扣能量；生成中返回 409）
curl -sS -X PUT "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/viral/outlines/rec_xxxx" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{"pages":[{"index":0,"type":"cover","content":"改后的封面说明"}]}'

# 3) 确认后整篇出图（异步）
curl -sS -X POST "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/viral/images" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{"record_id": "rec_xxxx"}'
```

`outlines` 请求字段：`topic`（必填）；`style` / `page_count`（3~15）/ `image_urls`（参考图 1~4 张）/ `auto`（true = 大纲后立即出图）/ `callback_url` 均可选。

### 封面：POST /covers — 多规格封面（异步）

```bash
curl -sS -X POST "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/covers" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "AI 绘画入门指南",
    "subtitle": "零基础 10 分钟上手",
    "platforms": ["wechat_article_cover", "xiaohongshu_cover"],
    "style_type": "shock"
  }'
```

`platforms` 必填 1~5 个（来自 /covers/platforms）；`style_type` 可选 custom/shock/list/compare/pitfall/case。

### 卡片：POST /cards — 知识卡片（异步，一步到位）

```bash
curl -sS -X POST "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/cards" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{"text": "要转成卡片的原文……", "style_id": "从 /styles?scene=card 获取", "ratio": "9:16"}'
```

`text` 必填（原文，服务端自动润色）；`style_id` 必填；`ratio` 可选 9:16/3:4/1:1（默认 9:16）。

### 通用：GET /records/:record_id — 状态轮询

```bash
curl -sS "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/records/rec_xxxx" \
  -H "Authorization: Bearer $KAKA_API_KEY"
```

`status`：draft | generating_outline | generating_images | completed | partial | error。`pages[]` 含 `image_url`（OSS 持久链接），完成后直接以 markdown 图片列表展示给用户。

### 单页重生成（异步）

```bash
curl -sS -X POST "${KAKA_BASE_URL:-https://api.cardcrafter.cn}/openapi/v1/viral/images/regenerate" \
  -H "Authorization: Bearer $KAKA_API_KEY" -H "Content-Type: application/json" \
  -d '{"record_id": "rec_xxxx", "page_index": 2}'
# 封面 / 卡片同理，端点换为 /covers/regenerate、/cards/regenerate（可带 feedback 字段）
```

## 错误处理

非 2xx 统一返回 `{"error":{"code":"...","message":"..."}}`。按状态码处置：

| 状态码 | Agent 该怎么做 |
|---|---|
| 401 | Key 缺失或无效。引导用户自助创建（见上方话术），不要反复重试 |
| 402 | 能量不足。调 `GET /me` 报 `energy_balance`，引导去卡咔网页端充值 |
| 403 / 404 | record_id 不属于当前 key 或不存在，检查参数 |
| 409 | 生成中/已完成，不是错误——继续轮询；整篇重出已完成记录用 `force: true`（仅 viral images） |
| 422 | 参数错误，按 message 修正请求体 |
| 429 | 日配额用尽（`quota_exceeded`）明天再试；提交过频（`rate_limited`）等 2 秒重试 |
| 503 / 5xx | 服务异常，等几秒重试一次；再失败如实报告用户 |

## 注意事项

- 爆款图文单篇 **3~15 页**（含封面）；PUT 编辑必须整组覆盖。
- 大纲接口同步、服务端超时上限 4 分钟——curl 请带 **`--max-time 300`**。
- 请勿并发对同一 record 提交出图（409 保护）。
- 生成内容的归属与合规责任由调用方承担；涉及功效宣称、医疗等敏感品类时提醒用户自行把关文案合规。
