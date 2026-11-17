# Magic Hour model catalogue

Source: https://docs.magichour.ai (checked 2026-08). Credits are charged per second of output video; failed jobs are refunded. Free tier: 400 credits on signup + 100/day.

## Video

| id | allowed durations (s) | credits/sec | max resolution | tier | pick it for |
|---|---|---|---|---|---|
| wan-2.2 | 3,4,5,6,7,8,9,10,15 | 24 | 1080p | free | default, quick drafts, product shots |
| ltx-2.3 | 1-10,15,20,25,30 | 24 | 1080p | free | long free clips, b-roll |
| minimax-h3 | 1-10,15,20,25,30 | 24 | 1080p | free | stylised / anime, long clips |
| seedance-1.5 | 4-12 | 30 | 1080p | paid | cheap quality bump |
| kling-2.6 | 5,10 | 36 | 1080p | paid | realistic people |
| kling-3.0 | 3-15 | 48 | 1080p | paid | best motion & physics per credit |
| veo3.1-lite | 4,6,8,16,24,32,40,48,56 | 48 | 1080p | paid | cinematic on a budget |
| veo3.1 | 4,6,8,16,24,32,40,48,56 | 96 | 1080p | paid | cinematic, prompt adherence |
| veo3.1-audio | 4,6,8,16,24,32,40,48,56 | 96 | 1080p | paid | same + generated sound (`--audio`) |
| sora-2 | 4,8,12,24,36,48,60 | 120 | 720p | paid | complex scenes, multi-shot |
| seedance-2.0-mini | 4-15 | 96 | 720p | paid | |
| seedance-2.0 | 4-15 | 120 | 720p | paid | |
| seedance-2.5 | 4-30 | 120 | 720p | paid | longest premium clips |

Example costs: wan-2.2 5s = 120; kling-3.0 10s = 480; veo3.1 8s = 768; sora-2 12s = 1440.

## Image

| id | notes |
|---|---|
| default | Magic Hour's balanced default |
| gpt-image-2 | best text rendering and instruction following |
| nano-banana-pro | photoreal, strong at edits/consistency |
| seedream-5-pro | high aesthetic quality |
| flux-2-klein | fast |
| z-image-turbo | fastest/cheapest |
| qwen-edit | image editing |

`aspect_ratio`: 16:9, 9:16, 1:1. `image_count`: 1-4.

## Other Magic Hour endpoints (not wrapped by this skill's scripts)

face swap, lip sync, talking photo, voice generation/cloning, image upscaler, background remover, auto subtitles, video-to-video. All available via the same SDK under `client.v1.*`; see https://docs.magichour.ai/api-reference.
