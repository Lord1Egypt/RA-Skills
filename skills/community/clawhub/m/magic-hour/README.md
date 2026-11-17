# Magic Hour skill for OpenClaw (ClawHub)

Teaches an OpenClaw agent to generate AI video and images with [Magic Hour](https://magichour.ai): text-to-video, image-to-video and image generation across Sora 2, Veo 3.1, Kling 3.0, WAN 2.2, LTX 2.3, MiniMax, Seedance, GPT-image, Nano Banana Pro and more, with one API key.

## Zero-install alternative

Magic Hour also runs a hosted MCP server at `https://mcp.magichour.ai/` (docs: https://magichour.ai/mcp) - attach it to any MCP-capable agent with `Authorization: Bearer $MAGIC_HOUR_API_KEY`. This skill covers that in SKILL.md and ships scripts for agents without MCP.

## Install

```bash
npx clawhub@latest install magic-hour
pip install magic_hour
export MAGIC_HOUR_API_KEY=mhk_...   # free key: https://magichour.ai/developer
```

## Quickstart (scripts work standalone too)

```bash
S=skills/magic-hour/scripts
python3 $S/text_to_video.py "a corgi surfing at golden hour" --model wan-2.2 --duration 5 --download-dir out
python3 $S/image_to_video.py photo.png "slow push-in, wind in hair" --model kling-3.0 --resolution 720p
python3 $S/generate_image.py "isometric cozy coffee shop" --model nano-banana-pro --count 2 --aspect-ratio 1:1
python3 $S/status.py <project_id> --kind video --wait
# each prints: {"project_id": "...", "status": "complete", "url": "https://...", "credits_charged": 120, ...}
```

## Models

| Video | Credits/sec | Notes |
|---|---|---|
| wan-2.2, ltx-2.3, minimax-h3 | 24 | free tier |
| seedance-1.5 / kling-2.6 / kling-3.0 | 30 / 36 / 48 | |
| veo3.1-lite / veo3.1 / veo3.1-audio | 48 / 96 / 96 | |
| sora-2, seedance-2.x | 120 | 720p max |

Image: default, gpt-image-2, nano-banana-pro, seedream-5-pro, flux-2-klein, z-image-turbo, qwen-edit. Full table: [references/models.md](references/models.md).

## Layout

- `SKILL.md` - agent instructions (frontmatter gates on `MAGIC_HOUR_API_KEY`, `python3`, `magic_hour`)
- `scripts/` - argparse CLIs printing JSON
- `references/` - raw HTTP API + model catalogue
- `tests/` - offline pytest (SDK mocked): `uv run --with pytest --with magic_hour pytest`

## Links

[Magic Hour docs](https://docs.magichour.ai) - [langchain-magic-hour](https://pypi.org/project/langchain-magic-hour/) - [llama-index-tools-magic-hour](https://pypi.org/project/llama-index-tools-magic-hour/) - [magic-hour-ai-provider](https://www.npmjs.com/package/magic-hour-ai-provider) - [Magic Hour hosted MCP](https://magichour.ai/mcp)

MIT (and MIT-0 on ClawHub).
