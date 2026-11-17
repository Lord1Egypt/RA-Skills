---
name: linkfox-echotik-get-video-download-url
description: 解析 TikTok 视频链接，返回无水印/含水印下载地址、播放地址与封面地址。
---

# EchoTik TikTok 视频下载地址查询

本技能用于把一个 TikTok 视频链接解析为可直接下载/播放的视频地址，帮助卖家保存带货视频素材或离线分析复用。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 把单个 TikTok 视频链接解析为：无水印下载地址（`noWatermarkDownloadUrl`）、含水印下载地址（`downloadUrl`）、播放地址（`playUrl`）与封面（静态 `coverUrl` / 动态 `dynamicCoverUrl`）。
- 支持两种链接格式：短链 `https://vt.tiktok.com/xxxxxx` 与完整链接 `https://www.tiktok.com/@user/video/1234567890`。
- 适用于归档高表现带货视频、复用创作者素材等场景。

### ❌ 边界与限制

- **必填参数**：必须提供 `url`，最大长度 1000。
- **下载地址不一定返回**：受区域、隐私或源站限制，部分视频不返回 `noWatermarkDownloadUrl` / `downloadUrl`，仅返回 `playUrl` 与封面；此时应改用 `playUrl` 播放预览，不要伪造下载链接。
- **链接时效**：返回的下载/播放地址会过期，应在解析后尽快使用；链接失效时需重新解析。
- **不在范围内**：按商品查询关联带货视频（用 `linkfox-echotik-product-video`，需 `productId`）；TikTok 商品搜索（用 `linkfox-echotik-product-search`）；TikTok 新品榜单（用 `linkfox-echotik-new-product-rank`）；TikTok 直播数据；视频剪辑或内容创作建议；非 TikTok 平台的视频下载。

## 核心概念

本工具接收单个 TikTok 视频链接，解析为直接媒体地址：无水印下载地址（推荐用于干净素材）、含水印下载地址、播放地址与封面（静态/动态）。当卖家想归档通过 EchoTik 商品视频工具发现的高表现带货视频，或复用创作者片段而无需重新录制时，本工具很有用。

**必填输入**：`url` 必填，支持两种格式：
- 短链：`https://vt.tiktok.com/xxxxxx`
- 完整链接：`https://www.tiktok.com/@user/video/1234567890`

**下载地址为条件返回**：并非所有视频都返回可下载地址。`noWatermarkDownloadUrl` 与 `downloadUrl` 仅在源视频允许时返回；部分视频（受区域/隐私/可用性限制）两者都缺省，仅返回 `playUrl` 与封面。呈现下载链接前务必检查字段是否存在，下载字段缺失时用 `playUrl` 播放兜底。

**地址时效**：返回的下载/播放地址会随时间失效，应在解析后尽快使用；链接失效时重新解析。

## 调用方式

- **API 端点**：`POST /echotik/getVideoDownloadUrl`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_get_video_download_url.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-get-video-download-url-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 解析完整 TikTok 视频链接**
```json
{
  "url": "https://www.tiktok.com/@user/video/1234567890"
}
```

**2. 解析 TikTok 短链**
```json
{
  "url": "https://vt.tiktok.com/Z123abc/"
}
```

## 展示规则

1. **优先呈现无水印链接**：`noWatermarkDownloadUrl` 存在时，作为首选下载选项呈现，因为干净素材通常是卖家想要的。
2. **同时提供含水印版本**：`downloadUrl`（含水印）存在时也列出，以备用户需要原版品牌。
3. **处理下载地址缺失**：`noWatermarkDownloadUrl` 与 `downloadUrl` 都缺失时（部分视频常见），不要伪造下载链接——告知用户该视频无直接下载地址，改用 `playUrl` 播放/预览。
4. **提供播放与封面**：说明 `playUrl` 可快速预览，`coverUrl` / `dynamicCoverUrl` 作为缩略图。
5. **时效提醒**：提醒用户解析的地址会过期，应尽快下载。
6. **只呈现数据**：清晰展示解析出的地址，不对视频如何使用做主观建议。
7. **错误处理**：解析失败时根据 `errcode`/`errmsg` 说明原因——`400` 表示 `url` 缺失或无效，`10000` 表示链接非有效/可访问的 TikTok 视频；建议检查 URL 格式。

## 用户表达与场景速查

**适用** —— TikTok 视频下载与素材保存：

