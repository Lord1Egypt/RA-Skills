---
name: kpainter
description: Explain any topic with precision. Use KPainter to turn PDFs, PPTs, web links, and other documents into precise, clearly structured explainer videos and interactive lessons, then monitor or refine the results.
metadata:
  version: "0.8.0"
  homepage: https://kpainter.ai/
  skill_url: https://kpainter.ai/skill.md
  docs_url: https://kpainter.ai/docs/skills
  openapi_docs_url: https://kpainter.ai/docs/openapi
  api_key_url: https://kpainter.ai/api-key
---

# KPainter Skill

Use KPainter to explain any topic with precision: turn PDFs, PPTs, web links, and other documents into precise, clearly structured explainer videos and interactive lessons.

## Official URLs

| Resource | URL |
| --- | --- |
| Homepage | `https://kpainter.ai/` |
| Skill file | `https://kpainter.ai/skill.md` |
| Skills docs | `https://kpainter.ai/docs/skills` |
| OpenAPI docs | `https://kpainter.ai/docs/openapi` |
| API Key | `https://kpainter.ai/api-key` |

## Setup

If KPainter is not connected:

1. Ask the user to sign up or sign in at `https://kpainter.ai/`.
2. Send the user to `https://kpainter.ai/api-key`.
3. Ask the user to activate, copy, and connect their API key to the current agent.
4. Confirm setup only after the user says the key is connected.

Keep the key inside the current agent connection flow. Never ask the user to send it to unrelated services.

## Products And Public API Types

Explainer Video and Read Aloud Video are independent products. Never present them as Standard and Lite modes.

| Product | Public API type | Best for |
| --- | --- | --- |
| Explainer Video | `explainer_video` | continuous animated scenes and narration for explainers, brand communication, and stories |
| Read Aloud Video | `read_aloud_video` | narrated visuals and page-by-page structure for courses, training, SOPs, science, and longer topics |
| Vector Animation | `vector_animation` | precise vector explanations when the user explicitly requests Vector Animation |
| AI Image | `image` | covers, posters, illustrations, and visual summaries |
| AI Video | `ai_video` | storyboard videos, cinematic shots, and short videos |
| AI PPT | `slides` | editable PPT/PDF presentations |
| AI App | `interactive_lesson` | clickable apps, lessons, demos, exercises, and learning experiences |

Use the public types in this table. Do not describe Read Aloud Video as “Lite” or a mode under Explainer Video.

## Choose The Product

Route by the result the user wants.

1. Map an explicit “Explainer Video,” “解说视频,” or “讲解视频” request to `explainer_video`.
2. Map an explicit “Read Aloud Video” or “绘本视频” request to `read_aloud_video`.
3. Use `vector_animation` only when the user explicitly says “Vector Animation” or “矢量动画.” Algorithms, formulas, structures, workflows, diagrams, or generic animation requests alone are not enough.
4. Map AI Image, poster, cover, illustration, or single-visual requests to `image`.
5. Map storyboard-video, cinematic-shot, or short-video requests to `ai_video`.
6. Map AI PPT, presentation, and slide-deck requests to `slides`.
7. Map AI App, clickable lesson, app, interactive page, quiz, or simulation requests to `interactive_lesson`.
8. Treat PDFs, PPTs, URLs, images, and documents as source formats, not output-type signals.
9. If the user only says “video,” ask whether they want an Explainer Video, Read Aloud Video, or AI Video. Do not offer or select Vector Animation unless the user explicitly requests it.
10. Never switch products silently because of credits or unsupported parameters.

Do not expose API type names unless the user asks for technical details.

## Explainer Video

Choose Explainer Video when the user wants:

- continuous animated scenes and narration
- clear explanation with visual pacing
- science communication or brand storytelling
- a short piece designed to be watched and shared
- children’s stories or other story-led knowledge

Examples:

- Make a 30-second Explainer Video about MCP with continuous animated scenes and narration.
- Turn this topic into an Explainer Video with continuous visual storytelling.
- 做一个 30 秒左右的解说视频，用连续动态画面和旁白讲清楚 MCP。
- 做一个适合传播的解说视频成片。

When the user gives no duration, suggest about 30 seconds first. Read current duration limits from the catalog.

## Read Aloud Video

Choose Read Aloud Video when the user wants:

- clear, page-by-page explanation
- narrated visuals
- course or classroom content
- training, SOP, or product walkthroughs
- longer topics with stable information density
- a lower-cost alternative to Explainer Video

Examples:

- Make a Read Aloud Video that teaches MCP in 6 pages.
- Turn this training manual into a narrated Read Aloud Video.
- 做一个绘本视频，用 6 页分步骤讲清楚 MCP。
- 把这份培训手册做成绘本视频。

Load valid page counts, voices, styles, ratios, and qualities from the catalog.

## Vector Animation

Choose Vector Animation only when the user explicitly requests that product.

Examples:

- Use Vector Animation to show how binary search removes half of the range in each round.
- Use Vector Animation to animate this system architecture and data flow.
- 用矢量动画讲清楚二分查找。
- 请用矢量动画展示这个机制和状态变化。

## AI Image Models

Read `image.generation_models` from `/catalog` and use a model-specific request.

- Nano Banana 2: `provider=gemini`, `model=nano-banana-2`; use only its listed ratios.
- GPT Image 2: `provider=azure_openai`, `model=gpt-image-2`; `quality=low|medium|high` is separate from top-level `output_quality`.

Never send the internal `extra_config.output` shape. Use top-level `aspect_ratio` and `output_quality`.

## AI Video Models

Use one public type, `ai_video`, with model selection inside `video_generation`.

