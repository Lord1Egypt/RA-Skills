---
name: inflyu
description: AI influencer image and video generation for your agent — persona content, studio reels and carousels, and AI video and image editing, through Inflyu's hosted MCP server.
version: 1.0.0
license: MIT-0
homepage: https://inflyu.com/inflyu-mcp
---

# Inflyu

Inflyu is an AI influencer studio. This skill connects your agent to Inflyu's hosted MCP server so it can
generate persona images and reels, run studio generations, and edit images and videos in the user's own
Inflyu account.

## Setup

1. Add the server: `openclaw mcp add inflyu --url https://inflyu.com/api/mcp --transport streamable-http`
2. Sign in: choose **Sign in** next to the Inflyu server in Settings → MCP, or run `openclaw mcp login inflyu`,
   then approve access in the browser. The connection uses OAuth; no API key or secret goes in this skill.

Setup guide: https://inflyu.com/inflyu-mcp

## What it can do

- List, create and update the user's AI influencers, and generate persona-aware content for them.
- Generate studio images, reels, stories and carousels from a prompt.
- Edit images (restyle, relight, background swap, upscale, object edits).
- Edit short videos (swap, restyle, erase an object, extend, lip-sync, captions, voiceover) and poll the job.

## Hard rules

- **Spend only after an explicit yes.** Every generation and edit spends the user's Inflyu credits,
  including the 20 free starter credits. Quote the credit cost first (`video_editor_tools` lists costs)
  and wait for the user to confirm before calling any tool that spends.
- **No impersonation.** Never use `clone_influencer_run`, a person swap or a face swap to imitate a real
  person or to mislead anyone about who appears in an image or video.
- **No sexual or explicit content.** Requests like that are refused before any credit is spent.
- **Inflyu does not post to social platforms.** Don't tell the user that content was or will be published.

## Support

support@inflyu.com · Privacy: https://inflyu.com/privacy · Terms: https://inflyu.com/terms