| 用户说 | 场景 |
|--------|------|
| "下载这个 TikTok 视频"、"保存这个 TikTok 片段" | 把视频链接解析为下载地址 |
| "给我这个 TikTok 视频的无水印版本" | 优先返回 `noWatermarkDownloadUrl` |
| "我想保存这个达人的带货视频" | 解析并归档创作者视频 |
| "给我这个 TikTok 视频的可播放链接" | 返回 `playUrl` |
| "给我这个 TikTok 视频的封面/缩略图" | 返回 `coverUrl` / `dynamicCoverUrl` |

不适用场景见上方【能力边界】。

**边界判断**：当用户提到「TikTok 视频」时，判断其是否已有想下载的**具体视频链接**（本技能），还是想**发现某商品关联的视频**（商品视频技能）。若用户提供 `tiktok.com` 或 `vt.tiktok.com` 链接并要求保存/下载/提取，适用本技能；若其提供商品 ID 并问「这个商品有哪些带货视频」，则用 `linkfox-echotik-product-video`。

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

# EchoTik TikTok 视频下载 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/getVideoDownloadUrl`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | TikTok 视频地址，支持两种格式：`https://vt.tiktok.com/xxx` 短链或 `https://www.tiktok.com/@user/video/xxx` 完整链接。最大长度 1000 |

## 响应结构

成功时 HTTP 状态码为 200，响应体顶层同时包含业务码 `errcode=200`、`errmsg="ok"` 与下列数据字段。

| 字段 | 类型 | 是否必返 | 说明 |
|------|------|----------|------|
| noWatermarkDownloadUrl | string | 条件返回 | 视频下载地址（无水印）。**并非所有视频都返回**：部分视频该字段缺省，此时无法提供无水印下载 |
| downloadUrl | string | 条件返回 | 视频下载地址（含水印）。**并非所有视频都返回**：与无水印地址一同缺省或出现 |
| playUrl | string | 始终返回 | 视频播放地址。当下载地址缺省时，可作为播放/预览的兜底 |
| coverUrl | string | 始终返回 | 视频封面地址（静态） |
| dynamicCoverUrl | string | 始终返回 | 视频动态封面地址 |
| videoId | string | 始终返回 | 视频 ID |
| columns | array | 始终返回 | 渲染列定义（字段元数据：field/title/cellType/filterable/sortable，供前端表格渲染用） |
| type | string | 始终返回 | 渲染样式（如 `tableListWorkbenches`） |
| costToken | integer | 始终返回 | 消耗 token |
| errcode | integer | 始终返回 | 业务码，200 表示成功 |
| errmsg | string | 始终返回 | 业务信息，成功时为 `ok` |

> **下载地址缺省说明**：实测部分视频（受区域、隐私或源站限制）不会返回 `noWatermarkDownloadUrl` / `downloadUrl`，仅返回 `playUrl` 与封面。此时应向用户说明该视频暂无可直接下载地址，可改用 `playUrl` 播放预览。

成功响应示例（真实调用，已截断长 URL）：

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "videoId": "7096674515245206810",
  "noWatermarkDownloadUrl": "https://v45.tiktokcdn-eu.com/51678f6e0de3...",
  "downloadUrl": "https://v45.tiktokcdn-eu.com/626c5d3d5a7d...",
  "playUrl": "https://v45.tiktokcdn-eu.com/51678f6e0de3...",
  "coverUrl": "https://agent-files.linkfox.com/tiktok/20260629/7096674515245206810.jpg",
  "dynamicCoverUrl": "https://p16-common-sign.tiktokcdn-eu.com/tos-useast2a-p-0037...",
  "type": "tableListWorkbenches",
  "costToken": 12000,
  "columns": [/* 渲染列定义 */]
}
```

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 `errcode` 字段区分（`errcode = 200` 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数错误 | `errmsg` 会指明缺失项，如 `url 为必填参数`；检查 `url` 是否传入且非空 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 10000 | 未获取到视频下载地址 | URL 非 TikTok 视频链接、视频不可访问或已被删除；提示用户检查链接是否为有效的 TikTok 视频地址 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
// 参数缺失
{
    "errcode": 400,
    "errmsg": "url 为必填参数",
    "url": ""
}

// 非有效 TikTok 视频链接
{
    "errcode": 10000,
    "errmsg": "未获取到视频下载地址"
}

// 未授权
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/echotik/getVideoDownloadUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@user/video/1234567890"
  }'
```
