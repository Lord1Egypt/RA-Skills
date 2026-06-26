---
name: IMA Studio Text-to-Speech
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, tts, text-to-speech, speech synthesis, voice, 语音合成, 文字转语音, seed-tts
argument-hint: "[text to speak]"
description: >
  Complete API documentation for IMA TTS Generator. Includes detailed model parameters,
  speaker list, error handling, UX protocol, and Python examples.
---

# IMA TTS AI — Complete Documentation

## Supported Models

| Name | model_id | Sub-models | Notes |
|------|----------|------------|-------|
| **Seed TTS 2.0** | `seed-tts-2.0` | expressive, standard | Only supported model |

**Sub-model selection via `extra-params`:**
- `seed-tts-2.0-expressive` — More expressive, emotional (default)
- `seed-tts-2.0-standard` — More stable, neutral

---

## Estimated Generation Time

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|---------------|------------|---------------------|
| **seed-tts-2.0** | 5~30s | 3s | 10s |

---

## 💬 User Experience Protocol (IM / Feishu / Discord)

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_tts_create.py` / 脚本 / script | — |
| attribute_id / model_version / form_config | — |
| API 调用 / HTTP 请求 / 任何技术参数名 | — |

Only tell users: **model name · estimated time · credits · result (audio/media) · plain-language status**.

### UX Flow

1. **Step 0 — Acknowledgment:** "好的，正在帮你把这段文字转成语音。"
2. **Step 1 — Pre-generation:** "🔊 开始语音合成，请稍候… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
3. **Step 2 — Progress:** Every 10-15s: "⏳ 语音合成中… [P]%"
4. **Step 3 — Success:** Send audio via `media=audio_url` + caption with link
5. **Step 4 — Failure:** Natural language error + suggestions

---

## ⚠️ Error Message Translation

**NEVER show technical error messages to users.**

| Technical Error | ✅ Say Instead (Chinese) | ✅ Say Instead (English) |
|----------------|------------------------|------------------------|
| `401 Unauthorized` | ❌ 密钥无效或未授权<br>💡 **生成新密钥**: https://www.imaclaw.ai/imaclaw/apikey | ❌ API key invalid<br>💡 **Generate at**: imaclaw.ai |
| `4008 Insufficient points` | ❌ 积分不足<br>💡 **购买积分**: https://www.imaclaw.ai/imaclaw/subscription | ❌ Insufficient points<br>💡 **Buy at**: imaclaw.ai |
| `Invalid product attribute` | 参数配置异常，请稍后重试 | Configuration error, try again |
| `Error 6006 / 6010` | 积分或参数不匹配，请重试 | Points/params mismatch |
| `resource_status == 2` | 合成失败，建议缩短文本重试 | Synthesis failed, try shorter text |
| `timeout` | 合成超时，请稍后重试 | Timed out, try again |

---

## 🎤 当用户说「帮我制作旁白/配音」时如何询问

### 必问

| 询问项 | 对应参数 | 说明 |
|--------|----------|------|
| **要朗读的内容 / 旁白文案** | `prompt` | 合成文本，必填 |

### 建议问（让用户选择）

| 询问项 | 对应参数 | 选项来源与示例 |
|--------|----------|----------------|
| **音色 / 发音人** | `speaker` | 从 `volcengine_tts_timbre_list.json` 按场景推荐 |

### 可选问（按需补充）

| 询问项 | 对应参数 | 说明与取值 |
|--------|----------|------------|
| **情感 / 情绪** | `audio_params.emotion` | neutral、sad、angry |
| **语速** | `audio_params.speech_rate` | 范围 [-50, 100]，0 为正常 |
| **音量** | `audio_params.loudness_rate` | 范围 [-50, 100]，0 为正常 |
| **模型风格** | `model` | expressive（默认）或 standard |

---

## 🎙️ Speaker / 音色列表

### 通用场景

| 音色名称 | speaker ID | 性别 | 场景 |
|----------|------------|------|------|
| 魅力苏菲 | `zh_male_sophie_uranus_bigtts` | 男 | 通用 |
| Vivi | `zh_female_vv_uranus_bigtts` | 女 | 通用 |
| 云舟 | `zh_male_m191_uranus_bigtts` | 男 | 通用 |

### 视频配音

| 音色名称 | speaker ID | 性别 | 场景 |
|----------|------------|------|------|
| 大壹 | `zh_male_dayi_uranus_bigtts` | 男 | 视频配音 |
| 猴哥 | `zh_male_sunwukong_uranus_bigtts` | 男 | 角色配音 |

### 角色扮演

| 音色名称 | speaker ID | 性别 | 场景 |
|----------|------------|------|------|
| 知性灿灿 | `zh_female_cancan_uranus_bigtts` | 女 | 知性 |
| 撒娇学妹 | `zh_female_sajiaoxuemei_uranus_bigtts` | 女 | 可爱 |

**完整音色列表:** 见项目内 `volcengine_tts_timbre_list.json`

**⚠️ 重要:** 使用原生格式（`*_uranus_bigtts`），不支持 `BV*_streaming` 格式。

---

## 🌐 Network Endpoints

| Domain | Purpose | What's Sent |
|--------|---------|-------------|
| `api.imastudio.com` | Main API | Prompts, model params, task IDs |

This skill does **NOT** use image upload domains.

---

## seed-tts-2.0 — Verified Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | ✅ | Text to speak |
| `n` | int | ✅ | Usually 1 |
| `model` | string | ✅ | `seed-tts-2.0-expressive` or `seed-tts-2.0-standard` |
| `speaker` | string | optional | Speaker ID, e.g. `zh_male_sophie_uranus_bigtts` |
| `audio_params` | object | optional | `emotion`, `speech_rate`, `loudness_rate` |
| `additions` | object | optional | e.g. `{"explicit_language": "crosslingual"}` |
| `cast` | object | ✅ | `{"points": <credit>, "attribute_id": <id>}` |

---

## API Reference

### Core Flow

```
1. GET /open/v1/product/list?app=ima&platform=web&category=text_to_speech
   → Get attribute_id, credit, model_version

