---
name: lumi-api
description: "Use this skill when the user wants to manage social media content via Lumi — uploading videos, publishing to TikTok/YouTube/Instagram, translating or dubbing content, checking account analytics, listing connected accounts, or managing localization tasks. All API calls use curl with Bearer token authentication."
metadata:
  {
    "openclaw":
      {
        "homepage": "https://lumipath.cn",
        "requires": { "env": ["LUMI_API_KEY"] },
        "primaryEnv": "LUMI_API_KEY",
      },
  }
---

# 权限声明
# SECURITY MANIFEST:
# - Allowed to read: {baseDir}/README.md, {baseDir}/references/*.json
# - Allowed to make network requests to: https://lumipath.cn


## 通用工作流

当用户提出请求时，请严格执行以下步骤：

1. **检查API密钥**：首先检查环境变量 `LUMI_API_KEY` 是否存在。如果不存在，提示用户设置：`export LUMI_API_KEY="lumi_your_key_here"`
2. **阅读README**：仔细阅读 `{baseDir}/README.md`，了解接口概览和认证方式。
3. **目录索引**：扫描 `{baseDir}/references/` 目录下的所有文件名，确定哪些 OpenAPI 定义文件与用户需求相关。
4. **精准读取**：仅读取选定的 `.json` 文件，分析其 `paths`、`parameters` 和 `requestBody`。
5. **收集参数**（见下方各场景的参数清单），向用户确认所有必要参数后再执行。
6. **构造请求**：使用 curl 执行请求。
   - **Base URL**: `https://lumipath.cn`
   - **Auth**: `Authorization: Bearer $LUMI_API_KEY`


---

## 场景一：搬运视频（repurpose）

**触发条件**：用户提供抖音/B站/小红书链接，或说"搬运"、"复用"、"翻译发布"。

### 第一步：收集参数（在执行任何 API 调用前，必须向用户确认以下所有信息）

| 参数 | 是否必须 | 说明 |
|------|---------|------|
| 视频链接 | ✅ 必须 | 抖音/B站/小红书/xhslink URL |
| 原始语言 | ✅ 必须 | 视频的语言，如 zh、en、ja |
| 目标语言 | ✅ 必须 | 要翻译成的语言，如 en、ko、ja、es |
| 是否配音 | ✅ 必须 | 是否用 AI 声音替换原声（dubbing） |
| 配音声音 | 配音时必须 | 引导用户访问 [lumipath.cn/voices](https://lumipath.cn/voices) 查看和试听声音后选择 |
| 是否加字幕 | ✅ 必须 | 是否在视频中烧录翻译字幕（subtitle） |
| 发布到哪些平台 | ✅ 必须 | TikTok / YouTube / Instagram，可多选 |
| 发布文案 | ✅ 必须 | 发布时的标题或 caption |
| YouTube 标题 | 发布到 YouTube 时必须 | YouTube 视频标题 |
| YouTube 可见性 | 发布到 YouTube 时必须 | public / private / unlisted |
| TikTok 隐私设置 | 可选 | 默认 PUBLIC_TO_EVERYONE |

> **autoPublish 默认启用**：搬运场景中，只要用户指定了发布平台，必须始终设置 `autoPublish` 字段，无需额外询问用户是否自动发布。

> **禁止跳过参数收集步骤直接发起请求。** 如果用户没有提供某个必要参数，必须主动询问。

### 第二步：获取账号连接 ID

调用 `GET /api/v1/connections` 获取目标平台的 `connectionId`，展示给用户确认使用哪个账号。

### 第三步：获取 TTS 声音列表（如需配音）

引导用户访问 **https://lumipath.cn/voices** 查看所有可用声音（支持试听）。用户选定声音名称后，调用 `GET /api/v1/tts?language=<目标语言>` 匹配对应的 `id`。

### 第四步：发起搬运任务

调用 `POST /api/v1/repurpose`，将发布信息通过 `autoPublish` 字段一并传入，确保翻译完成后自动发布。

```
autoPublish: {
  text: "<用户提供的发布文案>",
  tiktokConnectionIds: [...],   // 如选择了 TikTok
  youtubeConnectionIds: [...],  // 如选择了 YouTube
  instagramConnectionIds: [...] // 如选择了 Instagram
}
```

### 第五步：轮询任务进度

每隔 15 秒调用一次 `GET /api/v1/localization?taskId=<taskId>`，向用户展示当前进度（`step` 和 `progress`），直到 `status=completed` 或 `status=failed`。

### 第六步：完成确认

- `status=completed`：告知用户任务已完成，已自动发布到指定平台。
- `status=failed`：展示 `failureReason`，建议用户重试。

---

## 场景二：直接发布视频（social post）

**触发条件**：用户提供视频 URL 或已有视频，要直接发布，不需要翻译。

### 参数收集

| 参数 | 是否必须 | 说明 |
|------|---------|------|
| 视频来源 | ✅ 必须 | 公开 URL 或已在库中的视频 |
| 发布平台 | ✅ 必须 | TikTok / YouTube / Instagram |
| 发布文案 | ✅ 必须 | Caption 或描述 |
| YouTube 标题 | 发布到 YouTube 时必须 | |
| YouTube 可见性 | 发布到 YouTube 时必须 | public / private / unlisted |
| TikTok 隐私 | 可选 | 默认 PUBLIC_TO_EVERYONE |

### 执行步骤

1. 如果是新视频 URL，先调用 `POST /api/v1/videos/upload` 上传，获取 OSS `url`
2. 调用 `GET /api/v1/connections` 获取目标平台的 `connectionId`
3. 调用 `POST /api/v1/social-posts` 发布

---

## 场景三：仅本地化（不发布）

**触发条件**：用户只想翻译/配音/加字幕，暂不发布。

### 参数收集

同场景一，但不询问发布平台，不设置 `autoPublish`。

完成后展示 `outputUrl`，告知用户可随时用此链接手动发布。

---

## 注意事项

- **禁止全量加载**：除非涉及多个领域，否则禁止同时读取多个 JSON 文件。
- **参数完整性**：**绝对禁止**在用户未确认目标语言、发布平台、发布文案的情况下启动 repurpose 或 localization 任务。
- **账号确认**：当用户有多个同平台账号时，必须列出所有账号让用户选择，不得自动选第一个。
- **轮询**：任务启动后必须持续轮询并向用户报告进度，不得静默等待。
- **错误处理**：请求失败时展示友好提示和详细错误信息。
