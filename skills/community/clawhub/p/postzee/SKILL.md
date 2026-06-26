---
name: postzee
description: Generate AI images/videos and post to 30+ social media platforms with Postzee. Use when the user wants to create AI media, generate images or videos, optimize prompts, create HeyGen avatar videos, or schedule social media posts.
user-invocable: true
metadata: {"primaryEnv": "POSTZEE_API_KEY", "emoji": "🎨"}
---

# Postzee — AI Social Media Studio

You are connected to **Postzee**, an AI-powered social media management platform. You can generate stunning images and videos with AI, optimize prompts automatically, and post to 30+ social networks — all in one conversation.

## Setup (First Time Only)

If the MCP server is not configured yet, help the user set it up:

1. **Ask for the MCP URL**: "Copy your MCP URL from https://dashboard.postzee.app/settings → tab 'API Pública' → section 'MCP (Model Context Protocol)'. It looks like: `https://api.postzee.app/mcp/.../sse`"
2. **Configure MCP**:
   - **Claude Code**: Run `claude mcp add --transport sse postzee <MCP_URL>` (paste the full URL)
   - **OpenClaw**: Store the MCP URL via the `primaryEnv` configuration.
3. **Verify**: Call `POSTZEE_GET_CREDITS` to confirm the connection works.

If the user says "install postzee" or "configure postzee", run this setup flow.

## Available MCP Tools

| Tool | What it does |
|------|-------------|
| `POSTZEE_LIST_CHANNELS` | List connected social media accounts |
| `POSTZEE_GET_CREDITS` | Check available AI credit balance |
| `POSTZEE_LIST_IMAGE_MODELS` | Show available AI image models with costs |
| `POSTZEE_LIST_VIDEO_MODELS` | Show available AI video models with costs |
| `POSTZEE_ENHANCE_PROMPT` | Optimize a prompt for better AI results |
| `POSTZEE_GENERATE_IMAGE` | Generate an AI image (supports reference images, aspect ratio, quality, style) |
| `POSTZEE_GENERATE_VIDEO` | Generate an AI video (supports image-to-video, duration, aspect ratio) |
| `POSTZEE_GENERATE_HEYGEN_VIDEO` | Create an avatar video with HeyGen AI |
| `POSTZEE_LIST_HEYGEN_AVATARS` | List available HeyGen avatars |
| `POSTZEE_LIST_HEYGEN_VOICES` | List available HeyGen voices |
| `POSTZEE_CHECK_JOB` | Check generation job status (poll until "success") |
| `POSTZEE_CREATE_POST` | Create or schedule a social media post |

## Workflow — Generate AI Image

1. **Check credits** — call `POSTZEE_GET_CREDITS`. If 0, suggest purchasing at https://dashboard.postzee.app/credits.
2. **Enhance the prompt** — call `POSTZEE_ENHANCE_PROMPT`. Always do this unless the user explicitly says not to. Show the enhanced prompt for approval.
3. **Show model options** — call `POSTZEE_LIST_IMAGE_MODELS`. Present 2-3 recommended options with credit costs.
4. **Generate** — call `POSTZEE_GENERATE_IMAGE` with:
   - `prompt`: the enhanced prompt
   - `model`: chosen model ID
   - `aspectRatio`: based on target platform (see table below)
   - `imageUrls`: reference images if the user provided any
   - `quality`: for GPT Image 2 ("low", "medium", "high")
   - `style`: for Recraft models ("realistic_image", "digital_illustration", "vector_illustration")
5. **Poll** — call `POSTZEE_CHECK_JOB` every 5 seconds until "success" or "failed".

### Image-to-Image (Reference Images)

When the user wants to transform or use a photo as reference:
- **OpenClaw (Telegram)**: The user sends a photo in chat — use the received image URL in `imageUrls`
- **Claude Code**: The user provides a public URL — pass it in `imageUrls`
- **From previous generation**: Use the `mediaUrl` returned by `POSTZEE_CHECK_JOB`

Example: "Transform my photo into an anime style" — enhance prompt + pass the photo URL in `imageUrls`

## Workflow — Generate AI Video

1. **Check credits** — call `POSTZEE_GET_CREDITS`.
2. **Enhance the prompt** — call `POSTZEE_ENHANCE_PROMPT` with `mediaType: "video"`.
3. **Generate** — call `POSTZEE_GENERATE_VIDEO` with:
   - `prompt`: enhanced prompt
   - `model`: chosen model ID
   - `duration`: seconds (e.g., "5", "8", "10")
   - `aspectRatio`: based on platform
   - `imageUrl`: reference image for image-to-video (animate a photo)
4. **Poll** — call `POSTZEE_CHECK_JOB` every 5 seconds.

### Image-to-Video (Animate a Photo)

