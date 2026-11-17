---
name: linkfox-tiktok-video
description: TikTok 视频上传 API 业务技能，经 /tiktokVideo/developerProxy 转发紫鸟 tiktok-proxy/creator 调用视频号相关开放接口（path 白名单 affiliate_creator / video / creator）。依赖 linkfox-tiktok-video-auth 取得 ttsAccessToken。当用户提到 TikTok 视频上传、上传 TikTok 视频、发布 TikTok 视频、Post Shoppable Video、发布可购物视频、Pre-check Shoppable Video、Get Shoppable Video Pre-check Result、视频内容预检、预检结果、precheck、Get Shoppable Video Status、视频发布状态、查视频是否发布成功、TikTok 达人主页、达人档案、Get Creator Profile、搜索达人店铺商品、Get Shop Products、达人橱窗商品、Get Showcase Products、showcase 商品、可带货商品、大文件分片上传、Large File Upload、分片上传视频、TikTok video upload、TikTok 视频 API、/tiktokVideo 业务接口、查询/管理 TikTok 视频号视频 时触发。即使未明确说「授权」，只要需求是通过已授权视频号执行视频上传、预检、查预检结果、发布、查发布状态、达人档案查询、店铺/橱窗商品选品或大文件上传（非 TikTok Shop 小店 ERP），也应触发。**不含授权**（授权用 linkfox-tiktok-video-auth）。
---

# TikTok 视频上传 API

TikTok **视频上传模块**业务 skill。经 LinkFox 网关 **`POST /tiktokVideo/developerProxy`** 转发至紫鸟 `tiktok-proxy/creator/{region}/{path}`，调用视频号相关开放接口。

> 📌 **前置依赖**：`linkfox-tiktok-video-auth` — 达人授权与 `accessToken`（作为 `ttsAccessToken`）。**勿使用** `linkfox-tiktok-shop-auth`（TikTok Shop 卖家模块）。

