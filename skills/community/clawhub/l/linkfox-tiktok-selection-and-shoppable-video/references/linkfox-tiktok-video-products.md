---
name: linkfox-tiktok-video-products
description: 查询 TikTok 视频号达人店铺商品与橱窗/直播袋商品，取得 product_id 供可购物视频挂车使用。
---

# TikTok 视频号可带货商品查询

本 skill 负责 TikTok **视频上传模块**下的**商品选品**能力：搜索达人绑定店铺商品、查询达人橱窗/直播袋商品，取得 `product_id` 供后续可购物视频挂车使用。参数与接口详见 [references/api.md](references/api.md)。

> 📌 **前置依赖**：`linkfox-tiktok-video-auth` — 达人授权与 `accessToken`（作为 `ttsAccessToken`）。
>
> 📌 **下游用途**：返回商品中的 **`product_id`** 用于 **`linkfox-tiktok-video`** 的 `precheck_shoppable_video`（预检）与 `post_shoppable_video`（发布）接口中的 `product_link_info.product_id`。

## 能力边界

### ✅ 能力范围

- 搜索达人绑定店铺中的可带货商品（`get_shop_products`），支持关键词与排序。
- 列出达人橱窗或直播间带货袋中的商品（`get_showcase_products`）。
- 从返回结果中提取 `product_id`，供 `linkfox-tiktok-video` 预检/发布可购物视频使用。

### ❌ 边界与限制

- **模块隔离**：仅 `/tiktokVideo/developerProxy`；不可用于 `/tiktokShop/*`。
- **不含授权**：达人/视频号授权、刷新令牌请使用 `linkfox-tiktok-video-auth`。
- **不含视频能力**：上传、预检、发布视频请使用 `linkfox-tiktok-video`。
- **数据范围**：仅达人自有可带货商品；非达人自有商品的选品/数据分析（如 EchoTik）不在范围内。
- **列表较大时**：使用 `response_io.py` 落盘提取字段，避免上下文溢出。

## 执行流程

### 步骤 1：校验授权依赖

- 【输入】本 skill 运行环境
- 【动作】运行 `python scripts/check_auth_dependency.py`；若 exit code 为 **42**，先安装 `linkfox-tiktok-video-auth` 并完成达人授权
- 【输出】确认授权依赖已就绪

### 步骤 2：选定达人并取得令牌

- 【输入】已授权视频号列表
- 【动作】通过 `linkfox-tiktok-video-auth` 的 `authorized_accounts.py` 列出已授权视频号，用户选定 `openId`；runner 自动调 `/tiktokVideo/accountTokens` 取得 `ttsAccessToken`
- 【输出】`openId` 与 `ttsAccessToken`

### 步骤 3：查询商品

- 【输入】`openId`、`ttsAccessToken`、查询条件（关键词/排序/来源/分页游标）
- 【动作】调用 `get_shop_products.py`（店铺商品搜索）或 `get_showcase_products.py`（橱窗/直播袋商品）；如需翻页，将响应中的 `data.next_page_token` 作为下一次 `page_token` 继续拉取
- 【输出】商品列表（含 `product_id`）

### 步骤 4：提取 product_id

- 【输入】步骤 3 返回的商品列表
- 【动作】从商品对象中提取 `product_id`
- 【输出】`product_id`，供 `linkfox-tiktok-video` 的 `precheck_shoppable_video` / `post_shoppable_video` 使用

## 核心概念

- **调用链路**：`accountTokens`（或用户传入 `ttsAccessToken`）→ `developerProxy` → 紫鸟 `tiktok-proxy/creator` → TikTok Open API
- **两类商品来源**：
  - **店铺商品**（`get_shop_products`）：搜索达人绑定店铺中的商品，支持关键词与排序
  - **橱窗/直播袋**（`get_showcase_products`）：列出达人橱窗或直播间带货袋中的商品
- **`product_id` 用途**：预检/发布可购物视频时作为 `product_link_info.product_id`，由 `linkfox-tiktok-video` skill 消费

### 可用脚本

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测是否已安装 `linkfox-tiktok-video-auth` |
| `products_api.py` | 具名 API 入口：JSON 含 `api` 字段 |
| `get_shop_products.py` | 搜索达人绑定店铺商品（`affiliate_creator/202509/shop_products`） |
| `get_showcase_products.py` | 达人橱窗/直播袋商品（`affiliate_creator/202405/showcases/products`） |

