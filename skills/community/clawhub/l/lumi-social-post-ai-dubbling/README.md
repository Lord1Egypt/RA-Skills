# Lumi API — 使用说明

Lumi 是一个多平台社交媒体内容管理工具，支持视频上传、多平台发布、AI 配音/翻译本地化、数据分析等功能。

## 认证

所有接口均需在 Header 中传入 Bearer Token：

```
Authorization: Bearer <LUMI_API_KEY>
```

API Key 格式：`lumi_xxxxxxxxxxxx`，可在 Lumi 控制台生成。

**Base URL**: `https://lumipath.cn`

---

## 接口概览

| 分类 | 文件 | 接口数 | 说明 |
|------|------|--------|------|
| 已连接账号 | connections.openapi.json | 1 | 列出已绑定的社交账号 |
| 视频库 | videos.openapi.json | 3 | 上传视频、从中文平台导入、列出库存 |
| 社交发布 | social-posts.openapi.json | 1 | 发布视频到 TikTok/YouTube/Instagram |
| 本地化 | localization.openapi.json | 2 | 启动/查询翻译配音任务 |
| TTS 声音 | tts.openapi.json | 1 | 列出可用配音声音 |
| 一键复用 | repurpose.openapi.json | 1 | 爬取中文平台视频并翻译发布 |
| 数据洞察 | insights.openapi.json | 1 | 获取账号粉丝/播放量等指标 |

---

## 快速入门

### 1. 设置环境变量
```bash
export LUMI_API_KEY="lumi_your_key_here"
export LUMI_BASE_URL="https://lumipath.cn"
```

### 2. 验证连通性
```bash
curl -s "$LUMI_BASE_URL/api/v1/connections" \
  -H "Authorization: Bearer $LUMI_API_KEY"
```

---

## 典型工作流

### 工作流 A：上传视频并发布到 TikTok
1. `POST /api/v1/videos/upload` — 上传视频，获取 `url`
2. `GET /api/v1/connections?platform=tiktok` — 获取 `connectionId`
3. `POST /api/v1/social-posts` — 发布，传入 `mediaUrls` 和 `tiktokConnectionIds`

### 工作流 B：一键复用抖音/B站视频到英文 TikTok
1. `POST /api/v1/repurpose` — 传入抖音 URL、sourceLang、targetLang、autoPublish
2. `GET /api/v1/localization?taskId=...` — 轮询直到 `status=completed`
3. 如未设置 autoPublish，手动用 `outputUrl` 调用 `POST /api/v1/social-posts`

### 工作流 C：视频本地化（翻译+配音+字幕）
1. `GET /api/v1/tts?language=en` — 选择合适的配音声音，记录 `id`
2. `GET /api/v1/videos` — 找到目标视频的 `vid` 和 OSS URL
3. `POST /api/v1/localization` — 启动任务，传入 `vid`、`sourceUrl`、`dubbingVoiceId`
4. `GET /api/v1/localization?taskId=...` — 轮询状态，完成后获取 `outputUrl`

### 工作流 D：查看账号数据分析
1. `GET /api/v1/connections` — 获取所有 `connectionId`
2. 对每个账号调用 `GET /api/v1/insights?connectionId=...`

---

## 认证说明

- API Key 通过 MongoDB `api_keys` 集合验证，有 7 天 Redis 缓存
- 格式必须为 `Bearer lumi_xxxx`，不带 `Bearer` 前缀会返回 401
- 支持的平台：TikTok、YouTube、Instagram（发布）；Facebook、X、Reddit（仅连接查看）

---

## 错误码

| HTTP 状态码 | 含义 |
|------------|------|
| 401 | API Key 无效或缺失 |
| 400 | 参数校验失败 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 枚举值参考

### 社交平台（发布用）
`TIKTOK` | `YOUTUBE` | `INSTAGRAM`

### 社交平台（连接查询用）
`tiktok` | `youtube` | `instagram` | `facebook` | `x` | `reddit`

### TikTok 隐私设置
`PUBLIC_TO_EVERYONE` | `MUTUAL_FOLLOW_FRIENDS` | `FOLLOWER_OF_CREATOR` | `SELF_ONLY`

### YouTube 可见性
`public` | `private` | `unlisted`

### 视频状态
`uploaded` | `translating` | `translated` | `published` | `failed` | `scheduled`

### 本地化任务状态
`pending` | `running` | `completed` | `failed`

### backgroundMusic 参数
`0` = 保留原始音乐 | `1` = 静音 | `2` = 仅保留音效

### TTS 性别
`female` | `male`
