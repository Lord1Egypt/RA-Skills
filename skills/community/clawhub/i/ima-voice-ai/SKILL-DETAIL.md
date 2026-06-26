---
name: IMA Studio Music Generation
version: 1.2.2
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, ai music, text_to_music, music generation, Suno, DouBao, GenBGM, GenSong, AI作曲, 音乐生成
argument-hint: "[music description or style]"
description: >
  Complete API documentation for IMA Music Generator. Includes detailed model parameters,
  attribute_id references, error handling, UX protocol, and Python examples.
---

# IMA Voice AI — Complete Documentation

## Supported Models

| Name | model_id | Description | Best For |
|------|----------|-------------|----------|
| **Suno** | `sonic` | Full songs with vocals, multiple genres | General music, songs |
| **DouBao BGM** | `GenBGM` | Instrumental background music | BGM, podcasts, videos |
| **DouBao Song** | `GenSong` | Songs with vocals (Chinese focus) | Chinese songs |

---

## Estimated Generation Time per Model

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|---------------|------------|---------------------|
| **Suno (sonic)** | 60~180s | 5s | 30s |
| **DouBao BGM (GenBGM)** | 30~90s | 5s | 20s |
| **DouBao Song (GenSong)** | 60~120s | 5s | 25s |

---

## 💬 User Experience Protocol (IM / Feishu / Discord)

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_voice_create.py` / 脚本 / script | — |
| attribute_id / model_version / form_config | — |
| API 调用 / HTTP 请求 / 任何技术参数名 | — |

Only tell users: **model name · estimated time · credits · result (audio/media) · plain-language status**.

### UX Flow

1. **Pre-generation:** "🎵 开始生成音乐… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
2. **Progress:** Every 30-60s: "⏳ 正在生成中… [P]%" (cap at 95%)
3. **Success:** Send audio via `media=audio_url` + caption with link
4. **Failure:** Natural language error + suggest alternatives

---

## ⚠️ Error Message Translation

**NEVER show technical error messages to users.**

| Technical Error | ✅ Say Instead (Chinese) | ✅ Say Instead (English) |
|----------------|------------------------|------------------------|
| `401 Unauthorized` | ❌ API密钥无效或未授权<br>💡 **生成新密钥**: https://www.imaclaw.ai/imaclaw/apikey | ❌ API key is invalid<br>💡 **Generate API Key**: https://www.imaclaw.ai/imaclaw/apikey |
| `4008 Insufficient points` | ❌ 积分不足<br>💡 **购买积分**: https://www.imaclaw.ai/imaclaw/subscription | ❌ Insufficient points<br>💡 **Buy Credits**: https://www.imaclaw.ai/imaclaw/subscription |
| `Error 6006` | 积分计算异常，系统正在修复 | Points calculation error |
| `Error 6010` | 模型参数不匹配，请尝试其他模型 | Model parameters incompatible |
| `timeout` | 生成时间过长已超时，建议用更快的模型 | Generation took too long |

**Failure fallback table:**

| Failed Model | First Alt | Second Alt |
|-------------|-----------|------------|
| sonic (Suno) | GenBGM | GenSong |
| GenBGM | sonic | GenSong |
| GenSong | sonic | GenBGM |

---

## 🌐 Network Endpoints

| Domain | Purpose | What's Sent |
|--------|---------|-------------|
| `api.imastudio.com` | Main API | Prompts, model params, task IDs |

This skill does **NOT** use secondary upload domains.

---

## API Reference

### Core Flow

```
1. GET /open/v1/product/list?app=ima&platform=web&category=text_to_music
   → Get attribute_id, credit, model_version

2. POST /open/v1/tasks/create
   → task_type: "text_to_music", parameters[].parameters.prompt = music description

3. POST /open/v1/tasks/detail  { "task_id": "..." }
   → Poll every 5s until medias[].resource_status == 1
```

### API 1: Product List

```
GET /open/v1/product/list?app=ima&platform=web&category=text_to_music
```

### API 2: Create Task

```json
{
  "task_type": "text_to_music",
  "enable_multi_model": false,
  "src_img_url": [],
  "parameters": [{
    "attribute_id": "<from credit_rules>",
    "model_id": "sonic",
    "model_name": "Suno",
    "model_version": "<version_id>",
    "app": "ima",
    "platform": "web",
    "category": "text_to_music",
    "credit": "<points>",
    "parameters": {
      "prompt": "upbeat lo-fi hip hop, 90 BPM",
      "n": 1,
      "input_images": [],
      "cast": {"points": "<points>", "attribute_id": "<attribute_id>"}
    }
  }]
}
```

### API 3: Task Detail (Poll)

```
POST /open/v1/tasks/detail
{"task_id": "<id>"}
```

| resource_status | status | Action |
|-----------------|--------|--------|
| 0 or null | pending/processing | Keep polling |
| 1 | success | Done, read `url` |
| 2/3 | any | Failed |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `attribute_id` is 0 or missing | Always query product list first |
| `prompt` at outer level | Must be inside `parameters[].parameters` |
| Wrong `credit` value | Must match `credit_rules[].points` |

---

## Python Example

```python
import time, requests

BASE_URL = "https://api.imastudio.com"
API_KEY = "ima_your_key_here"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "x-app-source": "ima_skills",
    "x_app_language": "en",
}

def get_products(category):
    r = requests.get(f"{BASE_URL}/open/v1/product/list",
                     headers=HEADERS,
                     params={"app": "ima", "platform": "web", "category": category})
    r.raise_for_status()
    versions = []
    for node in r.json()["data"]:
        for child in node.get("children") or []:
            if child.get("type") == "3":
                versions.append(child)
    return versions

def create_task(prompt, product):
    rule = product["credit_rules"][0]
    body = {
        "task_type": "text_to_music",
        "enable_multi_model": False,
        "src_img_url": [],
        "parameters": [{
            "attribute_id": rule["attribute_id"],
            "model_id": product["model_id"],
            "model_name": product["name"],
            "model_version": product["id"],
            "app": "ima", "platform": "web",
            "category": "text_to_music",
            "credit": rule["points"],
            "parameters": {
                "prompt": prompt, "n": 1,
                "input_images": [],
                "cast": {"points": rule["points"], "attribute_id": rule["attribute_id"]}
            }
        }]
    }
    r = requests.post(f"{BASE_URL}/open/v1/tasks/create", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]["id"]

def poll(task_id, interval=5, timeout=480):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.post(f"{BASE_URL}/open/v1/tasks/detail",
                          headers=HEADERS, json={"task_id": task_id})
        r.raise_for_status()
        task = r.json()["data"]
        medias = task.get("medias", [])
        if medias and all(m.get("resource_status") == 1 for m in medias):
            return task
        time.sleep(interval)
    raise TimeoutError(f"Task timed out: {task_id}")

# Example: generate music
products = get_products("text_to_music")
suno = next(p for p in products if p["model_id"] == "sonic")
task_id = create_task("upbeat lo-fi hip hop, 90 BPM, no vocals", suno)
result = poll(task_id)
print(result["medias"][0]["url"])
```