共享模块：`_tiktok_video_products_common.py`、`_products_endpoints.py`、`_products_api_runner.py`。

## 使用示例

### 示例 1：搜索达人绑定店铺商品

按标题关键词搜索达人店铺中的可带货商品：

```bash
python scripts/get_shop_products.py '{"openId": "...", "title_keyword": "apple", "page_size": 20}'
```

或：

```bash
python scripts/products_api.py '{"api": "get_shop_products", "openId": "...", "page_size": 20}'
```

从返回商品列表中取 `product_id`，用于 `linkfox-tiktok-video` 的预检/发布。

### 示例 2：查询达人橱窗/直播袋商品

```bash
# 橱窗商品（默认 origin=SHOWCASE）
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20}'

# 直播间带货袋
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "LIVE"}'
```

### 示例 3：翻页拉取更多商品

首次请求不传 `page_token`；若响应含 `data.next_page_token`，将其作为下一次请求的 `page_token` 继续拉取。详见 [references/api.md](references/api.md)。

## 展示规则

1. **只呈现数据**：展示接口返回字段，不做主观选品建议。
2. **令牌安全**：不输出完整 `ttsAccessToken`。
3. **明确 product_id**：用户需要挂车发布时，从商品列表中提取并展示 `product_id`。
4. **无授权时**：引导用户先走 `linkfox-tiktok-video-auth`。

## 用户表达与场景速查

**适用** —— TikTok 视频号达人可带货商品查询：

| 用户说 | 场景 |
|--------|------|
| "查这个达人的店铺商品"、"达人绑定店铺能卖什么" | 店铺商品搜索 |
| "达人橱窗里有哪些商品"、"showcase 商品" | 橱窗商品查询 |
| "直播间带货袋商品"、"直播袋里挂了啥" | 直播袋商品查询 |
| "可带货商品"、"可购物视频选品" | 可购物视频挂车选品 |
| "找 product_id 挂车"、"视频挂车选品" | 取 product_id 供发布 |
| "翻页拉更多商品" | 分页拉取 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# TikTok 视频号可带货商品 API 参考

本文档收录 TikTok **视频上传模块（`/tiktokVideo`）** 下的商品查询接口，经 LinkFox 网关 `/tiktokVideo/developerProxy` 代理至紫鸟 `tiktok-proxy/creator/{region}/{path}`。

> **授权不在本 skill**：OAuth / 令牌管理见 **`linkfox-tiktok-video-auth`**。
>
> **下游用途**：返回的 **`product_id`** 供 **`linkfox-tiktok-video`** 的 `precheck_shoppable_video`（预检）与 `post_shoppable_video`（发布）使用。

## 调用规范

- **网关代理端点**：`POST /tiktokVideo/developerProxy`
- **Base URL**：`https://tool-gateway.linkfox.com`（默认；可用环境变量 `LINKFOX_TOOL_GATEWAY` 覆盖）
- **Content-Type**：`application/json`
- **网关鉴权**：Header `Authorization: <api_key>`，读取环境变量 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **达人令牌**：`ttsAccessToken` = creator `access_token`，由 `linkfox-tiktok-video-auth` 授权后从 `/tiktokVideo/accountTokens` 取得

### developerProxy 入参

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| path | string | 是 | - | Creator API 相对路径 |
| method | string | 是 | - | `GET` / `POST` / `PUT` / `DELETE` |
| ttsAccessToken | string | 是 | - | creator access_token |
| region | string | 否 | `global` | 区域 |
| queryString | string | 否 | - | 查询字符串（**不含** `?`） |

### developerProxy 出参

| 字段 | 类型 | 说明 |
|------|------|------|
| httpStatus | integer | 上游 HTTP 状态码 |
| contentType | string | 响应 Content-Type |
| body | string | TikTok API **原始响应正文**（JSON 字符串） |

### 通过 products_api.py 调用

```json
{
  "api": "<api_name>",
  "openId": "<creator_open_id>"
}
```

具名脚本返回结构：

| 字段 | 说明 |
|------|------|
| `api` | 调用的 api 名称 |
| `developerProxy` | 网关原始返回 |
| `resolvedPath` | 实际转发 path |
| `data` | 解析后的 TikTok 完整 JSON 响应 |

