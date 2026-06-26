---
name: media-gen-vision-video
description: Generate and analyze images, and generate videos using OpenClaw's preferred Google media workflows. Use when the user asks to create, edit, inspect, compare, or describe images/screenshots, or to generate videos, especially when the task should follow the preferred Nano Banana 2 / Gemini image path, Gemini multimodal image understanding path, or Veo 3.1 video path.
---

# Media Generation, Vision, and Video

## Choose the right path

- **Image generation or editing**: use the preferred Nano Banana 2 / Gemini image workflow.
- **Image understanding / screenshot analysis**: use Gemini multimodal image understanding.
- **Video generation**: use Google Veo 3.1.

## Non-negotiables

- Prefer Google-native media models and official flows first.
- Preserve aspect ratio, resolution, style, and reference-image constraints.
- Do not guess image contents when a multimodal path is available.
- Do not claim video generation succeeded unless a real video file was produced.
- When delivering files, send the generated asset directly into the conversation when supported.
- For successful image or video generation, always deliver the actual media asset to the chat; do not stop at a summary or path when direct sending is available.

## Image generation and editing

- Use the preferred image tool path first.
- For edits, keep the user’s reference image identity intact unless explicitly asked to change it.
- If the user specifies size or ratio, honor it exactly when possible.
- If the task asks for multiple variants, generate a small set rather than one-by-one loops.

## Image understanding

- Use multimodal analysis for screenshots, photos, and UI inspection.
- Report only what is visible or strongly supported.
- Separate confirmed observations from inference.
- If the image is unreadable or only partially visible, say so plainly.

## Video generation

- Default to Veo 3.1.
- Prefer the official Gemini API workflow when possible.
- Save the final file with a stable filename before sharing it.
- If video output is not available in the current environment, say that clearly and identify the blocker.
- Do not substitute a still image or text summary for an actual video file unless the user accepts that fallback.

## Delivery and reporting

- Return the generated asset when available.
- If the user asks for a file, do not bury it in prose—attach or send it directly.
- Keep the response short: result, file/path if any, and blockers if any.
