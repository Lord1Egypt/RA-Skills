# TikTok 视频上传 API Reference

本文档收录 TikTok **视频上传模块（`/tiktokVideo`）** 业务接口，经 LinkFox 网关 `/tiktokVideo/developerProxy` 代理至紫鸟 `tiktok-proxy/creator/{region}/{path}`。MRD 可购物视频主链路接口已全部收录（见下方总表与完整链路）。

> **授权不在本 skill**：OAuth / 令牌管理见 **`linkfox-tiktok-video-auth`**（`/tiktokVideo/authorizeUrl`、`accountTokens` 等）。

## Calling Conventions

- **网关代理端点**：`POST /tiktokVideo/developerProxy`
- **Base URL**：`https://tool-gateway.linkfox.com`（默认；可用环境变量 `TIKTOK_VIDEO_API_BASE_URL` 覆盖）
- **Content-Type**：`application/json`
- **网关鉴权**：Header `Authorization: <api_key>`，读取环境变量 `LINKFOXAGENT_API_KEY`
- **达人令牌**：`ttsAccessToken` = creator `access_token`，由 `linkfox-tiktok-video-auth` 授权后从 `/tiktokVideo/accountTokens` 取得，对应上游请求头 **`x-tts-access-token`**
- **签名**：上游 `app_key` / `timestamp` / `sign` 由紫鸟代理自动注入，调用方**无需**传
- **固定 appType**：紫鸟侧固定 `creator`（达人端），**无需**传 `appType` 参数（与 `/tiktokShop/developerProxy` 不同）

### 转发链路

```
Agent / Skill
  → POST /tiktokVideo/developerProxy  (LinkFox 网关)
  → GET|POST|PUT|DELETE https://sbappstoreapi.ziniao.com/tiktok-proxy/creator/{region}/{path}
  → TikTok Creator Open API
```

| 项 | 说明 |
|----|------|
| region | 默认 `global`；美国站可传 `us`（与授权 region 保持一致） |
| path | Creator API **相对路径**，不含 `tiktok-proxy/creator/{region}/` 前缀 |
| method | `GET` / `POST` / `PUT` / `DELETE` |
| ttsAccessToken | creator 授权 `access_token` |

### 路径白名单

网关仅转发 `path` 前缀匹配以下配置之一的请求（`application.yml` → `tiktok-video.developer-proxy.allowed-path-prefixes`）：

| 前缀 | 说明 |
|------|------|
| `affiliate_creator` | 达人 affiliate_creator 系列接口 |
| `video` | 视频相关接口 |
| `creator` | creator 系列接口 |

未在白名单内的 `path` 返回 **errcode 1005**。

### developerProxy 入参

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| path | string | 是 | - | Creator API 相对路径（最长 2048） |
| method | string | 是 | - | `GET` / `POST` / `PUT` / `DELETE` |
| ttsAccessToken | string | 是 | - | creator access_token → 上游 `x-tts-access-token` |
| region | string | 否 | `global` | 区域 |
| queryString | string | 否 | - | 查询字符串（**不含** `?`） |
| body | string | 否 | - | POST/PUT 请求体（通常为 JSON 字符串） |
| contentType | string | 否 | `application/json` | 请求体 Content-Type |

### developerProxy 出参

| 字段 | 类型 | 说明 |
|------|------|------|
| httpStatus | integer | 上游 HTTP 状态码 |
| contentType | string | 响应 Content-Type |
| body | string | TikTok API **原始响应正文**（JSON 字符串） |

> 业务成功/失败以 `body` 解析后的 TikTok 字段（如 `code` / `message`）为准；同时参考 `httpStatus`。

### 通过 video_proxy.py 调用（通用）

```json
{
  "path": "video/example/path",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx"
}
```

POST 示例：

```json
{
  "path": "video/example/path",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "body": "{\"field\": \"value\"}",
  "contentType": "application/json"
}
```

### 通过 video_api.py 调用（已注册端点）

当 `_video_endpoints.py` 中登记了具名 API 后：

```json
{
  "api": "<api_name>",
  "openId": "<creator_open_id>"
}
```

脚本会自动：`accountTokens` → `developerProxy` → 解析 `body`。