---

## 已收录接口

| api 名称 | Method | path | 说明 |
|----------|--------|------|------|
| `get_shop_products` | GET | `affiliate_creator/202509/shop_products` | 搜索达人绑定店铺的商品 |
| `get_showcase_products` | GET | `affiliate_creator/202405/showcases/products` | 达人橱窗/直播袋商品列表 |

---

## 1. Get Shop Products（搜索达人绑定店铺的商品）

- **官方文档**：[get-shop-products-202509](https://partner.tiktokshop.com/docv2/page/get-shop-products-202509)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Get Shop Products 章节
- **上游接口**：`GET /affiliate_creator/202509/shop_products`
- **用途**：按关键词搜索/检索「与该达人绑定的店铺」中的商品信息，取得 `product_id` 供可购物视频挂车。

### Query — 业务参数

| 字段 | 必填 | 类型 | 默认/范围 | 说明 |
|------|------|------|-----------|------|
| title_keyword | 否 | string | — | 商品标题关键词 |
| sort_field | 否 | string | `PRODUCT_ID` | `PRODUCT_ID` / `PRICE` / `SALE` |
| sort_order | 否 | string | `DESC` | `DESC` / `ASC` |
| page_size | **是** | int32 | 1~20，推荐 20 | 每页返回商品数 |
| page_token | 否 | string | — | 翻页游标 |

#### sort_field 取值

| 值 | 说明 |
|----|------|
| `PRODUCT_ID` | 按商品 ID（默认） |
| `PRICE` | 按价格 |
| `SALE` | 按销量 |

### 通过 get_shop_products.py / products_api.py 调用

```json
{
  "api": "get_shop_products",
  "openId": "<creator_open_id>",
  "title_keyword": "apple",
  "sort_field": "PRICE",
  "sort_order": "DESC",
  "page_size": 20
}
```

```bash
python scripts/get_shop_products.py '{"openId": "...", "title_keyword": "apple", "page_size": 20}'
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码 |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 商品检索结果（含 `next_page_token` 等） |

> 从返回商品中取 **`product_id`**，作为 `linkfox-tiktok-video` 中 `product_link_info.product_id` 使用。

### 翻页

1. 首次请求传 `page_size`，不传 `page_token`。
2. 若 `data.next_page_token` 非空，作为下一次 `page_token` 继续拉取。
3. `next_page_token` 为空表示末页。

### 业务错误码

| Code | Message |
|------|---------|
| 16015006 | 该达人当前无选品区域 |
| 16015007 | 达人没有销售区域 |
| 16501011 | 用户无权限访问该接口 |
| 16504002 | 查询达人信息失败 |
| 36009002 | 请求过于频繁（限流） |

---

## 2. Get Showcase Products（达人橱窗/直播袋商品列表）

- **官方文档**：[get-showcase-products-202405](https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405)
- **上游接口**：`GET /affiliate_creator/202405/showcases/products`
- **用途**：列出达人橱窗或直播间带货袋中的商品，取得 `product_id` 供可购物视频挂车。

### Query — 业务参数

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| page_size | **是** | int | 1~20 |
| page_token | 否 | string | 翻页游标 |
| origin | **是** | string | `SHOWCASE` 或 `LIVE` |

#### origin 取值

| 值 | 说明 |
|----|------|
| `SHOWCASE` | 达人橱窗商品（默认） |
| `LIVE` | 直播间带货袋商品 |

### 通过 get_showcase_products.py / products_api.py 调用

```json
{
  "api": "get_showcase_products",
  "openId": "<creator_open_id>",
  "page_size": 20,
  "origin": "SHOWCASE"
}
```

```bash
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "SHOWCASE"}'
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码 |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 商品列表与分页信息 |

> 从返回商品中取 **`product_id`**，作为 `linkfox-tiktok-video` 中 `product_link_info.product_id` 使用。

### 业务错误码

| Code | Message |
|------|---------|
| 18001405 | 该达人账号无选品区域 |
| 36009003 | 内部错误，请重试 |

---

## 错误码（网关层）

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| HTTP 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| HTTP 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 1002 | 参数校验失败 | 检查 path、method、ttsAccessToken |
| 1003 | 上游异常 | 稍后重试 |
| 1005 | path 未在白名单 | 确认 path 前缀 |
