# 曼格云视频号视频拆解 API 目录

平台 base url 固定 `https://api.we-media.cn`（写死在脚本里）。鉴权：所有接口 Header 加 `X-API-Key: <api_key>`。

> 接口路径、参数、响应字段均严格依据曼格云 API 接入说明文档，不臆造未给出的字段。

---

## 接口 33：视频号作品资料（核心元信息 + 媒体 + 互动）

**用途**：一次调用获取作品标题/文案、发布账号、发布时间、封面、时长、分辨率、文件大小、互动数据（点赞/推荐/转发/评论）及播放地址+解密密钥。此接口未提供独立收藏量和播放量。

- 方法：`POST`
- 地址：`/openapi/wechat-native-channel-info/videos/info`
- 计费：¥0.21/次（url 路线）

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| url | body | string | 与 shortUri 二选一 | 视频号分享链接 |
| shortUri | body | string | 与 url 二选一 | 视频号短 URI |

### 关键响应字段

| 字段路径 | 说明 |
| --- | --- |
| `data.title` | 作品标题或公开描述 |
| `data.description` | 作品公开描述（文案） |
| `data.accountName` | 发布账号名称 |
| `data.accountAvatarUrl` | 发布账号头像 URL |
| `data.publishedTimestamp` | 发布时间 Unix 秒 |
| `data.publishedAt` | 发布时间 UTC ISO-8601 |
| `data.coverUrl` | 作品封面 URL |
| `data.objectId` | 稳定作品 ID |
| `data.objectNonceId` | 作品配套 nonce ID |
| `data.media[0].playbackUrl` | 短期 CDN 媒体地址（需解密） |
| `data.media[0].decodeKey` | 十进制解码密钥（ISAAC64 XOR 前段） |
| `data.media[0].fileSize` | 媒体文件字节数 |
| `data.media[0].videoPlayLen` | 视频播放时长（秒）；`spec[].durationMs` 才是毫秒 |
| `data.media[0].width` | 媒体宽度像素 |
| `data.media[0].height` | 媒体高度像素 |
| `data.metrics.likeCount` | 历史命名：实际为推荐数；报告规范化为 `recommendCount` |
| `data.metrics.commentCount` | 精确评论数 |
| `data.metrics.favoriteCount` | 历史命名：来自 Finder `favCount`，实际为心形点赞数；报告规范化为 `likeCount`，不是收藏 |
| `data.metrics.shareCount` | 精确转发/分享数 |
| `data.metrics.viewCount` | 本接口未提供，缺失不得补 0 或计算互动率 |
| `data.commentCount` | 作品评论数 |
| `balance` | 扣费后账户余额（元） |
| `consumption` | 本次实际消费（元） |

> `playbackUrl` 是短期 CDN 地址，不是可持久化的 MP4。当存在 `decodeKey` 时，前 128 KiB 需用 ISAAC64 流按字节 XOR 解密，并校验解密结果包含 MP4 的 `ftyp` 标识。

### 互动字段兼容口径（1.3.1）

上述映射只适用于本 Skill 调用的作品资料接口旧字段，不能套用到评论的点赞数或其它平台。`scripts/interaction_metrics.py` 集中规范化数据和 `metricDetails`，以 `wechat-channels-interactions-v2` 标记，已标记的数据不再交换。原始 `info` 保留接口响应字段；AI 与报告共同使用 `wm_interaction_facts.json`，其中 `likeCount`=点赞、`recommendCount`=推荐。

`metricDetails.exact=false` 或非 `exact` 关系、缩写值、无效/缺失值不作为精确数字参与合计或比值。推荐不等于收藏，没有独立收藏字段时不输出收藏指标或推导留存需求。

核对依据（2026-10-19）：微信官方网页 `https://channels.weixin.qq.com/web/pages/home` 的 `virtual_svg-icons-register.publishJiuw8DRXAy.js` 中 `toggleLikeFeed` 更新 `likeCount` 和好友推荐列表，`toggleFavFeed` 更新 `favCount`；`like.publishBwHsEJv4rY.js` 将 `account_like` 标为“推荐”、`account_fav` 标为“喜欢”、`account_global_fav` 单独标为“收藏”。脚本位置在 `https://res.wx.qq.com/t/wx_fed/finder/web/web-finder/res/js/`，文件名可能随微信发布变化。

---

## 临时文件上传（免费基础设施）

**用途**：把本机已解密的视频或本地视频文件直传到平台临时对象存储，换取公网 HTTPS 临时地址供 AI 接口使用。

