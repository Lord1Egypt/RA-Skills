---
name: linkfox-tiktok-video
description: TikTok 视频上传 API 业务技能，支持可购物视频预检、发布、发布状态查询、达人档案查询及大文件分片上传。
---

# TikTok 视频上传 API

TikTok **视频上传模块**业务 skill。经 LinkFox 网关 **`POST /tiktokVideo/developerProxy`** 转发至紫鸟 `tiktok-proxy/creator/{region}/{path}`，调用视频号相关开放接口。参数与响应字段详见 [references/api.md](references/api.md)。

> 前置依赖：`linkfox-tiktok-video-auth` 提供达人授权与 `ttsAccessToken`；`linkfox-tiktok-video-products` 提供 `product_id` 选品。勿使用 `linkfox-tiktok-shop-auth`（TikTok Shop 卖家模块）。

## 能力边界

### ✅ 能力范围

- 经 `/tiktokVideo/developerProxy` 调用视频号开放接口（path 白名单 `affiliate_creator` / `video` / `creator`）。
- 可购物视频内容预检、查询预检结果。
- 发布可购物视频、查询发布状态。
- 达人主页/档案查询（独立功能项，非发布链路必经步骤）。
- 大文件（>10MB）分片上传流程说明。

### ❌ 边界与限制

- **模块隔离**：仅 `/tiktokVideo/developerProxy`；不可用于 `/tiktokShop/*`。
- **白名单**：path 须以 `affiliate_creator` / `video` / `creator` 开头，否则 errcode **1005**。
- **二进制上传限制**：`upload_shoppable_video_file`（multipart）与 `open/` 大文件 init/bind **当前不可**经 proxy；≤10MB 直传待网关 multipart 支持，>10MB 见 [references/large-file-upload.md](references/large-file-upload.md)。
- **封面可选**：发布时可用 `cover_timestamp_ms` 或视频首帧，无需单独封面上传接口。
- **不含授权**：达人/视频号授权、刷新令牌用 `linkfox-tiktok-video-auth`。
- **不含商品查询**：达人店铺/橱窗商品查询、选品、`product_id` 获取用 `linkfox-tiktok-video-products`。
- **不在范围内**：TikTok Shop 小店 ERP（商品/订单/财务）用 `linkfox-tiktok-shop-auth` + 对应业务 skill；TikTok Shop 可购物视频（`/tiktokShop/developerProxy`）用 `linkfox-tiktok-creator`；TikTok 选品/数据分析用 EchoTik 等。

## 执行流程

完整参考链路（MRD 推荐顺序，非强制）：授权 → 选品 → 上传 `file_id` →（可选）预检 → 查预检 → 发布 → 查状态。

### 步骤 0：前置准备（授权与选品）
- 【输入】用户要发布视频的视频号、待发布视频文件、商品锚点。
- 【动作】运行 `python scripts/check_auth_dependency.py`（exit code **42** → 先安装 `linkfox-tiktok-video-auth` 并完成达人授权）；通过 `linkfox-tiktok-video-products` 的 `get_shop_products` / `get_showcase_products` 获取 `product_id`。
- 【输出】`openId`、`product_id`、视频文件路径。

### 步骤 1：取得达人令牌
- 【输入】`openId`（来自授权 skill）。
- 【动作】具名脚本自动调 `/tiktokVideo/accountTokens` 取得 `ttsAccessToken`；或在参数中直接传 `openId` / `ttsAccessToken`。
- 【输出】`ttsAccessToken`（勿向用户明文展示）。

### 步骤 2：上传视频文件取得 file_id
- 【输入】`ttsAccessToken`、视频文件。
- 【动作】≤10MB 走 `upload_shoppable_video_file`（multipart，当前网关暂不支持）；>10MB 走大文件分片三步流程（Initialize → PUT 分片 → Bind，见 references/large-file-upload.md，Step 1/3 当前不可经 proxy）。
- 【输出】`file_id`（`data.video_file.id`）。