When the user wants to animate a photo into video:
- Pass the image URL in `imageUrl` parameter
- Suggest vertical models for Stories/Reels/TikTok (9:16)
- Best models for I2V: Kling 3.0 Pro, Veo 3.1, Luma Ray 2

## Workflow — HeyGen Avatar Video

HeyGen creates videos with AI avatars speaking custom text. **HeyGen uses its own credits (not Postzee credits).**

1. **List avatars** — call `POSTZEE_LIST_HEYGEN_AVATARS`. If not configured, inform the user to set up at https://dashboard.postzee.app/settings.
2. **List voices** — call `POSTZEE_LIST_HEYGEN_VOICES`. Let the user choose.
3. **Generate** — call `POSTZEE_GENERATE_HEYGEN_VIDEO` with:
   - `script`: text for the avatar to speak (20-1500 chars)
   - `avatarId`: chosen avatar
   - `voiceId`: chosen voice
   - `aspectRatio`: "16:9" or "9:16"
4. **Poll** — call `POSTZEE_CHECK_JOB` every 5 seconds.

**Important**: HeyGen videos do NOT consume Postzee credits. They use the user's HeyGen account credits.

## Workflow — Post to Social Media

1. **List channels** — call `POSTZEE_LIST_CHANNELS`. If none connected, direct to https://dashboard.postzee.app/channels
2. **Ask which channel(s)** — let the user choose.
3. **Create post** — call `POSTZEE_CREATE_POST` for **each** channel:
   - `type: "now"` — publish immediately (**default when user says "post" or "publish"**)
   - `type: "schedule"` — with `date` in UTC
   - `type: "draft"` — save as draft
   - `mediaUrls` — attach generated media URLs

### Multi-channel posting
- Call `POSTZEE_CREATE_POST` once per channel with the same content.
- If user wants different text per platform, ask before creating.

## Quick Actions

Execute the full flow without asking at each step:

- **"Generate and post to Instagram"** — credits → enhance → generate (4:5) → poll → channels → post
- **"Create a video for TikTok"** — credits → enhance → generate video (9:16) → poll → channels → post
- **"Animate my photo"** — credits → enhance → generate video with imageUrl → poll
- **"Create a HeyGen video"** — avatars → voices → generate → poll
- **"Post this text to all channels"** — channels → create post on each

## Smart Model Recommendations

### Image Models
| Intent | Model | Why |
|--------|-------|-----|
| Photorealistic photos | Nano Banana 2 or GPT Image 2 | Best quality for photos |
| Logos, icons, vectors | Recraft V4 | Native vector output |
| Text in images (posters) | Ideogram V3 | Perfect text rendering |
| Artistic/creative | GPT Image 2 or Recraft V3 | Versatile styles |
| Budget-friendly | Nano Banana | Cheapest option |
| Maximum quality | GPT Image 2 High or Recraft V4 Pro | Premium output |

### Video Models
| Intent | Model | Why |
|--------|-------|-----|
| Cinematic clips | Kling 3.0 Pro or Veo 3.1 | High quality |
| Quick social content | Veo 3.1 Fast or Luma Ray 2 Flash | Fast + affordable |
| Animate a photo | Kling 3.0 Pro or Veo 3.1 | Best I2V quality |
| High production | Sora 2 Pro | Premium (expensive) |
| Budget-friendly | Seedance 1.0 Lite | Cheapest video |
| Avatar speaking | HeyGen | Realistic AI avatars |

Always show credit cost next to recommendations.

## Platform-Aware Aspect Ratios

Automatically apply when the user mentions a platform:

| Platform | Aspect Ratio |
|----------|-------------|
| Instagram Feed | 1:1 or 4:5 |
| Instagram Stories/Reels | 9:16 |
| TikTok | 9:16 |
| YouTube | 16:9 |
| YouTube Shorts | 9:16 |
| LinkedIn | 16:9 or 1:1 |
| X (Twitter) | 16:9 |
| Facebook | 16:9 or 1:1 |
| Pinterest | 2:3 |

Default to 16:9 if no platform is mentioned.

## Error Handling

- **Generation failed** — suggest different model or simpler prompt
- **Insufficient credits** — show balance + cheapest model + link to https://dashboard.postzee.app/credits
- **No channels connected** — direct to https://dashboard.postzee.app/channels
- **HeyGen not configured** — direct to https://dashboard.postzee.app/settings
- **Polling timeout (>3 min)** — direct to https://dashboard.postzee.app to check result

## Guidelines

- **Always enhance prompts** before generating — results are dramatically better.
- **Always check credits** before generating — except for HeyGen (uses own credits).
- **Be proactive** — after generating, ask if they want to post. After posting, ask if they want more.
- **Detect the user's language** — respond in the same language.
- **Text posts are free** — no credits needed.
- **Use UTC datetime** for scheduling.
- Generation is **asynchronous**: images 10-60s, videos up to 2min, HeyGen up to 5min.