### 第一步：申请票据

- 方法：`POST`
- 地址：`/api/v1/file-uploads/ticket`
- 认证：`X-API-Key`
- 请求体：

```json
{ "filename": "video.mp4", "bytes": 12345678, "contentType": "video/mp4" }
```

- 响应：

| 字段 | 说明 |
| --- | --- |
| `data.requiredFields` | multipart 表单字段（逐项作为表单字段提交） |
| `data.uploadUrl` | 直传目标地址（对象存储预签名 URL） |
| `data.fileUrl` | 上传成功后可用的公网 HTTPS 临时文件地址 |

### 第二步：直传

把 `data.requiredFields` 逐项作为 multipart 字段，本地文件字段名设为 `file`，直接 POST 到 `data.uploadUrl`。不要把文件流 POST 到网关。

### 第三步：使用

上传成功后，将 `data.fileUrl` 传给接口 27 的 `videoUrl` 参数。文件最多 128MB，票据有效期 2 小时，文件约 2 小时后自动清理。申请票据不计费。

---

## 接口 27：视频视觉理解（深度拆解）

**用途**：通过多模态大模型分析并深入理解视频画面，返回内容摘要、时间线分段、镜头/运镜/转场/情绪线索、画面事实与不确定项。

- 方法：`POST`
- 地址：`/openapi/stepfun-video-understanding/analyze`
- 计费：summary ¥0.12 / timeline ¥0.18 / decompose ¥0.24

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| videoUrl | body | string | 是 | 公网 HTTPS MP4 地址或 `stepfile://` 引用 |
| analysisMode | body | string | 否 | `summary`/`timeline`/`decompose`，默认 `timeline` |
| extraPrompt | body | string | 否 | 用户附加分析要求，最多 4000 字符 |

### 关键响应字段

| 字段路径 | 说明 |
| --- | --- |
| `data.analysisMode` | 实际执行的分析档位 |
| `data.model` | 实际使用的阶跃模型 |
| `data.observation.summary` | 仅基于可观察视频证据的内容摘要 |
| `data.observation.durationSeconds` | 模型估计的视频时长 |
| `data.observation.segments` | 带起止秒、画面、屏幕文字、语音摘要、镜头信息与置信度的结构化片段 |
| `data.observation.visualFacts` | 带时间证据和置信度的可核验画面事实 |
| `data.observation.uncertainties` | 无法从视频确认的内容 |
| `data.usage.inputTokens` | 输入 Token 用量 |
| `data.usage.outputTokens` | 输出 Token 用量 |
| `data.usage.totalTokens` | 总 Token 用量 |
| `balance` | 扣费后余额 |
| `consumption` | 本次消费 |

---

## 接口 13：账户余额查询（免费）

- 方法：`GET`
- 地址：`/openapi/account-balance/`
- 计费：¥0.00

### 响应

| 字段 | 说明 |
| --- | --- |
| `data.balance` | 当前账户可用余额（元） |
| `data.currency` | 余额币种，固定 CNY |

---

## 本机解密规则

1. 只接受 HTTPS 的 `finder.video.qq.com` 播放地址。
2. 下载到随机临时目录，文件必须小于 128 MiB。
3. 用十进制 `decodeKey` 创建 ISAAC64 状态，生成 131072 字节（128 KiB）密钥流：按 `seed[255]` 到 `seed[0]` 取值，以大端序写出每个 64 位字，再与前 128 KiB XOR。所有中间值按无符号 64 位溢出。
4. 回归向量：`decodeKey=1233185028`、全零输入时密钥流前 64 字节为 `59cd728cbf3e0f6c525f36b3079a51cd606cd7f9af2b30dccf6decbccc7563fa14ffc4254d415520fc6bf0c68bb14b086b34d0cab535aa463c05a027ba8e7770`。
5. 解密后第 4 至第 8 字节必须是 ASCII `ftyp`。校验失败立即删除临时文件并停止。
6. 后续字节不处理；视觉调用结束后删除本机临时目录。

---

## 通用约定

- 成功响应为统一结构：`requestId`、`code`、`data`；客户计费响应还包含 `balance` 和 `consumption`。
- 网关成功响应 `code` 通常为 `OK`。
- 普通请求不需要 `Idempotency-Key`；只有客户端自行重试同一非 GET 请求时才复用同一值避免重复扣费。
- 不要向终端用户暴露平台内部服务、内部路由或实现细节。
