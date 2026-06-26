---
name: UGC Factory
description: AI-powered video and content generation pipeline with script writing, TikTok automation, YouTube analysis, media library, avatars, and voice synthesis — built for AI agents.
author: MCF Agentic
version: 1.0.0
tags: [ugc, video, content, tiktok, youtube, ai-video, media, avatars, voices, automation]
pricing: x402 (USDC on Base)
gateway: https://gateway.mcfagentic.com
---

# UGC Factory

A complete AI content factory accessible via API. Generate video scripts, produce AI-generated videos with avatars and synthetic voices, analyze TikTok and YouTube content for viral patterns, manage a media library with auto B-roll sourcing, and schedule posts — all without a human in the loop. Your agent can go from idea to published content autonomously: generate a script, pick a voice and avatar, pull B-roll from Pexels or Pixabay, produce the video, and schedule it for posting.

## Authentication

All endpoints require x402 payment (USDC on Base L2). Send a request without payment to receive pricing info in the 402 response.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | /api/ugc/providers | $0.001 | List AI providers |
| GET | /api/ugc/costs | $0.001 | Provider cost breakdown |
| POST | /api/ugc/estimate-cost | $0.01 | Estimate cost for video job |
| GET | /api/ugc/voices | $0.001 | List AI voices |
| GET | /api/ugc/avatars | $0.001 | List avatars |
| POST | /api/ugc/scripts/generate | $0.10 | AI script generation |
| GET | /api/ugc/jobs | $0.001 | List video pipeline jobs |
| POST | /api/ugc/jobs | $0.25 | Create video generation job |
| GET | /api/ugc/tiktok/niches | $0.001 | List TikTok niches |
| POST | /api/ugc/tiktok/analyze-video | $0.05 | AI TikTok video analysis |
| POST | /api/ugc/tiktok/analyze-url | $0.05 | AI TikTok URL analysis |
| GET | /api/ugc/tiktok/templates | $0.001 | List TikTok templates |
| POST | /api/ugc/tiktok/templates | $0.01 | Create TikTok template |
| GET | /api/ugc/tiktok/automation | $0.001 | List TikTok automation rules |
| POST | /api/ugc/tiktok/automation | $0.01 | Create TikTok automation rule |
| GET | /api/ugc/tiktok/posts | $0.001 | List TikTok posts |
| POST | /api/ugc/tiktok/posts | $0.01 | Create TikTok post |
| POST | /api/ugc/tiktok/schedule | $0.01 | Schedule TikTok content |
| GET | /api/ugc/tiktok/generated | $0.001 | List AI-generated TikTok content |
| GET | /api/ugc/media | $0.001 | List media library |
| POST | /api/ugc/media/upload | $0.01 | Upload media asset |
| POST | /api/ugc/media/fetch/pexels | $0.01 | Fetch from Pexels |
| POST | /api/ugc/media/fetch/pixabay | $0.01 | Fetch from Pixabay |
| POST | /api/ugc/media/fetch/youtube | $0.01 | Fetch from YouTube |
| POST | /api/ugc/media/auto-broll | $0.05 | Auto-fetch B-roll footage |
| POST | /api/ugc/media/:id/audit | $0.05 | AI media quality audit |
| POST | /api/ugc/media/:id/strip-watermark | $0.05 | AI watermark removal |
| GET | /api/ugc/prompt-presets | $0.001 | List prompt presets |
| POST | /api/ugc/prompt-presets | $0.01 | Create prompt preset |
| POST | /api/ugc/suggest-prompts | $0.05 | AI prompt suggestions |
| POST | /api/ugc/youtube/analyze | $0.10 | AI YouTube channel analysis |
| GET | /api/ugc/youtube/analyses | $0.001 | List YouTube analyses |
| POST | /api/ugc/youtube/generate-scripts | $0.10 | AI scripts from YouTube analysis |
