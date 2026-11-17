---
name: image-handoff
description: Detect image generation requests and route them to the artist agent. Use when user asks to draw, generate, create, sketch, render, or visualize an image.
---

# Image Handoff Skill

## Purpose
Detect image generation requests and route them to the artist agent.

## Detection Patterns

**Explicit trigger:**
- `!img <prompt>` — immediate handoff, no confirmation

**Auto-detection (ask for confirmation):**
- "draw me...", "generate an image of...", "make a picture of..."
- "can you create an image...", "I want an image of..."
- "sketch...", "render...", "visualize..."

## Handoff Protocol

When explicit trigger or confirmed auto-detect:
1. Extract the prompt (everything after trigger word, or the full request)
2. Send to artist agent via `sessions_send` with context:
   - Original prompt
   - Any style preferences from memory
   - Request ID for tracking

3. Wait for artist agent response
4. Deliver image/result back to user

## Response Format to Artist

```
Image generation request from Deepak (明达):
Prompt: "a cat in space"
Preferences: sci-fi aesthetic, high contrast (from memory)
Request ID: img-2026-05-21-001
```

## Memory Tracking

Log to `memory/image-requests.md`:
- Request ID
- Prompt
- Model used
- Result (success/fail)
- User feedback

## Refusal

If request is ethically problematic, decline before handoff and explain why.
