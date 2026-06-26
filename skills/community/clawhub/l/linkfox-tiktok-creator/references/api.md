# TikTok 达人（Creator）API Reference

本文档收录 TikTok Shop **达人（affiliate_creator）** 开放接口，经 LinkFox 网关 `/tiktokShop/developerProxy` 代理调用。接口随提示文档逐步补充。

## Calling Conventions

- **网关代理端点**：`POST /tiktokShop/developerProxy`
- **Base URL**：`https://tool-gateway.linkfox.com`（默认；可用环境变量 `TIKTOK_SHOP_API_BASE_URL` 覆盖）
- **Content-Type**：`application/json`
- **网关鉴权**：Header `Authorization: <api_key>`，读取环境变量 `LINKFOXAGENT_API_KEY`
- **达人令牌**：`ttsAccessToken` = 达人 access_token（`user_type=1`），由 `linkfox-tiktok-auth`（`appType=creator`）授权获得，对应上游请求头 `x-tts-access-token`
- **签名**：上游 `app_key` / `timestamp` / `sign` 由紫鸟代理自动注入，调用方**无需**传

### developerProxy 入参（通用）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| path | string | 是 | TikTok Shop API 相对路径（不含 tiktok-proxy 前缀），见下方各接口 |
| method | string | 是 | `GET` / `POST` / `PUT` / `DELETE` |
| ttsAccessToken | string | 是 | 达人 access_token（user_type=1） |
| queryString | string | 否 | 查询字符串（不含 `?`） |
| body | string | 否 | POST/PUT 请求体（字符串；当前仅支持文本/JSON，详见下方上传说明） |
| appType | string | 否 | 代理侧应用类型，正则 `^(erp\|creator)$`，默认 `erp`。**达人(affiliate_creator)接口须传 `creator`**（脚本默认已置为 `creator`） |
| region | string | 否 | 默认 `global` |
| contentType | string | 否 | 默认 `application/json` |

> **重要**：所有达人接口（`path` 以 `affiliate_creator/` 开头）调用 `developerProxy` 时 **`appType` 必须为 `creator`**；脚本 `creator_proxy.py` 已默认置为 `creator`。

### developerProxy 返回（通用）

| 字段 | 类型 | 说明 |
|------|------|------|
| httpStatus | integer | 上游 HTTP 状态码 |
| contentType | string | 响应 Content-Type |
| body | string | TikTok Shop API 原始响应正文（JSON 字符串） |

---

## 1. Get Creator Profile（获取达人主页/档案）

- **上游接口**：`GET /affiliate_creator/202508/profiles`
- **用途**：获取达人的主页/档案信息（creator profile）。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |

**Query**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| app_key | 是 | string | 应用 key —— **由紫鸟代理自动注入** |
| sign | 是 | string | 签名 —— **由紫鸟代理自动注入** |
| timestamp | 是 | int | Unix 时间戳（GMT/UTC+0）—— **由紫鸟代理自动注入** |

> 该接口无业务 Query/Path 入参；经本 skill 调用时只需提供 `ttsAccessToken`。

### 通过 developerProxy 调用