具名脚本 / `video_api.py` 返回结构：

| 字段 | 说明 |
|------|------|
| `api` | 调用的 api 名称 |
| `developerProxy` | 网关原始返回（`httpStatus` / `contentType` / `body` 字符串） |
| `resolvedPath` | 实际转发 path（含 path 参数替换后） |
| `data` | 解析后的 TikTok **完整** JSON 响应（含 `code` / `message` / `data` 等） |

> 业务字段通常在 `data.data`（TikTok 响应体内的 `data` 对象）；同时检查 `data.code === 0`。

---

## 已收录接口

| api 名称 | Method | path | proxy | 说明 |
|----------|--------|------|-------|------|
| `get_creator_profile` | GET | `affiliate_creator/202508/profiles` | ✅ | 获取达人主页/档案 |
| `get_shop_products` | GET | `affiliate_creator/202509/shop_products` | ✅ | 搜索达人绑定店铺的商品 |
| `get_showcase_products` | GET | `affiliate_creator/202405/showcases/products` | ✅ | 达人橱窗/直播袋商品列表 |
| `upload_shoppable_video_file` | POST | `affiliate_creator/202505/videos/video_files` | ❌ | 上传可购物视频（multipart，见 §4） |
| `large_file_upload_init` | POST | `open/202505/file/init` | ❌ | 大文件分片 Step 1（见 §5） |
| `large_file_upload_bind` | POST | `open/202505/file/bind` | ❌ | 大文件分片 Step 3（见 §5） |
| `precheck_shoppable_video` | POST | `affiliate_creator/202511/videos/precheck_task` | ✅ | 可购物视频内容预检 |
| `get_shoppable_video_precheck_result` | GET | `affiliate_creator/202511/videos/precheck_tasks/{task_id}` | ✅ | 查询视频预检结果 |
| `post_shoppable_video` | POST | `affiliate_creator/202607/videos` | ✅ | 发布可购物视频 |
| `get_shoppable_video_status` | GET | `affiliate_creator/202509/videos/{video_id}/status` | ✅ | 查询可购物视频发布状态 |

> Step 2（分片 PUT 至 `upload_url`）不经 LinkFox 网关，无具名 api 登记。详见 `references/large-file-upload.md`。

### 可购物视频完整链路（MRD 推荐顺序）

```
授权 (linkfox-tiktok-video-auth)
  → 选品 get_shop_products / get_showcase_products
  → 上传 file_id（§4 直传 ≤10MB 或 §5 大文件分片 >10MB）
  → 预检 precheck_shoppable_video → get_shoppable_video_precheck_result
  → 发布 post_shoppable_video
  → 查状态 get_shoppable_video_status
```

> 章节编号（§1~§9）按接口类型排列，**不等于**调用顺序；调用顺序见上表。

**MRD**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f)

---

## 1. Get Creator Profile（获取达人主页/档案）

- **官方文档**：[get-creator-profile-202508](https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508)
- **上游接口**：`GET /affiliate_creator/202508/profiles`
- **用途**：获取达人的主页/档案信息（creator profile）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |

**Query**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| app_key | 是 | string | 应用 key —— **由紫鸟代理自动注入** |
| sign | 是 | string | 签名 —— **由紫鸟代理自动注入** |
| timestamp | 是 | int | Unix 时间戳（GMT/UTC+0）—— **由紫鸟代理自动注入** |

> 该接口**无业务 Query/Path 入参**；调用时只需 `ttsAccessToken`（或传 `openId` 由脚本自动取 token）。

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202508/profiles",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "region": "global"
}
```

### 通过 get_creator_profile.py / video_api.py 调用

```json
{
  "api": "get_creator_profile",
  "openId": "<creator_open_id>"
}
```

或：

```bash
python scripts/get_creator_profile.py '{"openId": "..."}'
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 达人档案信息（具体字段以接口实际返回为准） |

> `data` 内字段明细以 [官方文档](https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508) 及接口实际返回为准；字段较多时建议用 `response_io.py` 落盘后 `read` 提取。

### 业务错误码

