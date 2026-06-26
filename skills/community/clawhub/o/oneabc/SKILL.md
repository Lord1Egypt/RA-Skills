---
name: oneabc
description: Access OpenAI-, Claude-, DeepSeek-, Sora-, Midjourney-, and Suno-compatible models through the oneabc.io API. Use when the user asks to call OneABC models from a local wrapper or list available models.
metadata:
  openclaw:
    emoji: "🔥"
    requires:
      bins: ["node"]
---

# OneABC

Use this skill when the user asks to access OneABC models through a local script wrapper.

## Required environment

Set one of these before use:

- `ONEABC_API_KEY`
- `OPENAI_API_KEY` (only if you intentionally mirror the same key there)

Optional:

- `ONEABC_BASE_URL` default: `https://api.oneabc.org`

## Commands

List models:

```bash
node scripts/oneabc.js models
```

Chat:

```bash
node scripts/oneabc.js chat gpt-4o "Hello"
```

Image:

```bash
node scripts/oneabc.js image "a product photo on white background"
```

Video:

```bash
node scripts/oneabc.js video "a shower head rotating in studio light"
```

Music:

```bash
node scripts/oneabc.js music "an upbeat product promo song"
```

## Notes

- Never hardcode API keys into the skill files.
- If the environment variable is missing, stop and report it.
