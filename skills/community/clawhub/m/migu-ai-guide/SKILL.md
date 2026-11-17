---
name: migu-ai-guide
display_name: "咪咕AI导览"
description: 咪咕AI导览助手。用户需要景点/城市/图片导览讲解、识别图片内容、根据上传图片生成中文讲解、或询问“介绍某地/讲解这张图/这是什么景点”时使用。通过咪咕旅游同产品的 guide_chat WebSocket 调用真实大模型；token 清洗、保存、诊断和 WebSocket 连接逻辑仿照 migu-trip-agent，但 token 文件保存在本 skill 自己的 secrets 目录中。
metadata:
  openclaw:
    emoji: "🧭"
    priority: 82
    intents:
      - ai_guide
      - guide_chat
      - scenic_guide
      - image_guide
      - 导览
      - 图片讲解
      - 景点讲解
      - 城市介绍
---

# 咪咕AI导览

## 核心能力

本 skill 调用咪咕旅游同产品的真实接口：

1. 文本导览：向 `guide_chat` WebSocket 发送问题，例如“介绍成都”“讲讲鼓浪屿”。
2. 图片导览：先上传本地图片到 `/trip-agent-api/v1/file/upload`，再把返回的 `filePath` 放入 `image_list` 发送给 `guide_chat`。
3. 会话复用：保存并复用 `guide_session.txt` 中的 `session_id`，支持连续追问。
4. token 逻辑复用：沿用原 `migu-trip-agent` 的 JWT 清洗、保存、诊断、WebSocket probe 逻辑；token 值默认保存在本 skill 的 `secrets/plan_multi_token.txt`。

## OpenClaw 使用原则

OpenClaw 里不要使用交互终端。每次用户请求都执行一次 `scripts/migu_ai_guide_client.mjs`。

进入目录：

```powershell
cd C:\Users\ll\.openclaw\workspace\skills\migu-ai-guide
```

文本导览：

```powershell
node scripts\migu_ai_guide_client.mjs `
  --question "介绍成都" `
  --session-file "$env:USERPROFILE\.openclaw\workspace\skills\migu-ai-guide\guide_session.txt" `
  --json
```

图片导览：

```powershell
node scripts\migu_ai_guide_client.mjs `
  --image "C:\path\to\photo.jpg" `
  --prompt "讲解图片中的内容" `
  --session-file "$env:USERPROFILE\.openclaw\workspace\skills\migu-ai-guide\guide_session.txt" `
  --json
```

如果用户直接给了线上图片地址，可跳过上传：

```powershell
node scripts\migu_ai_guide_client.mjs `
  --image-url "https://gulangyu.migudm.cn/trip-agent/mediaFile/img/c/c1aceca77c8550f55f15dbe580f92b2c.jpg" `
  --prompt "讲解图片中的内容" `
  --json
```

## 请求协议

上传图片：

- URL：`POST https://gulangyu.migudm.cn/trip-agent-api/v1/file/upload`
- Header：`Authorization: Bearer <JWT>`、`X-APP-From: 10`、`X-App-Version: 0.6.0`
- multipart 字段默认名：`file`
- 成功返回：`data.filePath`

WebSocket：

- URL：`wss://gulangyu.migudm.cn/trip-agent/ws/api/ws`
- 查询参数复用原 skill：`token`、`client_type=web`、`X-App-Version=0.6.4`、`tenant=hmxt`、`version=v0.6.4`
- 默认同时发送 `Authorization: Bearer <JWT>` 握手头。

文本请求体：

```json
{
  "header": {
    "task_type": "text_to_llm",
    "biz_type": "guide_chat",
    "session_id": "<session_id>"
  },
  "body": {
    "session_id": "<session_id>",
    "question": "介绍成都"
  }
}
```

图片请求体：

```json
{
  "header": {
    "task_type": "text_to_llm",
    "biz_type": "guide_chat",
    "session_id": "",
    "image_list": ["<上传返回的 filePath>"]
  },
  "body": {
    "session_id": "",
    "question": "",
    "prompt": "讲解图片中的内容",
    "title": "【图片】",
    "image_list": ["<上传返回的 filePath>"]
  }
}
```

大模型流式帧示例：

```json
{"status":"middle","content_type":"markdown","content":"眼前的","session_id":"8b450e43-9b47-49ce-927b-7d70e00ed250","category":"llm"}
```

脚本会拼接所有 `category=llm` 的 markdown 文本并输出。

## Token 配置

默认 token 路径固定在本 skill 内：

```text
C:\Users\ll\.openclaw\workspace\skills\migu-ai-guide\secrets\plan_multi_token.txt
```

也支持：

- `--token-file <path>`
- 环境变量 `MIGU_AI_GUIDE_TOKEN_FILE`
- 环境变量 `PLAN_MULTI_TOKEN_FILE`（兼容原 skill 的环境变量名，仅作为显式覆盖）
- 环境变量 `MIGU_AI_GUIDE_TOKEN`
- 环境变量 `PLAN_MULTI_TOKEN`（兼容原 skill 的环境变量名，仅作为显式覆盖）

保存用户私发 token：

```powershell
$userToken = "<用户私发的整行 JWT>"
$userToken | node scripts\migu_ai_guide_client.mjs --save-token-stdin
```

预检：

```powershell
node scripts\migu_ai_guide_client.mjs --check-token --probe-auth --token-diagnostics
```

如果 token 不存在，不要编造导览内容；请提示用户登录 https://gulangyu.migudm.cn/multi-city-trip-agent/ 后，在 Network 的 WebSocket `token=` 或 HTTP `Authorization: Bearer ...` 中复制整段 JWT 私发。

## 输出规范

对用户直接输出脚本返回的 `content`。如果 `--json` 返回里包含：

- `uploaded.filePath`：说明图片上传成功，可在内部记录，不必默认展示。
- `sessionId`：已写入 `guide_session.txt`，后续追问继续复用。
- `content`：导览正文，优先展示。

不要自行扩写接口没有返回的信息；可以做少量排版，但不要改变事实内容。
