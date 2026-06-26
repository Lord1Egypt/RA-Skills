---
name: litmedia-skill
description: "Generate, Edit, Collaborate. Access all mainstream AI models in one toolkit. Simply describe your vision to create videos, images, and avatars—zero manual operations."
metadata:
  tags: litmedia, avatar, video, image, voice, ai, api, i2v, t2v, a2ls, anim, text2image, image_edit, tts, voice_clone
  requires:
    bins: [python3]
  primaryEnv: LITMEDIA_API_KEY
---

# LitMedia AI Skill

> Modular Python toolkit for the [LitMedia AI](https://www.litmedia.ai) API.

✨ **Generate. Edit. Collaborate. — All in One Place.** ✨

- 🧠 **All Mainstream Models**: Seamlessly access the world's top-tier AI models for video, image, and voice in one toolkit.
- 🗣️ **Describe to Create**: Just tell the agent what you want. From talking avatars to product composites, your prompts generate the exact output.
- ⚡ **Zero Manual Ops**: No manual uploads, no tedious tweaking.

## Execution Rule

> **Always use the Python scripts in `scripts/`. Do NOT use `curl` or direct HTTP calls.**

## User-Facing Reply Rules

> **⚠️ HIGHEST PRIORITY — every user-facing reply MUST follow ALL rules below.**
>
> Most users are non-technical. Many chat from Feishu, WeChat, or similar apps and **cannot** see local browser popups or terminals.

1. **Keep replies short** — give the result or next step directly. If one sentence is enough, don't write three.
2. **Use plain language** — no API jargon, no terminal references, no mentions of environment variables, polling, JSON, scripts, or "auth flow". Speak as if the user has never seen a command line.
3. **Never mention terminal details** — do not reference command output, logs, exit codes, file paths, config files, or any technical internals. These mean nothing to the user.
4. **Never ask the user to operate a browser popup** — the user cannot see the agent's machine screen. When login is needed, the **only** correct action is to send the authorization link directly in the chat.
5. **Always send the direct login link** — extract `URL: ...` from `auth.py login` output and use the login template below. Never say "browser opened" or similar. **If the URL is not found in the output, re-run `auth.py login` to get a new link. Never skip sending the link.**
6. **Wait for user confirmation after login** — ask the user to reply "好了" / "done", then continue the task.
7. **Handle account switching properly** — when switching accounts, use `auth.py accountswitch` and remind the user to log out of their current LitMedia web account or log in with the new account on the website first. After the switch, wait for user confirmation before proceeding.
8. **Explain errors simply** — if a task fails, tell the user in one sentence what happened and ask if they want to retry. Never paste error messages or technical details.
9. **Be result-oriented** — after task completion, give the user the result (link, image, video) directly. Do not describe intermediate steps.
10. **Always take the user's perspective** — the user can only see the chat conversation, nothing else. Anything requiring user action (links, confirmations) must appear in the chat.
11. **Do not tell the user to register separately** — the authorization page includes both login and sign-up. New users can register directly on that page. Never say "go to litmedia.ai to register first".
12. **Act directly, don't ask which method** — when login is needed, just run `auth.py login` and send the link. Don't ask "which method do you prefer?" or present multiple options. The user asked you to do something — login is just an intermediate step, handle it.
13. **Give time estimates for generation tasks** — after submitting a task, tell the user the estimated wait time so they know what to expect. Use the estimates from the "Estimated Generation Time" table below.

**Estimated Generation Time**

> Tell the user the estimated wait time after submitting a task. Match the user's language.

| Task Type | Model | Estimated Time                      |
|-----------|-------|-------------------------------------|
| Video | Standard / Fast (Seedance 2.0) | ~5–10 min                           |
| Video | All other video models (Kling, Sora, Veo, Vidu, etc.) | ~3–5 min                            |
| Image | image models (Nano Banana, Seedream etc.) | ~30s–1 min                          |
| Avatar | avatar4 | ~2–5 min (depends on script length) |
| Character Replace | `Kling V3.0`, `Seedance 2.0`, `Wan 2.2`   | ~3–5 min                            |

Example messages after submitting:
- Chinese: "已经开始生成了，视频大约需要 5-10 分钟，请稍等~"
- English: "Generation started — the video will take roughly 5–10 minutes. I'll send it to you as soon as it's ready."

**Required login message template**

Replace `<LOGIN_URL>` with the actual link. Follow the user's language (Chinese template for Chinese users, English for English users).

中文模板：

```text
安装完成，LitMedia Skill 已连接到你的智能助手。

复制下方链接到浏览器中登录，登录后将解锁以下能力：

<LOGIN_URL>

🎬 视频生成
文字转视频、图片转视频、参考视频生成，自动配音配乐。
视频模型：Seedance 2.0 · Sora 2 · Kling 3 · Veo 3.1 · Vidu Q3 · wan2.7

🖼️ AI 图片生成与编辑
文字生图、AI 修图、风格转换，最高支持 4K。
图片模型：Nano Banana · Nano Banana 2 · Nano Banana Pro · Seedream 4.0 · Seedream 4.5 · Seedream 5.0

🧑‍💼 口播数字人
上传一张照片 + 一段音频，自动生成真人口播视频，支持多语种。

✂️ 角色替换(动作模仿)
上传一张角色照片 + 动作视频，视频中的人物替换成图片中的角色或者照片中的人物会模仿视频中的动作

🎙️ 语音与配音
文字转语音、声音克隆，支持多语种配音输出。

登录完成后回我一句"好了"，我马上继续。
```

English template:

```text
Installation complete. LitMedia Skill is now connected to your agent.

Copy the link below into your browser to sign in. After signing in, the following capabilities will be unlocked.

<LOGIN_URL>

🎬 Video Generation
Text-to-video, image-to-video, reference-based generation with auto sound & music.
Models: Seedance 2.0 · Sora 2 · Kling 3 · Veo 3.1 · Vidu Q3 · wan2.7

🖼️ AI Image Generation & Editing
Text-to-image, AI retouching, style transfer — up to 4K resolution.
Models: Nano Banana · Nano Banana 2 · Nano Banana Pro · Seedream 4.0 · Seedream 4.5 · Seedream 5.0

🧑‍💼 Talking Avatar
Upload a photo + audio to auto-generate presenter-style talking head videos.

✂️ Character Replace
Upload a character photo along with an action video. In the video, replace the characters with those from the picture or the characters in the picture will imitate the actions shown in the video.

🎙️ Voice & TTS
Text-to-speech, voice cloning, multilingual dubbing and narration.

Once you've signed in, just reply "done" and I'll continue right away.
```

**Banned phrases (including any variations):**

- "Browser has opened" / "browser popped up"
- "Run this in the terminal" / "run the login command"
- "Check the popup" / "look at the browser"
- "Set the environment variable"
- "Command executed successfully"
- "Polling task status"
- "Script output is as follows"
- "Go operate on that computer" / "check the robot's computer"
- "Authorization page popped up" / "if the page appeared"
- "Go to litmedia.ai to register first" — auth page has built-in registration
- "Which method do you prefer?" / "two options for you" — don't give choices, just act
- "Auth flow" / "perform authentication" / "complete authentication" — too technical
- "Python config" / "environment setup" — user doesn't need to know
- Anything asking the user to operate outside the chat window
- Anything containing code, commands, or file paths

**Fallback when login URL is not captured:**

> If `auth.py login` output does not contain a `URL:` line (e.g. background execution missed the output), **re-run `auth.py login`** to get a fresh link.
> **NEVER** fall back to telling the user to "check the browser popup" or "go operate on the agent's computer". The user cannot see it.

## Prerequisites

- **Python 3.8+**
- **Authenticated** — see [references/auth.md](references/auth.md) for the direct-link login flow
  - **First-time setup**: After installing this skill, run `python {baseDir}/scripts/auth.py login` 
  - Use `python {baseDir}/scripts/auth.py status` to check current login state
- Credits available — see [references/user.md](references/user.md) to check balance
- Env vars `LITMEDIA_UID` + `LITMEDIA_API_KEY` are handled automatically after login; manual setup is only for CI/internal use

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent Workflow Rules

> **These rules apply to ALL generation modules (avatar4, video_gen, ai_image, video_mimic).**

1. **Always start with `run`** — it submits the task and polls automatically until done. This is the default and correct choice in almost all situations.
2. **Do NOT ask the user to check the task status themselves.** The agent is responsible for polling until the task completes or the timeout is reached.
3. **Only use `query`** when `run` has already timed out and you have a `taskId` to resume, or when the user explicitly provides an existing `taskId`.
4. **`query` polls continuously** — it keeps checking every `--interval` seconds until status is `completed` or `failed`, or `--timeout` expires. It does not stop after one check.
5. **If `query` also times out** (exit code 2), increase `--timeout` and try again with the same `taskId`. Do not resubmit unless the task has actually failed.

```
Decision tree:
  → New request?           use `run`
  → run timed out?         use `query --task-id <id>`
  → query timed out?       use `query --task-id <id> --timeout 1200`
  → task status=fail?      resubmit with `run`
```

**Task Status:**

| Status    | Description |
|-----------|-------------|
| `init`    | Task is queued, waiting to be processed |
| `working` | Task is actively being processed |
| `completed` | Task completed successfully |
| `failed`    | Task failed |

## MANDATORY Pre-Execution Protocol

> **CRITICAL: Before EVERY generation task, you MUST follow these steps WITHOUT EXCEPTION.**
> 
> **DO NOT proceed with any generation task until the user explicitly confirms the parameters.**

### Step 1: Estimate Cost

- **Video tasks**: Use `video_gen.py estimate-cost --model <model> --resolution <res> --duration <dur> --count <count>`
- **Image tasks**: Use `ai_image.py estimate-cost`
- **Avatar4**: Cost depends on video length

### Step 2: Validate Parameters

Use `list-models` to ensure model, aspect ratio, resolution, and duration are compatible:
```bash
python scripts/video_gen.py list-models --type <t2v|i2v|extend|anim|a2ls>
```

## Modules

| Module | Script | Reference | Description                                                                           |
|--------|--------|-----------|---------------------------------------------------------------------------------------|
| Auth | `scripts/auth.py` | [auth.md](references/auth.md) | OAuth 2.0 Device Flow — generate login link, wait for authorization, save credentials; supports account switching via `accountswitch` command |
| Avatar4 | `scripts/avatar4.py` | [avatar4.md](references/avatar4.md) | Talking avatar videos from a photo; `list-captions` for caption styles                |
| Video Gen | `scripts/video_gen.py` | [video_gen.md](references/video_gen.md) | Image-to-video, text-to-video, video extension, ai animation, lip sync                |
| AI Image | `scripts/ai_image.py` | [ai_image.md](references/ai_image.md) | Text-to-image and AI image editing (10+ models)                                       |
| Character Replace | `scripts/video_mimic.py` | [video_mimic.md](references/video_mimic.md) | Character Replace in Videos with Scene Consistency using LitMedia Common Task APIs.   |
| User | `scripts/user.py` | [user.md](references/user.md) | Credit balance and usage history                                                      |

> **Read individual reference docs for usage, options, and code examples.**
> Local files (image/audio/video) are auto-uploaded when passed as arguments — no manual upload step needed.

---

## Creative Guide

> **Core Principle:** Start from the user's intent, not from the API.
> Analyze what the user wants to achieve, then pick the right tool, model, and parameters.

### Step 1 — Intent Analysis

Every time a user requests content, identify:

| Dimension | Ask Yourself | Fallback |
|-----------|-------------|----------|
| **Output Type** | Image? Video? Audio? Composite? | Must ask |
| **Purpose** | Marketing? Education? Social media? Personal? | General social media |
| **Source Material** | What does the user have? What's missing? | Must ask |
| **Style / Tone** | Professional? Casual? Playful? Authoritative? | Professional & friendly |
| **Duration** | How long should the output be? | 5–15s for clips, 30–60s for avatar |
| **Language** | What language? Need captions? | Match user's language |
| **Channel** | Where will it be published? | General purpose |

### Step 2 — Tool Selection

```
What does the user need?
│
├─ A person speaking to camera (talking head)?
│  → avatar4 or video_gen with native-audio models
│
├─ An image animated into a video clip?
│  → video_gen --type i2v
│
├─ A video generated purely from text?
│  → video_gen --type t2v
│
├─ A new video based on reference style (style transfer, editing)?
│  → video_gen --type anim
│
├─ Generate a new video based on the extended version of the original video
│  → video_gen --type extend
│
├─ A new video based on reference image and sound (Lip Sync)?
│  → video_gen --type a2ls
│
├─ An image generated from a text prompt?
│  → ai_image --type text2image
│
├─ An existing image edited / modified with AI?
│  → ai_image --type image_edit
│
├─ Replace the video characters with photo characters
│  → Character Replace
│
├─ Photo characters imitate the ations of the video characters
│  → Character Replace
│
├─ Browse available caption styles for avatar videos?
│  → avatar4 list-captions
│
├─ view user all results?
│  → user logs
│
└─ Outside current capabilities?
   → See Capability Boundaries below
```

**Quick-reference routing table:**

| User says...                                              | Script & Type                                                            |
|-----------------------------------------------------------|--------------------------------------------------------------------------|
| "Make a talking avatar video with this photo and text"    | `avatar4.py` (pass local image path directly)                            |
| "Generate a video with this photo and my audio recording" | `avatar4.py` (pass local image + audio paths)                            |
| "Animate this image / image-to-video"                     | `video_gen.py --type i2v` (pass local image path)                        |
| "Generate a video about..."                               | `video_gen.py --type t2v`                                                |
| "Generate a new video referencing this image's style"     | `video_gen.py --type anim`                                               |
| "Extend the original videoo"                              | `video_gen.py --type extend`                                             |
| "Generate a new video referencing image and sound"        | `video_gen.py --type a2ls`                                               |
| "Generate an image / text-to-image"                       | `ai_image.py --type text2image`                                          |
| "Modify this image / change background"                   | `ai_image.py --type image_edit`                                          |
| "Character Replace / Action imitation"                    | `video_mimic.py`                                                         |
| "What caption styles are available?"                      | `avatar4.py list-captions`                                               |
| "View my creation history / check what was generated"     | `user.py logs --type image` or `user.py logs --type video`               |
| "Check how many credits I have left"                      | `user.py credit`                                                         |

> **Video model selection** — see [references/video_gen.md](references/video_gen.md) § Model Recommendation.

> **Image model tip:** For all image tasks, default to **Nano Banana** — strongest all-round model with best quality, 7 aspect ratios, and 14 reference images for editing. See [references/ai_image.md](references/ai_image.md) § Model Recommendation.

> **Caption styles for avatar4:** Use `avatar4.py list-captions` to discover available caption styles, then pass the `captionId` via `--caption`.

> **Talking-head tip — avatar4 vs video_gen with native audio:**
> Some video_gen models (e.g. Standard, Kling V3, Veo 3.1) support native audio and can produce talking-head videos with **better visual quality** than avatar4. However, they have **shorter max duration** (5–15s) and are **significantly more expensive**. Avatar4 supports up to 120s per segment at much lower cost.
> **Rule of thumb:** Default to avatar4 for most talking-head needs. Consider video_gen native-audio models only when the clip is short (<=15s) and the user explicitly prioritizes top-tier visual quality over cost.

### Step 3 — Simple vs Complex

**Simple requests** — the user's need is clear, materials are ready → handle directly from the reference docs.

**Complex requests** — the user gives a *goal* (e.g., "make a promo video", "explain how AI works") rather than a direct API instruction. Follow this universal workflow:

1. **Deconstruct & Clarify:** Ask the user for the target audience, core message, intended duration, and what assets they currently have (photos, scripts).
2. **Determine the Route:**
   - *Has a person's photo + needs narration* → Use `avatar4` (Talking Head).
   - *Has a product/reference photo* → Use `video_gen --type i2v` or `anim`.
   - *No assets, purely visual concept* → Use `video_gen --type t2v`.
   - *Requires both* → Plan a Hybrid approach (Avatar narration + B-roll inserts).
3. **Structure the Content:**
   - Write a structured script (Hook → Body/Explanation → Call to Action).
   - Add `<break time="0.5s"/>` tags to TTS scripts for natural pacing.
   - For visuals, write detailed prompts covering Subject + Action + Lighting + Camera.
4. **Handle Long-Form (>120s):** If the script exceeds the 120s limit for a single `avatar4` task, split it into logical segments (e.g., 60s each) at natural sentence boundaries. Submit tasks in parallel using the `submit` command, ensure parameters (voice/model) remain locked across segments, and deliver them in order.

---

## Pre-Execution Protocol

> Follow this before EVERY generation task.

1. **Estimate cost** — use `video_gen.py estimate-cost` for video tasks, `ai_image.py estimate-cost` for image tasks; avatar4 costs depend on video length
2. **Validate parameters** — ensure model, aspect ratio, resolution, and duration are compatible (use `list-models` to check)
3. **Ask about missing key parameters** — if the user has not specified important parameters that affect the output, ask before proceeding. Key parameters by module:
   - **video_gen**: duration, aspect ratio, model
   - **ai_image**: aspect ratio, resolution, model, number of images
   - **avatar4**: (usually determined by input, but confirm voice if not specified)
   - Do NOT silently pick defaults for these — always confirm with the user.
4. **Confirm before first submission** — before the very first generation task in a session, present the full plan (tool, model, parameters, cost estimate) and ask the user:
   - Whether to proceed with the generation
   - Whether they want the agent to ask for confirmation before each subsequent task, or trust the agent to proceed automatically for the rest of the session
   - These two questions should be combined into a single confirmation message.
   - If the user chooses "auto-proceed", skip the confirmation step (but still ask about missing parameters) for subsequent tasks in the same session.
   - If the user explicitly said "just do it" or similar upfront, treat it as auto-proceed from the start.

## Agent Behavior Protocol

### During Execution

1. **Pass local paths directly** — scripts auto-upload local files to OSS before submitting tasks
2. **Parallelize independent steps** — independent generation tasks can run concurrently
3. **Keep consistency across segments** — when generating multiple segments, use identical parameters

### After Execution

> **Use the structured result templates below.** The user should see the output link first, then key metadata. Keep it clean and scannable.

**Video result template:**

```text
🎬 视频已生成完成

🔗视频地址：<VIDEO_URL>
• 时长：<DURATION>
• 画幅：<ASPECT_RATIO>
• 模型：<MODEL_NAME>
• 消耗：<COST> credits

不满意的话可以告诉我，我帮你调整后重新生成。
```

**Image result template:**

```text
🖼️ 图片已生成完成

🔗 图片地址：<IMAGE_URL>
• 分辨率：<RESOLUTION>
• 模型：<MODEL_NAME>
• 消耗：<COST> credits

不满意的话可以告诉我，我帮你调整后重新生成。
```

**English video result template:**

```text
🎬 Video generated

🔗 Video: <VIDEO_URL>
• Duration: <DURATION>
• Aspect ratio: <ASPECT_RATIO>
• Model: <MODEL_NAME>
• Cost: <COST> credits

View, edit, and download in the project.

Not happy with the result? Let me know and I'll adjust and regenerate.
```

**English image result template:**

```text
🖼️ Image generated

🔗 Image: <IMAGE_URL>
• Resolution: <RESOLUTION>
• Model: <MODEL_NAME>
• Cost: <COST> credits

Not happy with the result? Let me know and I'll adjust and regenerate.
```

**Rules:**
1. **Result link first** — always show the video/image URL at the very top.
2. **Key metadata only** — duration, aspect ratio/resolution, model, cost. Don't dump raw JSON or extra fields.
3. **Offer iteration** — end with a short note that the user can ask for adjustments. Remind that regeneration costs additional credits.
4. **Multiple outputs** — if the task produced multiple results, number them (1, 2, 3…) each with its own link and metadata.
5. **Match user language** — use the Chinese template for Chinese users, English for English users.

### Error Handling

See [references/error_handling.md](references/error_handling.md) for error codes, task-level failures, and recovery decision tree.

---

## Capability Boundaries

| Capability                  | Status | Script                                                                     |
|-----------------------------|--------------|----------------------------------------------------------------------------|
| Photo avatar / talking head | Available | `scripts/avatar4.py`                                                       |
| Caption styles              | Available | `scripts/avatar4.py list-captions`                                         |
| Credit management           | Available | `scripts/user.py`                                                          |
| Image-to-video (i2v)        | Available | `scripts/video_gen.py --type i2v`                                          |
| Text-to-video (t2v)         | Available | `scripts/video_gen.py --type t2v`                                          |
| Video Extension (extend)    | Available | `scripts/video_gen.py --type extend`                                       |
| Animation (anim)            | Available | `scripts/video_gen.py --type anim`                                         |
| Audio-to-Lip-sync (a2ls)    | Available | `scripts/video_gen.py --type a2ls`                                         |
| Text-to-image               | Available | `scripts/ai_image.py --type text2image`                                    |
| Image editing               | Available | `scripts/ai_image.py --type image_edit`                                    |
| Character Replace           | Available | `scripts/video_mimic.py`                                                   |
| Creation history browsing   | Available | `scripts/user.py logs --type image` or `scripts/user.py logs --type video` |
| Marketing video (m2v)       | No module | Suggest [litmedia.ai](https://www.litmedia.ai) web UI                      |

> **Never promise capabilities that don't exist as modules.**
