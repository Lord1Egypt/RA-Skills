---
name: lemgen-ai-design
description: Search 4,500+ curated AI image and video prompts, enhance prompts, and generate with LemGen from OpenClaw.
---

# LemGen AI Design Skill

LemGen AI Design turns OpenClaw into a practical AI image and video creative
assistant. It connects OpenClaw to the LemGen MCP server so agents can search a
curated prompt gallery, inspect real image/video examples, improve prompts, and
optionally generate images or videos with LemGen.

Use this skill when the user asks for:

- AI image prompt examples for GPT Image, Nano Banana, Midjourney, or Seedream;
- AI video prompt examples for Seedance, Veo, Kling, Runway, or Wan;
- prompt engineering, prompt translation, prompt polish, or creative direction;
- visual reference research before generation;
- image generation or video generation through LemGen.

Source repository: https://github.com/aithink001/lemgen-ai-design-mcp

Prompt gallery: https://lemgen.org

Keywords: OpenClaw skill, MCP server, AI image prompts, AI video prompts,
prompt engineering, GPT Image prompts, Nano Banana prompts, Seedance prompts,
Midjourney prompts, LemGen.

## Workflow

1. Start with `search_gallery` when the idea is vague or the user wants examples.
2. Show concise search results with preview URLs, model names, and why each result is useful.
3. Use `get_inspiration` for a selected gallery item before copying or adapting it.
4. Use `enhance_prompt` or `prompt_tools` to translate, polish, or expand the final prompt.
5. Ask for explicit confirmation before calling `generate_image`.
6. Always confirm before calling `generate_video`; video jobs are slower and more expensive.

When the user writes in Chinese, Japanese, Korean, Spanish, French, German,
Portuguese, or another supported language, reply in that language while keeping
model names and API parameters in English.

## Tools

- `search_gallery`: free prompt search.
- `get_inspiration`: full prompt and metadata.
- `enhance_prompt`: local prompt expansion.
- `list_models`: model capabilities.
- `prompt_tools`: translate, polish, improve.
- `manage_preferences`: local user preferences.
- `generate_image`: LemGen image generation, requires `LEMGEN_API_TOKEN`.
- `generate_video`: LemGen video generation, requires `LEMGEN_API_TOKEN`.

## Recommended Prompts

Good OpenClaw requests for this skill:

- "Find 10 cinematic Seedance prompts for a product launch video."
- "Turn this short idea into a GPT Image prompt and show reference examples first."
- "Translate this Midjourney prompt into Japanese and make it more commercial."
- "Search for Nano Banana logo prompt examples, then create a better version."
- "Use LemGen to generate after I approve the final prompt."

## Setup For OpenClaw

```json
{
  "mcpServers": {
    "lemgen": {
      "command": "npx",
      "args": ["-y", "github:aithink001/lemgen-ai-design-mcp"],
      "env": {
        "LEMGEN_API_TOKEN": "sk_..."
      }
    }
  }
}
```

Create an API key at `https://lemgen.org`.

Free search, inspiration, prompt enhancement, model guidance, and translation
tools work without a LemGen token. Generation tools require `LEMGEN_API_TOKEN`.

## Safety And Cost Rules

- Do not generate images or videos until the user approves the final prompt.
- Do not retry failed video jobs repeatedly; check LemGen generation history first.
- Do not expose `LEMGEN_API_TOKEN` in chat, logs, screenshots, or shared configs.
- For brand, celebrity, political, or regulated-industry requests, keep prompts
  factual and avoid misleading claims.
- For copyrighted characters or logos, explain that results should be used only
  when the user has the right to use those assets.

## Troubleshooting

See `references/troubleshooting.md` for token setup, empty search results, and
video timeout guidance.