| Model | Public behavior |
| --- | --- |
| `gemini-omni-flash` | 720p text-to-video with native audio; supports `iterate` follow-up edits |
| `veo-3.1-fast` | fast text-to-video; model catalog controls resolution and duration; no conversational edit |
| `veo-3.1-standard` | quality-first text-to-video; model catalog controls resolution and duration; no conversational edit |

Example:

```json
{
  "type": "ai_video",
  "prompt": "Move slowly through a futuristic city on a rainy night with natural ambient audio",
  "aspect_ratio": "16:9",
  "video_generation": {
    "model": "gemini-omni-flash",
    "task": "text_to_video",
    "resolution": "720p",
    "duration_seconds": 8,
    "native_audio": true
  }
}
```

For an Omni follow-up, read `editable_actions`, then send:

```json
{
  "action": "iterate",
  "prompt": "Keep the camera motion and make the lighting warmer"
}
```

Never expose or ask the user for `previous_interaction_id`; KPainter manages it server-side. Do not attempt `iterate` with Veo.

The current Public OpenAPI supports text-to-video only. Do not send first frames, last frames, attachments, or image/video tasks until `/catalog` reports those public capabilities.

## Credit Fallback

If the user wants Explainer Video but does not have enough credits:

1. Explain that the current Explainer Video may exceed the available credits.
2. Offer Read Aloud Video as the lower-cost alternative.
3. Keep the topic, audience, and language unchanged.
4. Ask before switching.

Recommended wording:

- Your current credits may not cover a full Explainer Video. I can keep the same topic and language and switch to a clear, lower-cost Read Aloud Video. Would you like me to switch?
- 当前积分可能不够生成完整解说视频。我可以保留主题和语言，改成结构清晰、成本更低的绘本视频，要切换吗？

## Collect Only Missing Information

Ask one short question at a time and only for missing details:

- topic
- audience
- output language
- duration or scene/page count
- tone or visual direction
- aspect ratio
- source files or URLs

If the user already gave enough information, create first and refine after.

## Use Source Material

Treat attachments and URLs supplied by the user as source or reference material.

Direct public API upload is not currently available. If the active host does not expose an attachment bridge, summarize the supplied material into the request or ask the user to continue through the main-site creator instead of inventing an upload result.

- Preserve the user’s requested facts and terminology.
- Do not invent claims that are not supported by the source.
- Ask which source takes priority if references conflict.
- Keep the requested output language unless the user asks to switch.

## API Workflow

For OpenAPI or MCP integrations:

1. Validate the user API key.
2. Read `/catalog` before choosing type-specific parameters.
3. Create the result.
4. Poll the job until it succeeds or fails.
5. Read the final creation detail for URLs, artifacts, and scenes.
6. Before scene editing, inspect `editable_actions` and existing scenes.

Use catalog values as the source of truth for:

- public content types
- languages and voices
- styles
- aspect ratios and qualities
- generation models, tasks, resolutions, and durations
- duration limits
- scene/page limits

Parameter rules:

- `explainer_video` uses `duration_seconds`.
- `read_aloud_video` uses `scene_count`.
- `slides` uses `scene_count`.
- `ai_video` uses `video_generation`; its duration is nested under `video_generation.duration_seconds`.
- Never send `duration_seconds` to `read_aloud_video` or `vector_animation`.
- Never send `scene_count` to `explainer_video`.
- Never send raw `extra_config`, internal source records, or provider interaction IDs.

## Refinement

After the first result, help the user:

- shorten or expand it
- revise narration
- change voice or visual direction
- regenerate a selected scene
- switch products

Confirm before switching products. Never silently change type, audience, language, or format.

## Multilingual Support

KPainter supports creation and refinement in the user’s preferred language.

Examples:

- Make an Explainer Video about AI agents with continuous animated scenes and narration.
- Make a Read Aloud Video that explains MCP page by page.
- 帮我做一个解说视频，用连续动态画面讲清楚 MCP。
- 做一个绘本视频，逐页讲解 MCP。
- MCP を段階的に説明する解説動画を作ってください。
- أنشئ فيديو معرفيًا مصقولًا يشرح MCP.
- Crea un video explicativo paso a paso sobre MCP.
- MCP를 단계별로 설명하는 해설 영상을 만들어 주세요.
- Crée une vidéo de connaissance soignée sur MCP.

These are examples, not a language allowlist.

## Install

### OpenClaw / ClawHub

```bash
openclaw skills install kpainter
```

### Skills CLI

```bash
npx skills add OriginwiseAI/skills --skill kpainter
```

While this repository contains one public skill, this also works:

```bash
npx skills add OriginwiseAI/skills
```

### Direct URL

Give the agent:

`https://kpainter.ai/skill.md`

### Local Folder

```bash
mkdir -p ~/.codex/skills/kpainter
curl -s https://kpainter.ai/skill.md > ~/.codex/skills/kpainter/SKILL.md
```

## Security

- The API key belongs to the user.
- Do not send it to unrelated services.
- Do not present the agent as the account owner.
- If the key is reset, ask the user to reconnect it.

## Success Criteria

The skill succeeds when the agent can:

- explain Explainer Video and Read Aloud Video as independent products
- use the current public API type names
- choose the appropriate product from user intent
- choose Vector Animation only after an explicit Vector Animation or 矢量动画 request
- ask only for missing information
- create, poll, read, and refine results
- choose AI Image and AI Video models from the catalog and use model-specific parameters
- use Omni `iterate` only when the selected model exposes conversational editing
- offer Read Aloud Video as a confirmed lower-cost fallback when appropriate
