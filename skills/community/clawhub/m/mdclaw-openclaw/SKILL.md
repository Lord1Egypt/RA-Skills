---
name: MDClaw 多模态
description: MDClaw OpenClaw API 技能，支持文字转语音(TTS)、文生图(Text to Image)、文生视频(Text to Video)、图生视频(Image to Video)等多模态 AI 能力。通过网关服务统一调用，支持账号注册、图片上传、任务轮询等完整功能。
---

# MDClaw 多模态 技能

## 功能描述

通过 MDClaw OpenClaw API 网关访问多模态 AI 能力：

- **文字转语音 (TTS)** - 将文本转换为自然语音，支持多种音色
- **文生图 (Text to Image)** - 根据文字描述生成图片，支持多种宽高比和模型
- **文生视频 (Text to Video)** - 根据文字描述生成视频（异步任务）
- **图生视频 (Image to Video)** - 将图片转换为视频（异步任务）
- **图片上传** - 上传本地图片获取 URL，用于图生视频
- **全网搜索** - AI 驱动的全网搜索
- **天气查询 / 网页总结** - 实用辅助功能

## 认证方式

API Key 是主要认证方式，通过 `X-API-Key` 请求头传递。

**获取 API Key 的方式：**

```python
client = MDClawClient()
result = client.agent_register("用户名", "密码")
api_key = result["result"]["api_key"]
```

或设置环境变量：

```bash
export MDCLAW_API_KEY="你的API Key"
```

## API 参考

### 请求格式

```
POST https://backend.appmiaoda.com/projects/supabase287606411725160448/functions/v1/openclaw-skill-gateway

Headers:
  X-API-Key: 你的API Key
  Content-Type: application/json

Body:
  {"skill_id": "技能名称", "parameters": {...}}
```

### 技能列表

| 技能 | 参数 | 说明 |
|------|------|------|
| `text_to_speech` | text, model?, voice_id? | 文字转语音 |
| `text_to_image` | prompt, model?, aspect_ratio?, n? | 文生图 |
| `text_to_video` | prompt, model?, duration? | 文生视频（异步） |
| `image_to_video` | image, prompt?, model?, duration? | 图生视频（异步） |
| `video_status` | task_id | 查询视频任务状态 |
| `ai_search` | query | 全网搜索 |
| `weather_query` | city | 天气查询 |
| `web_summary` | url | 网页总结 |

### 视频生成说明

视频生成是异步操作：
1. 调用 `text_to_video` 或 `image_to_video` 获取 `task_id`
2. 用 `video_status(task_id)` 轮询状态
3. 状态流转: `Preparing` → `Queueing` → `Processing` → `Success` / `Fail`

**注意**: 不要传递 `resolution` 参数，否则 API 不返回 `task_id`。

## 使用示例

```python
from mdclaw_client import MDClawClient

# 初始化（从环境变量读取 API Key）
client = MDClawClient()

# 文字转语音
result = client.text_to_speech("你好，这是语音测试")
audio_url = result["result"]["audio_url"]

# 文生图
result = client.text_to_image("一只可爱的橘猫在阳光下伸懒腰", aspect_ratio="9:16")
image_url = result["result"]["image_urls"][0]

# 文生视频（异步）
result = client.text_to_video("一只金毛犬在公园快乐地奔跑", duration=6)
task_id = result["result"]["task_id"]

# 等待视频完成
video_result = client.wait_for_video(task_id)
video_url = video_result["result"]["url"]

# 上传图片并生成视频
upload = client.upload_image("local_image.jpg")
image_url = upload["result"]["url"]
result = client.image_to_video(image_url, "让画面动起来")
```

## 错误处理

```python
result = client.text_to_image("prompt")

if not result.get("success"):
    print(f"错误: {result.get('error')}")
```

## 依赖

```
requests>=2.31.0
```

---
**版本**: v2.0.0
**更新日期**: 2026-03-24
