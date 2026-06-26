---
name: giggle-generation-drama
description: "Use when the user wants to generate video, shoot short films, or view available video styles. Triggers: short film, make video, shoot short, AI video, generate video from story, short drama, narration video, cinematic video, available video styles."
version: "0.0.10"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      }
  }
---

[简体中文](./SKILL.zh-CN.md) | English

## ⚠️ Review Before Installing

**Please review before installing.** This skill will:

1. **Network** – Calls Giggle.pro API for video generation

**Requirements**: `python3`, `GIGGLE_API_KEY` (system environment variable), pip packages: `requests`

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Required Setup Before First Use

Before performing any operation, confirm the user has configured the API Key to avoid workflow failure due to auth errors.

- **API Key**: Log in to [Giggle.pro](https://giggle.pro/) and obtain the API Key from account settings.
- **Configuration**: Set system environment variable `GIGGLE_API_KEY`
  - `export GIGGLE_API_KEY=your_api_key`

**Verification steps**:

1. Confirm the user has configured `GIGGLE_API_KEY` in system environment.
2. If not configured, **guide the user**:
   > Hello! Before using the video generation feature, you need to configure the API Key. Please go to [Giggle.pro](https://giggle.pro/) to get your API Key, then run `export GIGGLE_API_KEY=your_api_key` in the terminal.
3. Wait for the user to configure before continuing the workflow.

## Generation Modes

Supports three modes. **Ask the user to select a mode before starting the workflow**. If not specified, default to **Episodes mode** (`director`).

| Mode | project_type | Description |
|------|--------------|-------------|
| **Episodes** | `director` | AI-directed short drama with storyboards and shot language |
| **Narration** | `narration` | Narration-focused video |
| **Short Film** | `short-film` | Story and visuals balanced; cinematic short film |

## Main Workflow: execute_workflow

Use `execute_workflow` to run the full workflow: submit + poll + auto-pay (if needed) + wait for completion. Call once and wait for return.

1. Submit task
2. Poll progress every 3 seconds
3. Detect pending payment and auto-pay (if needed)
4. Wait for completion (max 1 hour)
5. Return video download link or error

### Function Signature

```python
execute_workflow(
    diy_story: str,                           # Story/script content (required)
    aspect: str,                              # Aspect ratio: 16:9 or 9:16 (required)
    project_name: str,                        # Project name (required)
    video_duration: str = "auto",             # Duration, default "auto" (optional)
    style_id: Optional[int] = None,          # Style ID (optional)
    project_type: str = "director",           # Mode, default "director" (optional)
    character_info: Optional[List[Dict]] = None  # Character images (optional)
)
```

### Parameter Description

| Parameter | Required | Description |
|-----------|----------|-------------|
| diy_story | yes | Story or script content |
| aspect | yes | Aspect ratio: `16:9` or `9:16` |
| project_name | yes | Project name |
| video_duration | no | `auto`, `30`, `60`, `120`, `180`, `240`, `300`; default `"auto"` |
| style_id | no | Style ID; omit if not specified |
| project_type | no | `director` / `narration` / `short-film`; default `"director"` |
| character_info | no | Character image list: `[{"name": "Character name", "url": "Image URL"}, ...]` |

### Usage Flow

1. **Introduce and select generation mode** (required): Before generating, **must introduce the three modes** and let the user choose. Display:

   > We support three video generation modes. Please choose:
   >
   > **Episodes (director)**: AI director handles storyboards and shot language. Good for short drama with dialogue and plot.
   >
   > **Narration (narration)**: Narration-focused with visuals. Good for knowledge sharing, news commentary, product introductions.
   >
   > **Short Film (short-film)**: Story and visuals balanced; cinematic shots and pacing. Good for emotional shorts, creative stories, artistic expression.

   Wait for explicit user choice before continuing. If not specified, default to Episodes.

2. **If the user wants to pick a style**: Call `get_styles()` for the style list; show ID, name, category, description; wait for choice before continuing.
3. **If the user provides character image URLs**: Build `character_info` array with `name` and `url` per character.
4. **Run workflow**:
   - Call `execute_workflow()` with story, aspect ratio, project name.
   - Set `project_type` per chosen mode; pass `video_duration` if specified (else `"auto"`); pass `style_id` if chosen; pass `character_info` if provided.
   - **Call once and wait** — the function handles create, submit, poll, pay, and completion; returns download link or error.

### Examples

**View style list**:

```python
api = TrusteeModeAPI()
styles_result = api.get_styles()
# Display style list to user
```

**Basic workflow (no duration, no style)**:

```python
api = TrusteeModeAPI()
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project"
)
# result contains download URL or error
```

**Specify duration, no style**:

```python
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project",
    video_duration="60"
)
```

**Specify duration and style**:

```python
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project",
    video_duration="60",
    style_id=142
)
```

**Narration mode**:

```python
result = api.execute_workflow(
    diy_story="Today we'll talk about AI development...",
    aspect="16:9",
    project_name="Narration Video",
    project_type="narration"
)
```

**Short film mode**:

```python
result = api.execute_workflow(
    diy_story="Sunset. An old fisherman rows home alone. The sea glows red...",
    aspect="16:9",
    project_name="Short Film",
    project_type="short-film"
)
```

**With character images** (when user provides character image URLs):

```python
result = api.execute_workflow(
    diy_story="Xiao Ming and Xiao Hong meet in the park, they smile at each other...",
    aspect="16:9",
    project_name="Custom Character Video",
    character_info=[
        {"name": "Xiao Ming", "url": "https://xxx/xiaoming.jpg"},
        {"name": "Xiao Hong", "url": "https://xxx/xiaohong.jpg"}
    ]
)
```

## Return Value

The function blocks until the task completes (success or failure) or times out (1 hour). Wait for it to return.

**Success** (includes download link):

```json
{
    "code": 200,
    "msg": "success",
    "uuid": "...",
    "data": {
        "project_id": "...",
        "video_asset": {...},
        "status": "completed"
    }
}
```

Return the **full signed URL** to the user (`data.video_asset.download_url`), e.g.:

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```

Do not return unsigned URLs without query params, e.g.:

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

**Failure**:

```json
{
    "code": -1,
    "msg": "Error message",
    "data": null
}
```