| Code | Message |
|------|---------|
| 16015006 | 该达人当前无选品区域，请联系达人确认已开通 EC 权限 |
| 16015007 | 无销售区域错误：达人没有销售区域 |
| 16501011 | 用户无权限访问该接口，请检查达人授权信息 |
| 16504002 | 查询达人信息失败，请检查达人 EC 权限是否可用 |
| 36009002 | 请求过于频繁（限流），请稍后重试 |

---

## 2. Get Shop Products（搜索达人绑定店铺的商品）

- **官方文档**：[get-shop-products-202509](https://partner.tiktokshop.com/docv2/page/get-shop-products-202509)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Get Shop Products 章节（获取可带货商品流程中的选品步骤）
- **上游接口**：`GET /affiliate_creator/202509/shop_products`
- **用途**：按关键词搜索/检索「与该达人绑定的店铺」中的商品信息，用于后续可购物视频挂车选品。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |

**Query — 业务参数**

| 字段 | 必填 | 类型 | 默认/范围 | 说明 |
|------|------|------|-----------|------|
| title_keyword | 否 | string | — | 商品标题关键词（按标题搜索） |
| sort_field | 否 | string | `PRODUCT_ID` | 排序字段：`PRODUCT_ID` / `PRICE` / `SALE`；为空或非法时取 `PRODUCT_ID` |
| sort_order | 否 | string | `DESC` | 排序方向：`DESC` / `ASC`；为空或非法时取 `DESC` |
| page_size | **是** | int32 | 1~20，推荐 20 | 每页返回商品数 |
| page_token | 否 | string | — | 翻页游标：取上一次响应的 `next_page_token`；首页不传 |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

> 经本 skill 调用时，业务 Query 放入 `queryString` 或脚本 JSON 顶层字段；紫鸟自动注入签名相关参数。

#### sort_field 取值

| 值 | 说明 |
|----|------|
| `PRODUCT_ID` | 按商品 ID（默认） |
| `PRICE` | 按价格 |
| `SALE` | 按销量 |

#### sort_order 取值

| 值 | 说明 |
|----|------|
| `DESC` | 降序（默认） |
| `ASC` | 升序 |

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202509/shop_products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "region": "global",
  "queryString": "title_keyword=apple&sort_field=PRICE&sort_order=DESC&page_size=20"
}
```

翻页示例：

```json
{
  "path": "affiliate_creator/202509/shop_products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "queryString": "page_size=20&page_token=<next_page_token>"
}
```

### 通过 get_shop_products.py / video_api.py 调用

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

或：

```bash
python scripts/get_shop_products.py '{"openId": "...", "title_keyword": "apple", "page_size": 20}'
```

> `get_shop_products.py` / `video_api.py` 未传 `page_size` 时默认 **20**（见 `_video_endpoints` defaults）。

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 商品检索结果（商品列表、`next_page_token` 等，具体字段以接口实际返回为准） |

> 下游发布可购物视频时，从返回商品中取 **`product_id`** 作为 `product_link_info.product_id`。`data` 明细以官方文档及实际返回为准；列表较大时建议 `response_io.py` 落盘提取。

### 翻页

1. 首次请求传 `page_size`（必填），不传 `page_token`。
2. 若 `data.next_page_token` 非空，将其作为下一次请求的 `page_token` 继续拉取。
3. `next_page_token` 为空表示已到末页。

### 业务错误码

| Code | Message |
|------|---------|
| 16015006 | 该达人当前无选品区域，请联系达人确认已开通 EC 权限 |
| 16015007 | 无销售区域错误：达人没有销售区域 |
| 16501011 | 用户无权限访问该接口，请检查达人授权信息 |
| 16504002 | 查询达人信息失败，请检查达人 EC 权限是否可用 |
| 36009002 | 请求过于频繁（限流），请稍后重试 |

---

## 3. Get Showcase Products（达人橱窗/直播袋商品列表）

- **官方文档**：[get-showcase-products-202405](https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405)
- **上游接口**：`GET /affiliate_creator/202405/showcases/products`
- **用途**：列出达人**橱窗（showcase）**中的商品，按 `page_size` 分页、用 `page_token` 翻页（最多约 2000 个商品）。若达人正在直播且 `origin=LIVE`，还会返回直播带货袋（livebag）中的商品。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |

**Query — 业务参数**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| page_size | **是** | int | 每页返回数，范围 **1~20** |
| page_token | 否 | string | 翻页游标：取上一次响应的 `next_page_token`；首页不传 |
| origin | **是** | string | 请求来源：`SHOWCASE`=橱窗；`LIVE`=直播间/livebag |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

#### origin 取值

| 值 | 说明 |
|----|------|
| `SHOWCASE` | 达人橱窗商品（默认） |
| `LIVE` | 直播间带货袋（livebag）商品 |

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202405/showcases/products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "region": "global",
  "queryString": "page_size=20&origin=SHOWCASE"
}
```

