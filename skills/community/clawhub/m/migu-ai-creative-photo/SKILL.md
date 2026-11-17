---
name: migu-ai-creative-photo
description: 使用咪咕旅游服务将用户照片与指定景点生成创意合影。适用于用户要上传人像、选择性别、输入景点名称并获取 AI 合成旅行照片；不用于普通图片导览或修图。
metadata:
  openclaw:
    display_name: "咪咕AI创意合影"
    emoji: "camera"
    priority: 82
    intents:
      - creative_photo
      - ai_photo
      - travel_photo
      - 创意合影
      - AI合影
      - 景点合影
---

# 咪咕AI创意合影

使用咪咕旅游同一产品的创意合影接口：上传照片，提交性别和景点名称，随后轮询生成结果。JWT 清洗、保存及诊断沿用 `migu-ai-guide` 的规则，但 token 值保存于本 skill 自己的 `secrets/plan_multi_token.txt`，不读取或写入其他 skill 的默认 token 文件。

## 对话流程

收集以下信息后才能提交生成：

1. 用户的本地照片，或服务端已上传照片的 URL。
2. 性别：询问“请选择男性或女性”。命令中传 `male` 或 `female`；默认映射为 `male=1`、`female=2`。若产品实际枚举调整，可传明确的 `--category 1` 或 `--category 2`。
3. 景点名称：询问“想和哪个景点合影？”。名称作为 `content` 原样发送，例如“北京故宫”。

本操作会把人像上传到 `https://gulangyu.migudm.cn` 并请求第三方生成合成照片。照片、性别、景点齐备后，在上传和生成前明确告知该外发行为并取得用户授权。用户未授权时，不上传、不生成，也不猜测结果。

## 运行

```powershell
cd C:\Users\ll\.openclaw\workspace\skills\migu-ai-creative-photo
node scripts\migu_ai_creative_photo_client.mjs `
  --image "C:\path\to\portrait.jpg" `
  --gender female `
  --scenic-name "北京故宫" `
  --json
```

已有上传后的图片地址时使用 `--image-url`。只提交生成任务可增加 `--generate-only --json`；稍后用 `--session-id "<sessionId>" --json` 查询。脚本每 3 秒查询一次，最长 180 秒；`status=1` 为生成中，`status=2` 为完成，返回 `photoUrls` 和 `tphotoUrls`。成功提交的 session ID 会写入 `creative_photo_session.txt`，只有传 `--resume` 时才复用。

## 接口约定

- 上传：`POST /trip-agent-api/v1/file/upload`，multipart 字段为 `file`，取 `data.filePath`。
- 生成：`POST /trip-agent-api/ai/creative/photo/generate`，请求体 `{ "fileUrl": "<filePath>", "category": 1|2, "content": "<景点名称>" }`。
- 查询：`GET /trip-agent-api/ai/creative/photo/query?sessionId=<sessionId>`。
- 请求头使用 `Authorization: Bearer <JWT>`、`X-APP-From: 10`、`X-App-Version: 0.6.0`、`Origin` 与 `Referer`。

## 安全

脚本始终对 `gulangyu.migudm.cn` 启用 TLS 证书校验（`rejectUnauthorized: true`），不提供任何关闭校验的开关。上传的人像、JWT 与返回结果不会被中间人拦截或篡改。若遇到证书错误，请检查系统证书与网络，而不是绕过校验。

## Token

默认 token 文件为：

```text
C:\Users\ll\.openclaw\workspace\skills\migu-ai-creative-photo\secrets\plan_multi_token.txt
```

支持 `--token-file`、`MIGU_AI_CREATIVE_PHOTO_TOKEN_FILE`、`MIGU_AI_CREATIVE_PHOTO_TOKEN`，并兼容显式覆盖的 `PLAN_MULTI_TOKEN_FILE` 与 `PLAN_MULTI_TOKEN`。保存用户提供的 JWT：

```powershell
$creativePhotoToken = "<JWT 或 Bearer JWT>"
$creativePhotoToken | node scripts\migu_ai_creative_photo_client.mjs --save-token-stdin
```

用 `node scripts\migu_ai_creative_photo_client.mjs --check-token --token-diagnostics` 检查 token。token 缺失、格式错误或过期时，不要编造生成结果。

## 输出

将 `photoUrls` 作为主成片链接提供给用户，`tphotoUrls` 是对应的附加结果链接。不要声称已生成、已保存或已下载服务未返回的图片。