### 步骤 3：（可选）内容预检
- 【输入】`file_id`、`product_id`、商品锚点 `title`。
- 【动作】`precheck_shoppable_video` → 保存 `task_id` → `get_shoppable_video_precheck_result` 轮询至终态。
- 【输出】`result`（`SUCCESS` / `FAIL` / `PROCESSING`）；`FAIL` 时查看 `issues[]` 整改后重传/重检。

### 步骤 4：发布可购物视频
- 【输入】`file_id`、`product_id`、`video_info.title`、`product_link_info.title`。
- 【动作】`post_shoppable_video`。
- 【输出】`video.id`（`data.video.id`）。

### 步骤 5：查询发布状态
- 【输入】`video.id`。
- 【动作】`get_shoppable_video_status`，`PROCESSING` 时间隔轮询。
- 【输出】`post_status`（`SUCCESS` / `FAIL` / `PROCESSING`）及 `post_time`。

### 独立功能：获取达人档案
- 【输入】`openId`。
- 【动作】`get_creator_profile`（`affiliate_creator/202508/profiles`），不属于发布链路必经步骤。
- 【输出】达人主页/档案信息。

## 调用方式

- **调用链路**：`accountTokens`（或用户传入 `ttsAccessToken`）→ `developerProxy` → 紫鸟 `tiktok-proxy/creator` → TikTok Open API。
- **path 规则**：相对路径，不含 `tiktok-proxy/creator/{region}/` 前缀；须匹配白名单前缀。
- **响应透传**：网关返回 `httpStatus` / `contentType` / `body`；TikTok 业务层以 `body` 内 JSON 的 `code` / `message` 为准。
- **region**：默认 `global`，与授权 region 保持一致（美国站 `us`）。
- **调用原则**：先看 `developerProxy.httpStatus`，再解析 `body`；GET 业务 query 拼入 `queryString`（不含 `?`），POST/PUT 复杂结构传 `body`（JSON 字符串）或 `requestBody` 对象。
- 通用代理：`python scripts/video_proxy.py '{"path": "...", "method": "GET", "ttsAccessToken": "..."}'`；具名 API：`python scripts/video_api.py '{"api": "...", "openId": "..."}'`。

## 使用示例

**1. 获取达人档案**
```bash
python scripts/get_creator_profile.py '{"openId": "..."}'
```

**2. 内容预检（可选）**
```bash
python scripts/precheck_shoppable_video.py '{"openId": "...", "video_info": {"file_id": "..."}, "product_link_info": {"product_id": "...", "title": "Product anchor"}}'
```
保存返回的 `data.precheck.task_id` 查询预检结果：
```bash
python scripts/get_shoppable_video_precheck_result.py '{"openId": "...", "task_id": "1123123123"}'
```

**3. 发布可购物视频**
```bash
python scripts/post_shoppable_video.py '{"openId": "...", "video_info": {"file_id": "...", "title": "My shoppable video"}, "product_link_info": {"product_id": "...", "title": "Product anchor"}}'
```

**4. 查询发布状态**
```bash
python scripts/get_shoppable_video_status.py '{"openId": "...", "video_id": "7548431509997292816"}'
```

## 展示规则

1. **只呈现数据**：展示接口返回字段，不做主观建议。
2. **令牌安全**：不输出完整 `ttsAccessToken`。
3. **错误说明**：结合网关 errcode 与 TikTok `body.code` / `message` 解释。
4. **无授权时**：引导用户先走 `linkfox-tiktok-video-auth`。

## 用户表达与场景速查

**适用** —— TikTok 视频号视频上传与发布管理：

| 用户说 | 场景 |
|--------|------|
| "上传 TikTok 视频"、"发布可购物视频" | 上传 + 发布 |
| "视频内容预检"、"precheck" | 内容预检 |
| "查预检结果"、"视频是否违规" | 查询预检结果 |
| "查视频是否发布成功"、"视频发布状态" | 查询发布状态 |
| "TikTok 达人主页"、"达人档案" | 获取达人档案 |
| "大文件分片上传视频"、"Large File Upload" | 大文件分片上传 |

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

# TikTok 视频上传 API 参考