翻页示例：

```json
{
  "path": "affiliate_creator/202405/showcases/products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "queryString": "page_size=20&origin=SHOWCASE&page_token=<next_page_token>"
}
```

### 通过 get_showcase_products.py / video_api.py 调用

```json
{
  "api": "get_showcase_products",
  "openId": "<creator_open_id>",
  "page_size": 20,
  "origin": "SHOWCASE"
}
```

或：

```bash
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "SHOWCASE"}'
```

> `get_showcase_products.py` / `video_api.py` 未传时默认 `page_size=20`、`origin=SHOWCASE`。

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 橱窗/直播袋商品列表与分页信息（含 `next_page_token` 等，具体字段以接口实际返回为准） |

> 下游发布可购物视频时，从返回商品中取 **`product_id`** 作为 `product_link_info.product_id`。

### 翻页

1. 首次请求传 `page_size` + `origin`，不传 `page_token`。
2. 若 `data.next_page_token` 非空，作为下一次 `page_token` 继续拉取（保持相同 `origin`）。
3. `next_page_token` 为空表示已到末页。

### 业务错误码

| Code | Message |
|------|---------|
| 18001405 | 该达人账号无选品区域（no selection region） |
| 36009003 | 内部错误，请重试；多次重试仍失败请联系平台支持 |

---

## 4. Upload Shoppable Video File（上传可购物视频文件）