> 📌 **MRD 主链路已齐**：选品 → 上传 → 预检 → 发布 → 查状态；详见 `references/api.md` 总表与完整链路。

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-tiktok-video-auth`** 并完成达人授权。
2. **不要**在本 skill 内实现授权/令牌刷新逻辑（回到 auth skill）。

## Core Concepts

- **调用链路**：`accountTokens`（或用户传入 `ttsAccessToken`）→ `developerProxy` → 紫鸟 `tiktok-proxy/creator` → TikTok Open API
- **path 规则**：相对路径，不含 `tiktok-proxy/creator/{region}/` 前缀；须匹配白名单前缀 `affiliate_creator` / `video` / `creator`
- **响应透传**：网关返回 `httpStatus` / `contentType` / `body`；TikTok 业务层以 `body` 内 JSON 的 `code` / `message` 为准
- **region**：默认 `global`，与授权 region 保持一致（美国站 `us`）

## API Usage

详见 `references/api.md`（含 developerProxy 入参/出参、path 白名单、错误码）。已登记具名 API 见 `_video_endpoints.py`；暂无登记时可用通用代理。

### Available Scripts

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测是否已安装 `linkfox-tiktok-video-auth` |
| `video_proxy.py` | **通用代理**：任意白名单 path + method + ttsAccessToken |
| `video_api.py` | **具名 API 入口**：JSON 含 `api` 字段 |
| `get_creator_profile.py` | 获取达人主页/档案（`affiliate_creator/202508/profiles`） |
| `get_shop_products.py` | 搜索达人绑定店铺商品（`affiliate_creator/202509/shop_products`） |
| `get_showcase_products.py` | 达人橱窗/直播袋商品（`affiliate_creator/202405/showcases/products`） |
| `upload_shoppable_video_file.py` | 上传可购物视频文件（**multipart，暂不可经 proxy 调用**，见限制） |
| `large_file_upload.py` | 大文件分片上传流程说明（> 10MB，见 `references/large-file-upload.md`） |
| `large_file_upload_init.py` | 大文件 Step 1 初始化（**暂不可经 proxy 调用**） |
| `large_file_upload_bind.py` | 大文件 Step 3 绑定业务资源（**暂不可经 proxy 调用**） |
| `post_shoppable_video.py` | 发布可购物视频（`affiliate_creator/202607/videos`） |
| `get_shoppable_video_status.py` | 查询可购物视频发布状态（`.../videos/{video_id}/status`） |
| `precheck_shoppable_video.py` | 可购物视频内容预检（`affiliate_creator/202511/videos/precheck_task`） |
| `get_shoppable_video_precheck_result.py` | 查询视频预检结果（`.../precheck_tasks/{task_id}`） |

共享模块：`_tiktok_video_common.py`、`_video_endpoints.py`、`_video_api_runner.py`。

## 标准前置流程（选号 → 取令牌 → 调业务）

1. **`linkfox-tiktok-video-auth`**：`authorized_accounts.py` 列出已授权视频号 → 用户选定 `openId`
2. 取令牌：`account_tokens.py` 或在本 skill 参数中传 `openId`（runner 自动调 `/tiktokVideo/accountTokens`）
3. 调业务：`video_api.py`（已登记 API）或 `video_proxy.py`（path/method/ttsAccessToken）

| 用户上下文 | Agent 动作 |
|-----------|------------|
| 只授权 1 个视频号 | 直接取该 `openId` |
| 多个视频号 + 只说昵称 | 按 `displayName` 向用户澄清 |
| 已给 `openId` 或 `ttsAccessToken` | 直接使用 |

**静默原则**：不要在摘要里还原完整 token；脚本内部使用完整 `accessToken` 调代理即可。

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再解析 `body` 中 TikTok 业务字段
- GET：业务 query 拼入 `queryString`（不含 `?`）
- POST/PUT：复杂结构传 `body`（JSON 字符串）或 `requestBody` 对象
- path 不在白名单 → errcode **1005**，检查前缀或联系管理员开放配置

## Usage Scenarios

### 推荐完整链路（MRD）

```
授权 → 选品 → 上传 file_id → 预检 → 查预检 → 发布 → 查发布状态
```

对应 Scenario 3/4（选品）→ 5/6（上传）→ 7（预检+查结果）→ 8（发布）→ 9（查状态）。

### Scenario 1: 通用转发（尚无具名脚本时）

```bash
python scripts/video_proxy.py '{"path": "video/...", "method": "GET", "ttsAccessToken": "TTP_xxx"}'
```

### Scenario 2: 获取达人主页/档案

```bash
python scripts/get_creator_profile.py '{"openId": "..."}'
```

或：

```bash
python scripts/video_api.py '{"api": "get_creator_profile", "openId": "..."}'
```

### Scenario 3: 搜索达人绑定店铺商品（选品）

```bash
python scripts/get_shop_products.py '{"openId": "...", "title_keyword": "apple", "page_size": 20}'
```

返回的 `product_id` 可用于后续可购物视频发布挂车。

### Scenario 4: 查询达人橱窗/直播袋商品

```bash
# 橱窗商品（默认 origin=SHOWCASE）
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20}'