本文档收录 TikTok **视频上传模块（`/tiktokVideo`）** 业务接口，经 LinkFox 网关 `/tiktokVideo/developerProxy` 代理至紫鸟 `tiktok-proxy/creator/{region}/{path}`。MRD 可购物视频相关接口已全部收录（见下方总表与参考链路）。

> **授权不在本 skill**：OAuth / 令牌管理见 **`linkfox-tiktok-video-auth`**（`/tiktokVideo/authorizeUrl`、`accountTokens` 等）。

## 调用规范

- **网关代理端点**：`POST /tiktokVideo/developerProxy`
- **Base URL**：`https://tool-gateway.linkfox.com`（默认；可用环境变量 `LINKFOX_TOOL_GATEWAY` 覆盖）
- **Content-Type**：`application/json`
- **网关鉴权**：Header `Authorization: <api_key>`，读取环境变量 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
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
|----------|--------|------|----|------|
| `get_creator_profile` | GET | `affiliate_creator/202508/profiles` | ✅ | 获取达人主页/档案 |
| `upload_shoppable_video_file` | POST | `affiliate_creator/202505/videos/video_files` | ✅ | 上传可购物视频（multipart，见 §4） |
| `large_file_upload_init` | POST | `file/202505/init` | ✅ | 大文件分片 Step 1（见 §5） |
| `large_file_upload_bind` | POST | `file/202505/bind` | ✅ | 大文件分片 Step 3（见 §5） |
| `precheck_shoppable_video` | POST | `affiliate_creator/202511/videos/precheck_task` | ✅ | 可购物视频内容预检 |
| `get_shoppable_video_precheck_result` | GET | `affiliate_creator/202511/videos/precheck_tasks/{task_id}` | ✅ | 查询视频预检结果 |
| `post_shoppable_video` | POST | `affiliate_creator/202603/videos` | ✅ | 发布可购物视频 |
| `get_shoppable_video_status` | GET | `affiliate_creator/202509/videos/{video_id}/status` | ✅ | 查询可购物视频发布状态 |

> Step 2（分片 PUT 至 `upload_url`）不经 LinkFox 网关，无具名 api 登记。详见 `references/large-file-upload.md`。

### 可购物视频参考链路（MRD 推荐顺序，非强制）

以下为 MRD 推荐的**参考顺序**，仅作能力串联说明，**并非强制流程**；实际调用应按用户需求选择接口。

```
授权 (linkfox-tiktok-video-auth)
  → 选品 linkfox-tiktok-video-products（get_shop_products / get_showcase_products）
  → 上传 file_id（§4 直传 ≤10MB 或 §5 大文件分片 >10MB）
  → （可选）预检 precheck_shoppable_video → get_shoppable_video_precheck_result
  → 发布 post_shoppable_video
  → 查状态 get_shoppable_video_status
```

> **预检为可选**：上传获得 `file_id` 后可直接发布，不一定要先做预检。
>
> **`get_creator_profile`（§1）为独立功能项**，用于查询达人主页/档案，**不属于**上述发布链路中的必经步骤。
>
> 章节编号（§1~§9）按接口类型排列，**不等于**调用顺序；参考调用顺序见上表。

**MRD**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f)

---

## 1. 获取达人主页/档案（Get Creator Profile）

- **官方文档**：[get-creator-profile-202508](https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508)
- **上游接口**：`GET /affiliate_creator/202508/profiles`
- **用途**：获取达人的主页/档案信息（creator profile）。
- **定位**：**独立功能项**，不属于可购物视频发布链路的必经步骤；用户需要查看达人档案时单独调用即可。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### 上游请求

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| content-type | 是 | string | `application/json` |
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |

**Query 参数**

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

## 2. 获取可带货商品（已独立 skill）

搜索达人店铺商品、查询橱窗/直播袋商品已拆分为独立 skill **`linkfox-tiktok-video-products`**：

| api 名称 | 说明 |
|----------|------|
| `get_shop_products` | 搜索达人绑定店铺的商品 |
| `get_showcase_products` | 达人橱窗/直播袋商品列表 |

预检（§8）与发布（§6）所需的 **`product_link_info.product_id`**，须通过 **`linkfox-tiktok-video-products`** 查询商品后从返回结果中取得。详见该 skill 的 `references/api.md`。

