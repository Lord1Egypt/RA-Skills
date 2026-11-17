# TikTok 视频号可带货商品 API Reference

本文档收录 TikTok **视频上传模块（`/tiktokVideo`）** 下的商品查询接口，经 LinkFox 网关 `/tiktokVideo/developerProxy` 代理至紫鸟 `tiktok-proxy/creator/{region}/{path}`。

> **授权不在本 skill**：OAuth / 令牌管理见 **`linkfox-tiktok-video-auth`**。
>
> **下游用途**：返回的 **`product_id`** 供 **`linkfox-tiktok-video`** 的 `precheck_shoppable_video`（预检）与 `post_shoppable_video`（发布）使用。

## Calling Conventions

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

## Error Codes（网关层）

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| HTTP 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| HTTP 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 1002 | 参数校验失败 | 检查 path、method、ttsAccessToken |
| 1003 | 上游异常 | 稍后重试 |
| 1005 | path 未在白名单 | 确认 path 前缀 |

---

## Feedback API

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**: `application/json`

```json
{
  "skillName": "linkfox-tiktok-video-products",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Product query API worked as expected."
}
```

| Field | Required | Description |
|-------|----------|-------------|
| skillName | Yes | `linkfox-tiktok-video-products` |
| sentiment | Yes | `POSITIVE` or `NEGATIVE` |
| category | Yes | `BUG` / `FEATURE_REQUEST` / `OTHER` |
| content | Yes | Feedback description |