# 直播间带货袋
python scripts/get_showcase_products.py '{"openId": "...", "page_size": 20, "origin": "LIVE"}'
```

### Scenario 5: 上传可购物视频文件（规范已收录，暂不可调用）

上游为 `POST affiliate_creator/202505/videos/video_files`（multipart）。当前网关不支持，Agent 应：

1. 向用户说明暂无法经本 skill 自动上传二进制视频；
2. 引用 `references/api.md` §4 的文件格式/大小约束；
3. 若用户已有 `file_id`，可继续预检（Scenario 7）或发布（Scenario 8）步骤。

```bash
python scripts/upload_shoppable_video_file.py --help
```

### Scenario 6: 大文件分片上传（> 10MB，规范已收录）

视频 **> 10MB** 时走三步分片方案（Initialize → PUT 分片 → Bind），详见 `references/large-file-upload.md` 与 `references/api.md` §5。

1. 向用户说明 Step 1/3 的 `open/` path 当前不在 developerProxy 白名单，暂不能经本 skill 自动完成；
2. Step 2 须客户端直连 Step 1 返回的 `upload_url` 上传分片；
3. ≤ 10MB 仍优先 §4 直传（multipart 待网关支持）。

```bash
python scripts/large_file_upload.py --help
```

### Scenario 7: 可购物视频内容预检

发布前预检视频与商品锚点是否违规：

```bash
python scripts/precheck_shoppable_video.py '{
  "openId": "...",
  "video_info": {"file_id": "..."},
  "product_link_info": {"product_id": "...", "title": "Product anchor"}
}'
```

保存返回的 **`data.precheck.task_id`**，用于查询预检结果：

```bash
python scripts/get_shoppable_video_precheck_result.py '{"openId": "...", "task_id": "1123123123"}'
```

`result` 为 `SUCCESS` / `FAIL` / `PROCESSING`；`FAIL` 时查看 `issues[]`；`PROCESSING` 可间隔轮询。

### Scenario 8: 发布可购物视频

将已上传的 `file_id` 与选品得到的 `product_id` 绑定发布：

```bash
python scripts/post_shoppable_video.py '{
  "openId": "...",
  "video_info": {"file_id": "...", "title": "My shoppable video", "is_ai_generated": false},
  "product_link_info": {"product_id": "...", "title": "Product anchor"}
}'
```

或：

```bash
python scripts/video_api.py '{"api": "post_shoppable_video", "openId": "...", "video_info": {"file_id": "...", "title": "...", "is_ai_generated": false}, "product_link_info": {"product_id": "...", "title": "..."}}'
```

- 可选：`video_info.is_ai_generated`（bool）— 为 `true` 时标记为 AI 生成内容
- 发布后保存返回的 **`data.video.id`**，用于查询发布状态；成功时可能返回 **`data.quota`**（如 `3/day`）

### Scenario 9: 查询可购物视频发布状态

```bash
python scripts/get_shoppable_video_status.py '{"openId": "...", "video_id": "7548431509997292816"}'
```

`post_status` 为 `SUCCESS` / `FAIL` / `PROCESSING`；若为 `PROCESSING` 可间隔轮询。

### Scenario 10: 其他具名 API

```bash
python scripts/video_api.py '{"api": "<api_name>", "openId": "..."}'
```

## Display Rules

1. **只呈现数据**：展示接口返回字段，不做主观建议。
2. **令牌安全**：不输出完整 `ttsAccessToken`。
3. **错误说明**：结合网关 errcode 与 TikTok `body.code` / `message` 解释。
4. **无授权时**：引导用户先走 `linkfox-tiktok-video-auth`。

## Important Limitations

- **模块隔离**：仅 `/tiktokVideo/developerProxy`；不可用于 `/tiktokShop/*`。
- **白名单**：path 须以 `affiliate_creator` / `video` / `creator` 开头。
- **二进制上传限制**：`upload_shoppable_video_file`（multipart）与 `open/` 大文件 init/bind **当前不可**经 proxy；≤10MB 直传待网关 multipart 支持，>10MB 见 `references/large-file-upload.md`。
- **封面可选**：发布时可用 `cover_timestamp_ms` 或视频首帧，无需单独封面上传接口亦可发布。

## Not Applicable

| 场景 | 应使用的 skill |
|------|----------------|
| 达人/视频号 **授权**、刷新令牌 | `linkfox-tiktok-video-auth` |
| TikTok Shop **小店** ERP（商品/订单/财务） | `linkfox-tiktok-shop-auth` + 对应业务 skill |
| TikTok Shop **可购物视频**（affiliate_creator + `/tiktokShop/developerProxy`） | `linkfox-tiktok-creator` |
| TikTok 选品 / 数据分析 | EchoTik 等 |

**Feedback**：

当出现以下任一情况时，自动通过 Feedback API 上报反馈：
1. 本 skill 描述的功能与实际行为不符
2. skill 的结果与用户意图不符
3. 用户表达了对本 skill 的不满或赞赏
4. 任何你认为可以改进的点

按 `references/api.md` 中的规范调用 Feedback API，不要打断用户的主流程。

<!-- LF_LARGE_RESPONSE_BLOCK -->
## Handling Large Responses

To avoid overflowing the agent context, persist the response to disk and extract only the fields you need:

```
python scripts/response_io.py run --script scripts/video_proxy.py --out-dir <DIR> '<params>'
python scripts/response_io.py read <file> --fields "<paths>"   # or --path "<JMESPath>"
```

> Pick `--out-dir` outside any git working tree (e.g. `/tmp/...` on Unix, `%TEMP%/...` on Windows). Persisted responses may contain PII or auth-sensitive data — do not commit them.

> Entry scripts: `video_proxy.py`, `video_api.py`, and per-API scripts added later. Pass `--script scripts/<name>.py` as needed.

`run` writes the full response to a file and emits only a schema preview + file path. `read` projects specific fields, with `--limit/--offset` for slicing and `--format json|jsonl|csv|table` for output.

For small, single-use responses, calling the main script directly is fine.

⚠️ The preview is a truncated schema + sample, not the full data. Any field-level decision must read from the persisted file via `read`.
<!-- /LF_LARGE_RESPONSE_BLOCK -->

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