---

## 4. 上传可购物视频文件（Upload Shoppable Video File）

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

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `multipart/form-data` |

**Query 参数 — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**请求体（multipart/form-data）**

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
选品 (linkfox-tiktok-video-products: get_shop_products / get_showcase_products)
  → 上传视频文件
      ≤ 10MB: upload_shoppable_video_file（multipart，待网关支持）
      > 10MB: 大文件分片三步流程（§5）→ file_id
  → （可选）内容预检 (precheck_shoppable_video，§8) / 发布 (post_shoppable_video，§6) → video.id
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

## 5. 大文件分片上传（Shoppable Video Large File Upload）

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

## 6. 发布可购物视频（Post Shoppable Video）

- **官方文档**：[post-shoppable-video-202603](https://partner.tiktokshop.com/docv2/page/post-shoppable-video-202603)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Post Shoppable Video 章节
- **上游接口**：`POST /affiliate_creator/202603/videos`
- **用途**：将已上传的视频文件与商品锚点绑定后发布到 TikTok（可购物视频）。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。
- **Content-Type**：`application/json`（**可经** `/tiktokVideo/developerProxy` 调用）

### 前置依赖

| 字段来源 | 接口 |
|----------|------|
| `video_info.file_id` | §4 `upload_shoppable_video_file` 或 §5 大文件分片 Bind |
| `product_link_info.product_id` | **`linkfox-tiktok-video-products`** 的 `get_shop_products` 或 `get_showcase_products` |
| `video_info.cover_uri`（可选） | 自定义封面 URI（需单独图片上传 API；不传则用 `cover_timestamp_ms` 或视频首帧） |
| `video_info.cover_timestamp_ms`（可选） | 取指定毫秒处帧作封面；与 `cover_uri` 二选一 |

### 上游请求

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query 参数 — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**请求体（application/json）**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| video_info | 是 | object | 视频信息 |
| video_info.file_id | 是 | string | 视频文件 id，来自上传接口 |
| video_info.title | 是 | string | 视频文案/标题；最长 4000（UTF-16 runes） |
| video_info.cover_uri | 否 | string | 自定义封面 URI（需单独图片上传 API；不传则用 `cover_timestamp_ms` 或首帧） |
| video_info.cover_timestamp_ms | 否 | int32 | 取该时间戳处视频帧作封面；与 `cover_uri` **二选一**；皆传时 `cover_uri` 优先；都不传则用首帧 |
| video_info.music_id | 否 | string | 背景音乐 ID（Search Music Library）；不传则无背景音乐 |
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
    "music_id": "717294069642063456"
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
    "title": "Sample video title"
  },
  "product_link_info": {
    "product_id": "17294069642063424",
    "title": "Sample product anchor title"
  }
}
```

或：

```bash
python scripts/post_shoppable_video.py '{"openId": "...", "video_info": {"file_id": "...", "title": "..."}, "product_link_info": {"product_id": "...", "title": "..."}}'
```

### 通过 developerProxy 调用

```json
{
  "path": "affiliate_creator/202603/videos",
  "method": "POST",
  "ttsAccessToken": "TTP_xxxxx",
  "contentType": "application/json",
  "body": "{\"video_info\":{\"file_id\":\"v12d00gd0024d3nfqr7og65\",\"title\":\"Sample video title\"},\"product_link_info\":{\"product_id\":\"17294069642063424\",\"title\":\"Sample product anchor title\"}}"
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

> 成功发布后保存 **`data.video.id`**，供后续查询发布状态使用。

### 在发布链路中的位置

```
选品 → 上传视频 → file_id
  → （可选）预检 (precheck_shoppable_video，§8) → task_id → 查预检结果 (get_shoppable_video_precheck_result，§9)
  → 发布 (post_shoppable_video，§6) → video.id
  → 查发布状态 (get_shoppable_video_status，§7)
```

---

## 7. 查询可购物视频发布状态（Get Shoppable Video Status）

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

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query 参数 — 由紫鸟自动注入（勿传）**

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

## 8. 可购物视频内容预检（Pre-check Shoppable Video）

- **API Name**：Precheck Video Content
- **官方文档**：[precheck-shoppable-video-202511](https://partner.tiktokshop.com/docv2/page/precheck-shoppable-video-202511)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Pre-check Shoppable Video 章节
- **上游接口**：`POST /affiliate_creator/202511/videos/precheck_task`
- **用途**：发布前预检视频及可购物锚点内容是否违规；返回异步预检任务 `task_id`。
- **定位**：**可选步骤**；上传获得 `file_id` 后用户未要求合规检查时，可直接发布（§6），无需先预检。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。
- **Content-Type**：`application/json`（**可经** `/tiktokVideo/developerProxy` 调用）

### 前置依赖

| 字段来源 | 接口 |
|----------|------|
| `video_info.file_id` | §4 直传 或 §5 大文件 Bind |
| `product_link_info.product_id` | **`linkfox-tiktok-video-products`** 的 `get_shop_products` 或 `get_showcase_products` |

### 上游请求

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query 参数 — 由紫鸟自动注入（勿传）**

| 字段 | 说明 |
|------|------|
| app_key | 应用 key |
| sign | 签名 |
| timestamp | Unix 时间戳（GMT/UTC+0） |

**请求体（application/json）**

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
  → （可选）预检 (precheck_shoppable_video) → task_id → 查预检结果 (get_shoppable_video_precheck_result，§9)
  → 发布 (post_shoppable_video) → video.id → 查发布状态 (§7)
```

> **预检为可选步骤**：用户未要求合规检查时，上传后可直接发布（§6），无需先预检。
>
> 成功提交预检后保存 **`data.precheck.task_id`**，供 §9 查询预检结果。

---

## 9. 查询视频预检结果（Get Shoppable Video Pre-check Result）

- **API Name**：Get Shoppable Video Precheck Result
- **官方文档**：[get-shoppable-video-precheck-result-202511](https://partner.tiktokshop.com/docv2/page/get-shoppable-video-precheck-result-202511)
- **MRD 参考**：[Shoppable video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f) — Get Shoppable Video Pre-check Result 章节
- **上游接口**：`GET /affiliate_creator/202511/videos/precheck_tasks/{task_id}`
- **用途**：根据预检任务 `task_id` 查询视频内容预检结果（异步轮询）。
- **定位**：**可选步骤**，仅在用户已调用 §8 预检时使用；未做预检时可跳过。
- **达人令牌**：需 `user_type=1` 的 creator access_token（`x-tts-access-token`），由 `linkfox-tiktok-video-auth` 授权获得。

### Path 参数

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 预检任务 id，来自 §8 **Pre-check Shoppable Video**（`data.precheck.task_id`） |

### 上游请求

**请求头**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| x-tts-access-token | 是 | string | creator access_token，即 `ttsAccessToken` |
| content-type | 是 | string | `application/json` |

**Query 参数 — 由紫鸟自动注入（勿传）**

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

## 错误码（网关层）

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| HTTP 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| HTTP 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 1002 | 参数校验失败 / 未登录 / 未配置白名单 | 检查 path、method、ttsAccessToken |
| 1003 | 上游（紫鸟）服务或网络异常 | 稍后重试 |
| 1005 | path 未在白名单内 | 确认 path 前缀为 `affiliate_creator` / `video` / `creator` |

**错误响应示例**：

```json
{
  "errcode": 1005,
  "errmsg": "该路径未在白名单内，拒绝中转：..."
}
```

---

## curl 示例

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

## 重要说明

1. **令牌来源**：仅使用 `linkfox-tiktok-video-auth` 取得的 `/tiktokVideo/accountTokens`，勿用 `/tiktokShop/storeTokens`。
2. **令牌安全**：不要向用户明文展示完整 `ttsAccessToken`。
3. **multipart 上传**：若接口要求 `multipart/form-data` 二进制上传，当前通用 `developerProxy` 可能不支持，需在文档中单独标注（待具体接口确认）。
4. **模块隔离**：本 skill 仅走 `/tiktokVideo/developerProxy`；TikTok Shop 达人可购物视频（`/tiktokShop/developerProxy`）见 `linkfox-tiktok-creator`。