```json
{
  "appType": "creator",
  "path": "affiliate_creator/202508/profiles",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx"
}
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 达人档案信息（具体字段以接口实际返回为准） |

> 说明：上游文档的 `data` 字段明细未在本次抓取中展开，**以接口实际返回为准**，必要时落盘后用 `response_io.py read` 查看 `body` 内的字段。

### 错误码

| Code | Message |
|------|---------|
| 16015006 | 该达人当前无选品区域，请联系达人确认已开通 EC 权限 |
| 16015007 | 无销售区域错误：达人没有销售区域 |
| 16501011 | 用户无权限访问该接口，请检查达人授权信息 |
| 16504002 | 查询达人信息失败，请检查达人 EC 权限是否可用 |
| 36009002 | 请求过于频繁（限流），请稍后重试 |

---

## 2. Get Shop Products（搜索达人绑定店铺的商品）

- **上游接口**：`GET /affiliate_creator/202509/shop_products`
- **Host**：`open-api.tiktokglobalshop.com`（经紫鸟代理，调用方无需关心）
- **用途**：按关键词搜索/检索「与该达人绑定的店铺」中的商品信息。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |

**Query**

| 字段 | 必填 | 类型 | 默认/范围 | 说明 |
|------|------|------|-----------|------|
| app_key | 是 | string | — | 应用 key —— **由紫鸟代理自动注入** |
| sign | 是 | string | — | 签名 —— **由紫鸟代理自动注入** |
| timestamp | 是 | int64 | — | Unix 时间戳（GMT/UTC+0）—— **由紫鸟代理自动注入** |
| title_keyword | 否 | string | — | 商品标题关键词（按标题搜索） |
| sort_field | 否 | string | `PRODUCT_ID` | 排序字段：`PRODUCT_ID` / `PRICE` / `SALE`；为空或非法时取 `PRODUCT_ID` |
| sort_order | 否 | string | `DESC` | 排序方向：`DESC` / `ASC`；为空或非法时取 `DESC` |
| page_size | 是 | int32 | 1~20，推荐 20 | 每页返回商品数 |

> 经本 skill 调用时，业务 Query（`title_keyword` / `sort_field` / `sort_order` / `page_size`）放入 `queryString`；`app_key` / `sign` / `timestamp` 由紫鸟自动注入。翻页游标（如有 `page_token` / `next_page_token`）以接口实际返回为准。

### 通过 developerProxy 调用

```json
{
  "appType": "creator",
  "path": "affiliate_creator/202509/shop_products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "queryString": "title_keyword=apple&sort_field=PRICE&sort_order=DESC&page_size=20"
}
```

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 商品检索结果（商品列表、分页游标等，具体字段以接口实际返回为准） |

> 说明：本次抓取的上游文档未展开 `data` 字段与错误码明细，**以接口实际返回为准**；建议落盘后用 `response_io.py read` 查看 `body` 内字段。

---

## 3. Get Showcase Products（达人橱窗商品列表）

- **上游接口**：`GET /affiliate_creator/202405/showcases/products`
- **用途**：列出达人**橱窗（showcase）**中的商品，按 `page_size` 分页、用 `page_token` 翻页，最多 2000 个商品。若达人正在直播，还会返回直播带货袋（livebag）中的商品。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |

**Query**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| app_key | 是 | string | 应用 key —— **由紫鸟代理自动注入** |
| sign | 是 | string | 签名 —— **由紫鸟代理自动注入** |
| timestamp | 是 | int | Unix 时间戳（GMT/UTC+0）—— **由紫鸟代理自动注入** |
| page_size | 是 | int | 每页返回数，范围 1~20 |
| page_token | 否 | string | 翻页游标：取上一次响应的 `next_page_token`；首页不需要 |
| origin | 是 | string | 请求来源：`LIVE`=来自直播间；`SHOWCASE`=来自橱窗 |

### 通过 developerProxy 调用

```json
{
  "appType": "creator",
  "path": "affiliate_creator/202405/showcases/products",
  "method": "GET",
  "ttsAccessToken": "TTP_xxxxx",
  "queryString": "page_size=20&origin=SHOWCASE"
}
```

> 翻页：从上一次响应的 `data.next_page_token` 取值，作为下一次 `queryString` 中的 `page_token`。

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码（成功/失败） |
| message | string | 业务消息；失败时说明原因 |
| request_id | string | 请求日志 ID |
| data | object | 橱窗商品列表与分页信息（含 `next_page_token` 等，具体字段以接口实际返回为准） |

### 错误码

| Code | Message |
|------|---------|
| 18001405 | 该达人账号无选品区域（no selection region） |
| 36009003 | 内部错误，请重试；多次重试仍失败请联系平台支持 |

---

## 4. Upload Shoppable Video File（上传可购物视频文件）

- **上游接口**：`POST /affiliate_creator/202505/videos/video_files`
- **用途**：在发布到 TikTok 之前，上传可购物视频文件。**视频 > 10MB 时**改用「Shoppable Video Large File Upload Solution」（大文件分片方案，另见后续文档）。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。
- **⚠️ 上传方式（当前限制）**：本接口为 **`multipart/form-data` 二进制文件上传**。当前 LinkFox 网关 `/tiktokShop/developerProxy` 的 `body` 为**字符串**字段、按 `contentType` 原样构造请求体，**无法承载 multipart 二进制文件**，因此该上传接口**暂不能**经通用 `developerProxy` / `creator_proxy.py` 调用。需要网关侧提供支持 multipart 的上传链路（或使用大文件分片方案的专用上传端点）后再补脚本。本节先收录上游规范。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |
| content-type | 是 | string | `multipart/form-data` |

**Query**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| app_key | 是 | string | 应用 key —— **由紫鸟代理自动注入** |
| sign | 是 | string | 签名 —— **由紫鸟代理自动注入** |
| timestamp | 是 | int64 | Unix 时间戳（GMT/UTC+0）—— **由紫鸟代理自动注入** |

**Body（multipart/form-data）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| data | 是 | binary | 待上传的本地视频文件 |

**文件约束**

- 支持格式：MP4、MOV、MKV、WMV、WEBM、AVI、3GP、FLV、MPEG
- 最大视频大小：100 MB（> 10MB 建议用大文件分片方案）
- 视频宽高比：9:16 ~ 16:9
- 推荐：分辨率 ≥ 720p，时长 > 30 秒

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息（见下） |
| data.video_file | object | 视频文件信息 |
| data.video_file.id | string | 已上传视频文件的 id（后续发布可购物视频时引用） |
| data.video_file.md5 | string | 上传文件的 md5 校验值 |

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

---

## 5. Post Shoppable Video（发布可购物视频）

- **上游接口**：`POST /affiliate_creator/202603/videos`
- **用途**：发布可购物视频（将已上传的视频文件与商品锚点绑定后发布到 TikTok）。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。
- **Content-Type**：`application/json`（JSON body，可经 `creator_proxy.py` / `developerProxy` 的 `body` 传入）。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query**：`app_key` / `sign` / `timestamp` —— **由紫鸟代理自动注入**。

**Body（application/json）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_info | 是 | object | 视频信息（见下） |
| video_info.file_id | 是 | string | 视频文件 id，来自 **Upload Shoppable Video File** |
| video_info.title | 是 | string | 视频文案/标题；最长 4000（UTF-16 runes） |
| video_info.cover_uri | 否 | string | 封面图 URI，来自 **Upload Shoppable Photo File** API |
| video_info.cover_timestamp_ms | 否 | int32 | 取该时间戳处的视频帧作为封面；与 `cover_uri` **二选一**，二者皆传时以 `cover_uri` 优先；都不传则用视频首帧 |
| video_info.music_id | 否 | string | 背景音乐 ID（来自 Search Music Library）；不传则无背景音乐 |
| product_link_info | 是 | object | 商品关联信息（见下） |
| product_link_info.product_id | 是 | string | 关联商品 id，来自 **Get Shop Products** / **Get Showcase Products** |
| product_link_info.title | 是 | string | 商品锚点展示标题，建议 < 30 字符 |

**Body 示例**

```json
{
  "video_info": {
    "file_id": "v12d00gd0024d3nfqr7og65",
    "title": "Sample video title",
    "cover_uri": "v12d00gd0024d3nfqr7og65oooiuuyy",
    "cover_timestamp_ms": 1000,
    "music_id": "717294069642063456"
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

### 通过 developerProxy 调用

```json
{
  "appType": "creator",
  "path": "affiliate_creator/202603/videos",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "contentType": "application/json",
  "body": "{\"video_info\":{\"file_id\":\"v12d00gd0024d3nfqr7og65\",\"title\":\"Sample video title\"},\"product_link_info\":{\"product_id\":\"17294069642063424\",\"title\":\"Sample product anchor title\"}}"
}
```

> `body` 为 JSON **字符串**（注意转义）；`file_id` 来自接口 4，`product_id` 来自接口 2/3，`cover_uri` 来自 Upload Shoppable Photo File。

### 上游响应

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int32 | 业务状态码（0=成功） |
| message | string | 业务消息 |
| request_id | string | 请求日志 ID |
| data | object | 返回信息（见下） |
| data.video | object | 已发布视频信息 |
| data.video.id | string | 视频 id，可用于查询视频发布状态 |

**响应示例**

```json
{
  "code": 0,
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7",
  "data": {
    "video": {
      "id": "7548431509997292816"
    }
  }
}
```

---

## 6. Get Shoppable Video Status（查询可购物视频发布状态）

- **上游接口**：`GET /affiliate_creator/202509/videos/{video_id}/status`
- **用途**：查询可购物视频的发布结果/状态。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。

### 上游请求

**Path 参数**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_id | 是 | string | 视频 id，来自 **Post Shoppable Video**（`data.video.id`） |

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query**：`app_key` / `sign` / `timestamp` —— **由紫鸟代理自动注入**。

### 通过 developerProxy 调用

`video_id` 直接拼进 `path`：

```json
{
  "appType": "creator",
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
| data | object | 返回信息（见下） |
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

### 错误码

| Code | Message |
|------|---------|
| 38007001 | System Error（系统错误） |
| 170001016 | 视频不属于该达人，请检查有效的视频状态 |

---

## 7. Pre-check Shoppable Video（可购物视频内容预检）

- **API Name**：Precheck Video Content
- **上游接口**：`POST /affiliate_creator/202511/videos/precheck_task`
- **用途**：在发布前预检视频及可购物锚点内容是否存在违规。返回一个异步预检任务 `task_id`。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。
- **Content-Type**：`application/json`。

### 上游请求

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query**：`app_key` / `sign` / `timestamp` —— **由紫鸟代理自动注入**。

**Body（application/json）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_info | 是 | object | 视频信息 |
| video_info.file_id | 是 | string | 视频文件 id，来自 **Upload Shoppable Video File** |
| product_link_info | 是 | object | 商品关联信息 |
| product_link_info.product_id | 是 | string | 关联商品 id，来自 **Get Shop Products** / **Get Showcase Products** |
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

### 通过 developerProxy 调用

```json
{
  "appType": "creator",
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
| data | object | 返回信息（见下） |
| data.precheck | object | 视频内容预检任务结果 |
| data.precheck.task_id | string | 预检任务 id（异步，后续凭此查询预检结果） |

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

---

## 8. Get Shoppable Video Pre-check Result（查询视频预检结果）

- **API Name**：Get Shoppable Video Precheck Result
- **上游接口**：`GET /affiliate_creator/202511/videos/precheck_tasks/{task_id}`
- **用途**：根据预检任务 `task_id` 查询视频内容预检结果。
- **达人令牌**：需 `user_type=1` 的达人 access_token（`x-tts-access-token`）。

### 上游请求

**Path 参数**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 预检任务 id，来自 **Pre-check Shoppable Video**（`data.precheck.task_id`） |

**Header**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | 达人 access_token（user_type=1），即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query**：`app_key` / `sign` / `timestamp` —— **由紫鸟代理自动注入**。

### 通过 developerProxy 调用

`task_id` 直接拼进 `path`：

```json
{
  "appType": "creator",
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
| data | object | 返回信息（见下） |
| data.precheck_task | object | 视频预检任务 |
| data.precheck_task.id | string | 预检任务 id |
| data.precheck_task.result | string | 预检结果：`SUCCESS`=通过；`FAIL`=因违规未通过（详见 `issues`）；`PROCESSING`=仍在处理中 |
| data.precheck_task.issues | []object | 失败时返回的违规明细列表（见下） |
| data.precheck_task.issues[].risk | string | 违规风险点（如 `Pirated Content`） |
| data.precheck_task.issues[].suggestions | string | 解决该违规的详细建议 |

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

---

## curl 示例

```bash
# Get Creator Profile
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202508/profiles", "method": "GET", "ttsAccessToken": "TTP_xxxxx"}'

# Get Shop Products
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202509/shop_products", "method": "GET", "ttsAccessToken": "TTP_xxxxx", "queryString": "title_keyword=apple&page_size=20"}'

# Get Showcase Products
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202405/showcases/products", "method": "GET", "ttsAccessToken": "TTP_xxxxx", "queryString": "page_size=20&origin=SHOWCASE"}'

# Post Shoppable Video
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202603/videos", "method": "POST", "ttsAccessToken": "TTP_xxxxx", "contentType": "application/json", "body": "{\"video_info\":{\"file_id\":\"v12d0...\",\"title\":\"Sample\"},\"product_link_info\":{\"product_id\":\"172940...\",\"title\":\"Anchor\"}}"}'

# Get Shoppable Video Status
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202509/videos/7548431509997292816/status", "method": "GET", "ttsAccessToken": "TTP_xxxxx"}'

# Pre-check Shoppable Video
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202511/videos/precheck_task", "method": "POST", "ttsAccessToken": "TTP_xxxxx", "contentType": "application/json", "body": "{\"video_info\":{\"file_id\":\"v12d0...\"},\"product_link_info\":{\"product_id\":\"172940...\",\"title\":\"Anchor\"}}"}'

# Get Shoppable Video Pre-check Result
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"appType": "creator", "path": "affiliate_creator/202511/videos/precheck_tasks/7493990579714164574", "method": "GET", "ttsAccessToken": "TTP_xxxxx"}'
```

---

## Feedback API

> 本接口与上面的工具 API **是不同 base URL**，请勿混用。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**: `application/json`

```json
{
  "skillName": "linkfox-tiktok-creator",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Creator profile fetched successfully, user was satisfied."
}
```

**Field rules**:
- `skillName`: 使用本 skill 的 YAML frontmatter `name`
- `sentiment`: `POSITIVE` / `NEUTRAL` / `NEGATIVE`
- `category`: `BUG` / `COMPLAINT` / `SUGGESTION` / `OTHER`
- `content`: 用户说的话、实际发生了什么、为什么是问题或赞赏