2. POST /open/v1/tasks/create
   → task_type: "text_to_speech", parameters[].parameters.prompt = text

3. POST /open/v1/tasks/detail  { "task_id": "..." }
   → Poll every 2-5s until medias[].resource_status == 1
```

### API 2: Create Task

```json
{
  "task_type": "text_to_speech",
  "enable_multi_model": false,
  "src_img_url": [],
  "parameters": [{
    "attribute_id": "<from credit_rules>",
    "model_id": "seed-tts-2.0",
    "model_name": "Seed TTS 2.0",
    "model_version": "<version_id>",
    "app": "ima",
    "platform": "web",
    "category": "text_to_speech",
    "credit": "<points>",
    "parameters": {
      "prompt": "Text to be spoken.",
      "n": 1,
      "input_images": [],
      "model": "seed-tts-2.0-expressive",
      "speaker": "zh_male_sophie_uranus_bigtts",
      "audio_params": {"emotion": "neutral"},
      "cast": {"points": "<points>", "attribute_id": "<attribute_id>"}
    }
  }]
}
```

### Task Detail Response

| Field | Type | Meaning |
|-------|------|---------|
| `resource_status` | int/null | 0=处理中, 1=可用, 2=失败, 3=已删除 |
| `status` | string | "pending" / "processing" / "success" / "failed" |
| `url` | string | Audio URL when resource_status=1 |
| `duration_str` | string | Optional, e.g. "30s" |
| `format` | string | Optional, e.g. "mp3", "wav" |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| prompt at top level | Put inside `parameters[].parameters` |
| Wrong attribute_id | Always call product list first |
| Using `BV*_streaming` speaker format | Use `*_uranus_bigtts` format |
| Single poll | Poll until resource_status == 1 |

---

## Python Example

```python
import time, requests

BASE = "https://api.imastudio.com"
HEADERS = {
    "Authorization": "Bearer ima_your_key",
    "Content-Type": "application/json",
    "x-app-source": "ima_skills",
}

# 1. Product list
r = requests.get(
    f"{BASE}/open/v1/product/list",
    headers=HEADERS,
    params={"app": "ima", "platform": "web", "category": "text_to_speech"},
)
tree = r.json()["data"]
# ... find type=3 node, get attribute_id, model_id, model_version, credit ...

# 2. Create task
body = {
    "task_type": "text_to_speech",
    "enable_multi_model": False,
    "src_img_url": [],
    "parameters": [{
        "attribute_id": attribute_id,
        "model_id": "seed-tts-2.0",
        "model_name": "Seed TTS 2.0",
        "model_version": model_version,
        "app": "ima", "platform": "web",
        "category": "text_to_speech",
        "credit": credit,
        "parameters": {
            "prompt": "Hello, world.",
            "n": 1,
            "input_images": [],
            "model": "seed-tts-2.0-expressive",
            "speaker": "zh_male_sophie_uranus_bigtts",
            "cast": {"points": credit, "attribute_id": attribute_id},
        },
    }],
}
r = requests.post(f"{BASE}/open/v1/tasks/create", headers=HEADERS, json=body)
task_id = r.json()["data"]["id"]

# 3. Poll
while True:
    r = requests.post(f"{BASE}/open/v1/tasks/detail", headers=HEADERS, json={"task_id": task_id})
    task = r.json()["data"]
    medias = task.get("medias") or []
    if not medias:
        time.sleep(3)
        continue
    rs = medias[0].get("resource_status") or 0
    if rs == 2 or medias[0].get("status") == "failed":
        raise RuntimeError("failed")
    if rs == 1 and medias[0].get("url"):
        print(medias[0]["url"])
        break
    time.sleep(3)
```

---

## User Preference Memory

Storage: `~/.openclaw/memory/ima_prefs.json`

```json
{
  "user_{user_id}": {
    "text_to_speech": {
      "model_id": "seed-tts-2.0",
      "speaker": "zh_male_sophie_uranus_bigtts",
      "last_used": "..."
    }
  }
}
```

- **Save** when user explicitly says "用XXX音色" / "默认用XXX"
- **Clear** when user says "换个音色" / "推荐一个"