- **官方文档**：[upload-shoppable-video-file-202505](https://partner.tiktokshop.com/docv2/page/upload-shoppable-video-file-202505)（Partner Center，与 MRD 一致）
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Upload Shoppable Video 章节（素材上传步骤）
- **上游接口**：`POST /affiliate_creator/202505/videos/video_files`
- **用途**：在发布可购物视频之前，上传本地视频文件，取得 `data.video_file.id`（后续作为 `video_info.file_id` 使用）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### ⚠️ 当前 LinkFox 限制（必读）

本接口为 **`multipart/form-data` 二进制文件上传**（表单字段 `data` = 视频文件）。当前 `/tiktokVideo/developerProxy` 的 `body` 为**字符串**字段，按 `contentType` 原样构造请求体，**无法承载 multipart 二进制**，因此：

- **暂不能**经 `video_proxy.py` / `video_api.py` / `upload_shoppable_video_file.py` 完成实际上传。
- 本节先收录**上游规范**与文件约束；待网关提供 multipart 上传链路（或大文件分片专用端点）后再补可执行脚本。
- **视频 > 10MB** 时须使用 **§5 大文件分片上传**（`references/large-file-upload.md`）；≤ 10MB 可用本节直传（待网关 multipart 支持）。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `multipart/form-data` |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**Body（multipart/form-data）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| data | 是 | binary | 待上传的本地视频文件 |

### 文件约束

| 约束 | 说明 |
|------|------|
| 支持格式 | MP4、MOV、MKV、WMV、WEBM、AVI、3GP、FLV、MPEG |
| 最大大小 | 100 MB（> 10MB 建议用大文件分片方案） |
| 宽高比 | 9:16 ~ 16:9 |
| 推荐 | 分辨率 ≥ 720p，时长 > 30 秒 |

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息 |
| data.video_file | object | 视频文件信息 |
| data.video_file.id | string | 已上传视频文件 id（**后续发布时作为 `file_id`**） |
| data.video_file.md5 | string | 上传文件的 MD5 校验值 |

**响应示例**

```json
{
  "code": 0,
  "data": {
    "video_file": {
      "id": "123123123123",
      "md5": "D41D8CD98F00B204E9800998ECF8427E"
    }
  },
  "message": "success",
  "request_id": "202410011116276C0AA9039F31B70430A0"
}
```

### 在发布链路中的位置

```
选品 (get_shop_products / get_showcase_products)
  → 上传视频文件
      ≤ 10MB: upload_shoppable_video_file（multipart，待网关支持）
      > 10MB: 大文件分片三步流程（§5）→ file_id
  → 内容预检 (precheck_shoppable_video，§8) / 发布 (post_shoppable_video，§6) → video.id
  → 查发布状态 (get_shoppable_video_status，§7)
```

> 成功上传后保存 **`data.video_file.id`**，供 Post Shoppable Video 等后续步骤使用。

### 预期 developerProxy 调用形态（网关支持 multipart 后）

```json
{
  "path": "affiliate_creator/202505/videos/video_files",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "contentType": "multipart/form-data",
  "body": "<binary multipart — 待网关实现>"
}
```

---

## 5. Shoppable Video Large File Upload（大文件分片上传）

- **MRD 文档**：[Shoppable Video Large File Upload Solution](https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d)
- **Partner Center**：[shoppable-video-large-file-upload](https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload)
- **适用**：可购物视频 **> 10MB**（≤ 10MB 仍用 §4 直传）
- **详细规范**：见 **`references/large-file-upload.md`**（三步流程、分片规则、curl 示例、集成限制）

### 三步概览

| 步骤 | 接口 | 经 LinkFox proxy |
|------|------|------------------|
| 1 Initialize | `POST open/{version}/file/init` | **否**（`open/` 不在白名单） |
| 2 Upload Chunks | `PUT {upload_url}` | **否**（直连文件网关） |
| 3 Bind | `POST open/{version}/file/bind` | **否**（`open/` 不在白名单；bind path 以 Lark 为准） |

### 脚本

```bash
python scripts/large_file_upload.py --help
python scripts/large_file_upload_init.py   # 文档入口，暂不可调用
python scripts/large_file_upload_bind.py   # 文档入口，暂不可调用
```

> 旧版「请求头特殊参数」大文件方案已于 **2026-01-31** 停用。

---

## 6. Post Shoppable Video（发布可购物视频）

- **官方文档**：[post-shoppable-video-202607](https://partner.tiktokshop.com/docv2/page/post-shoppable-video-202607)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Post Shoppable Video 章节
- **上游接口**：`POST /affiliate_creator/202607/videos`（自 202603 升级）
- **用途**：将已上传的视频文件与商品锚点绑定后发布到 TikTok（可购物视频）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。
- **Content-Type**：`application/json`（**可经** `/tiktokVideo/developerProxy` 调用）

### 相对 202603 的变更

| 变更 | 说明 |
|------|------|
| path 版本 | `affiliate_creator/202603/videos` → `affiliate_creator/202607/videos` |
| `video_info.is_ai_generated` | **新增**可选 bool；`true` 时展示 AI 生成内容标识 |
| `video_info.title` 上限 | 官方明确最长 **4000** UTF-16 runes（202603 文档曾写 2200） |
| `data.quota` | **新增**响应字段（如 `3/day`）；成功时返回；失败时可能出现在错误信息中；无配额限制时省略 |

### 前置依赖

| 字段来源 | 接口 |
|----------|------|
| `video_info.file_id` | §4 `upload_shoppable_video_file` 或 §5 大文件分片 Bind |
| `product_link_info.product_id` | §2 `get_shop_products` 或 §3 `get_showcase_products` |
| `video_info.cover_uri`（可选） | 自定义封面 URI（需单独图片上传 API；不传则用 `cover_timestamp_ms` 或视频首帧） |
| `video_info.cover_timestamp_ms`（可选） | 取指定毫秒处帧作封面；与 `cover_uri` 二选一 |
| `video_info.is_ai_generated`（可选） | 是否 AI 生成内容 | 但是最好要选，通过真实标注可以提高账号的稳定性

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**Body（application/json）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_info | 是 | object | 视频信息 |
| video_info.file_id | 是 | string | 视频文件 id，来自上传接口 |
| video_info.title | 是 | string | 视频文案/标题；最长 4000（UTF-16 runes） |
| video_info.cover_uri | 否 | string | 自定义封面 URI（需单独图片上传 API；不传则用 `cover_timestamp_ms` 或首帧） |
| video_info.cover_timestamp_ms | 否 | int32 | 取该时间戳处视频帧作封面；与 `cover_uri` **二选一**；皆传时 `cover_uri` 优先；都不传则用首帧 |
| video_info.music_id | 否 | string | 背景音乐 ID（Search Music Library）；不传则无背景音乐 |
| video_info.is_ai_generated | 否 | bool | 是否 AI 生成内容；`true` 时帖子展示 AI 生成标识 |
| product_link_info | 是 | object | 商品关联信息 |
| product_link_info.product_id | 是 | string | 关联商品 id |
| product_link_info.title | 是 | string | 商品锚点展示标题，建议 < 30 字符 |

**Body 示例**

```json
{
  "video_info": {
    "file_id": "v12d00gd0024d3nfqr7og65",
    "title": "Sample video title",
    "cover_uri": "v12d00gd0024d3nfqr7og65oooiuuyy",
    "cover_timestamp_ms": 1000,
    "music_id": "717294069642063456",
    "is_ai_generated": false
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

### 通过 video_api / post_shoppable_video.py 调用

```json
{
  "api": "post_shoppable_video",
  "openId": "<creator_open_id>",
  "video_info": {
    "file_id": "v12d00gd0024d3nfqr7og65",
    "title": "Sample video title",
    "is_ai_generated": false
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

或：

```bash
python scripts/post_shoppable_video.py '{"openId": "...", "video_info": {"file_id": "...", "title": "...", "is_ai_generated": false}, "product_link_info": {"product_id": "...", "title": "..."}}'
```

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202607/videos",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "contentType": "application/json",
  "body": "{\"video_info\":{\"file_id\":\"v12d00gd0024d3nfqr7og65\",\"title\":\"Sample video title\",\"is_ai_generated\":false},\"product_link_info\":{\"product_id\":\"17294069642063424\",\"title\":\"Sample product anchor title\"}}"
}
```

> `/tiktokVideo/developerProxy` **无需**传 `appType`（与 `/tiktokShop/developerProxy` 不同）。

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息 |
| data.video | object | 已发布视频信息 |
| data.video.id | string | 视频 id，用于查询发布状态（§7 `get_shoppable_video_status`） |
| data.quota | string | 达人发帖配额（如 `3/day`）；成功时返回；失败时可能写入错误信息；无配额限制时省略 |

**响应示例**

```json
{
  "code": 0,
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7",
  "data": {
    "video": {
      "id": "7548431509997292816"
    },
    "quota": "3/day"
  }
}
```

> 成功发布后保存 **`data.video.id`**，供后续查询发布状态使用；可一并关注 **`data.quota`**。

### 在发布链路中的位置

```
选品 → 上传视频 → file_id
  → （可选）预检 (precheck_shoppable_video，§8) → task_id → 查预检结果 (get_shoppable_video_precheck_result，§9)
  → 发布 (post_shoppable_video，§6) → video.id
  → 查发布状态 (get_shoppable_video_status，§7)
```

---

## 7. Get Shoppable Video Status（查询可购物视频发布状态）

- **官方文档**：[get-shoppable-video-status-202509](https://partner.tiktokshop.com/docv2/page/get-shoppable-video-status-202509)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Get Shoppable Video Status 章节
- **上游接口**：`GET /affiliate_creator/202509/videos/{video_id}/status`
- **用途**：查询可购物视频的发布结果/状态（异步发布后轮询）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### Path 参数

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_id | 是 | string | 视频 id，来自 §6 **Post Shoppable Video**（`data.video.id`） |

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

### 通过 get_shoppable_video_status.py 调用

```json
{
  "api": "get_shoppable_video_status",
  "openId": "<creator_open_id>",
  "video_id": "7548431509997292816"
}
```

或：

```bash
python scripts/get_shoppable_video_status.py '{"openId": "...", "video_id": "7548431509997292816"}'
```

### 通过 developerProxy 调用

`video_id` 直接拼进 `path`：

```json
{
  "path": "affiliate_creator/202509/videos/7548431509997292816/status",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx"
}
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息 |
| data.video | object | 视频信息 |
| data.video.id | string | 视频 id |
| data.video.post_status | string | 发布状态：`SUCCESS` / `FAIL` / `PROCESSING` |
| data.video.post_time | int64 | 发布成功时间（秒）；仅当 `post_status=SUCCESS` 时返回 |

**响应示例**

```json
{
  "code": 0,
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7",
  "data": {
    "video": {
      "id": "7493990579714164574",
      "post_status": "FAIL",
      "post_time": 1685548800
    }
  }
}
```

### 业务错误码

| Code | Message |
|------|---------|
| 38007001 | System Error（系统错误） |
| 170001016 | 视频不属于该达人，请检查有效的视频状态 |

### 轮询建议

发布接口（§6）返回 `video.id` 后，若 `post_status=PROCESSING`，可间隔数秒重复调用本接口直至 `SUCCESS` 或 `FAIL`。

---

## 8. Pre-check Shoppable Video（可购物视频内容预检）

- **API Name**：Precheck Video Content
- **官方文档**：[precheck-shoppable-video-202511](https://partner.tiktokshop.com/docv2/page/precheck-shoppable-video-202511)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Pre-check Shoppable Video 章节
- **上游接口**：`POST /affiliate_creator/202511/videos/precheck_task`
- **用途**：发布前预检视频及可购物锚点内容是否违规；返回异步预检任务 `task_id`。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。
- **Content-Type**：`application/json`（**可经** `/tiktokVideo/developerProxy` 调用）

### 前置依赖

| 字段来源 | 接口 |
|----------|------|
| `video_info.file_id` | §4 直传 或 §5 大文件 Bind |
| `product_link_info.product_id` | §2 `get_shop_products` 或 §3 `get_showcase_products` |

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**Body（application/json）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_info | 是 | object | 视频信息 |
| video_info.file_id | 是 | string | 视频文件 id，来自上传接口 |
| product_link_info | 是 | object | 商品关联信息 |
| product_link_info.product_id | 是 | string | 关联商品 id |
| product_link_info.title | 是 | string | 商品锚点展示标题，建议 < 30 字符 |

**Body 示例**

```json
{
  "video_info": {
    "file_id": "v12d00gd0024d3nfqr7og65"
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

> 预检 body 比发布（§6）精简：仅需 `file_id` + 商品锚点信息，**无需** `video_info.title` / 封面 / 音乐等发布字段。

### 通过 precheck_shoppable_video.py 调用

```json
{
  "api": "precheck_shoppable_video",
  "openId": "<creator_open_id>",
  "video_info": {
    "file_id": "v12d00gd0024d3nfqr7og65"
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

或：

```bash
python scripts/precheck_shoppable_video.py '{"openId": "...", "video_info": {"file_id": "..."}, "product_link_info": {"product_id": "...", "title": "..."}}'
```

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202511/videos/precheck_task",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "contentType": "application/json",
  "body": "{\"video_info\":{\"file_id\":\"v12d00gd0024d3nfqr7og65\"},\"product_link_info\":{\"product_id\":\"17294069642063424\",\"title\":\"Sample product anchor title\"}}"
}
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息 |
| data.precheck | object | 视频内容预检任务结果 |
| data.precheck.task_id | string | 预检任务 id（异步，凭此查询预检结果 §9） |

**响应示例**

```json
{
  "code": 0,
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7",
  "data": {
    "precheck": {
      "task_id": "1123123123"
    }
  }
}
```

### 在发布链路中的位置

```
选品 → 上传 → file_id
  → 预检 (precheck_shoppable_video) → task_id → 查预检结果 (get_shoppable_video_precheck_result，§9)
  → result=SUCCESS 后发布 (post_shoppable_video) → video.id → 查发布状态 (§7)
```

> 成功提交预检后保存 **`data.precheck.task_id`**，供 §9 查询预检结果。

---

## 9. Get Shoppable Video Pre-check Result（查询视频预检结果）

- **API Name**：Get Shoppable Video Precheck Result
- **官方文档**：[get-shoppable-video-precheck-result-202511](https://partner.tiktokshop.com/docv2/page/get-shoppable-video-precheck-result-202511)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Get Shoppable Video Pre-check Result 章节
- **上游接口**：`GET /affiliate_creator/202511/videos/precheck_tasks/{task_id}`
- **用途**：根据预检任务 `task_id` 查询视频内容预检结果（异步轮询）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### Path 参数

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 预检任务 id，来自 §8 **Pre-check Shoppable Video**（`data.precheck.task_id`） |

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

### 通过 get_shoppable_video_precheck_result.py 调用

```json
{
  "api": "get_shoppable_video_precheck_result",
  "openId": "<creator_open_id>",
  "task_id": "1123123123"
}
```

或：

```bash
python scripts/get_shoppable_video_precheck_result.py '{"openId": "...", "task_id": "1123123123"}'
```

### 通过 developerProxy 调用

`task_id` 直接拼进 `path`：

```json
{
  "path": "affiliate_creator/202511/videos/precheck_tasks/7493990579714164574",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx"
}
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息 |
| data.precheck_task | object | 视频预检任务 |
| data.precheck_task.id | string | 预检任务 id |
| data.precheck_task.result | string | 预检结果：`SUCCESS`（通过）/ `FAIL`（违规，见 `issues`）/ `PROCESSING`（处理中） |
| data.precheck_task.issues | []object | 失败时的违规明细 |
| data.precheck_task.issues[].risk | string | 违规风险点（如 `Pirated Content`） |
| data.precheck_task.issues[].suggestions | string | 解决建议 |

**响应示例**

```json
{
  "code": 0,
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7",
  "data": {
    "precheck_task": {
      "id": "7493990579714164574",
      "result": "FAIL",
      "issues": [
        {
          "risk": "Pirated Content",
          "suggestions": "Your video may include unoriginal content. Creating original content is essential for standing out from the crowd."
        }
      ]
    }
  }
}
```

### 轮询与发布建议

1. §8 提交预检后保存 `task_id`。
2. 若 `result=PROCESSING`，间隔数秒重复调用本接口。
3. `result=SUCCESS` 后再调用 §6 **Post Shoppable Video** 发布。
4. `result=FAIL` 时查看 `issues[]` 整改后重新上传/预检。

---

## Error Codes（网关层）

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 1002 | 参数校验失败 / 未登录 / 未配置白名单 | 检查 path、method、ttsAccessToken |
| 1003 | 上游（紫鸟）服务或网络异常 | 稍后重试 |
| 1005 | path 未在白名单内 | 确认 path 前缀为 `affiliate_creator` / `video` / `creator` |

**Error Response Example**:

```json
{
  "errcode": 1005,
  "errmsg": "该路径未在白名单内，拒绝中转：..."
}
```

---

## curl Examples

### developerProxy（直接调用网关）

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "video/example",
    "method": "GET",
    "ttsAccessToken": "TTP_xxxxx",
    "region": "global"
  }'
```

---

## Feedback API

> 与工具 API **不同 base URL**，请勿混用。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**: `application/json`

```json
{
  "skillName": "linkfox-tiktok-video",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Video upload API worked as expected."
}
```

**Field rules**:
- `skillName`: 使用本 skill 的 YAML frontmatter `name`
- `sentiment`: `POSITIVE` / `NEUTRAL` / `NEGATIVE`
- `category`: `BUG` / `COMPLAINT` / `SUGGESTION` / `OTHER`
- `content`: 用户说的话、实际发生了什么、为什么是问题或赞赏

---

## Important Notes

1. **令牌来源**：仅使用 `linkfox-tiktok-video-auth` 取得的 `/tiktokVideo/accountTokens`，勿用 `/tiktokShop/storeTokens`。
2. **令牌安全**：不要向用户明文展示完整 `ttsAccessToken`。
3. **multipart 上传**：若接口要求 `multipart/form-data` 二进制上传，当前通用 `developerProxy` 可能不支持，需在文档中单独标注（待具体接口确认）。
4. **模块隔离**：本 skill 仅走 `/tiktokVideo/developerProxy`；TikTok Shop 达人可购物视频（`/tiktokShop/developerProxy`）见 `linkfox-tiktok-creator`。
