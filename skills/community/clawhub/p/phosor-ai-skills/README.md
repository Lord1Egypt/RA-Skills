# Phosor AI — Agent Skill

**Skill version 1.4.1** · API v1.3.0 · updated 2026-11-15

Two version numbers, on purpose: the skill version tracks this package
(commands, docs, the bundled client), the API version tracks the gateway
contract. A skill release that only rewords docs or fixes the client does not
move the API version, and a gateway change does not force a skill release.

Verify what you installed: `python3 scripts/phosor_client.py --version`

## Quick Start

```bash
export PHOSOR_API_KEY="your-key"

# MiniMax H3 Standard — Text-to-Video
python3 scripts/phosor_client.py submit "A cat walking on a beach" \
  --model minimax/h3/text-to-video --resolution-tier 480p --aspect 16:9 --duration 5

# MiniMax H3 Turbo — same input shape, faster variant
python3 scripts/phosor_client.py submit "A cat walking on a beach" \
  --model minimax/h3/text-to-video/turbo --resolution-tier 480p --aspect 16:9 --duration 5

# MiniMax H3 Image-to-Video (two-step: upload then submit)
python3 scripts/phosor_client.py upload-image photo.jpg
python3 scripts/phosor_client.py submit "The scene comes alive" \
  --model minimax/h3/image-to-video --image-url "images/img-xxx.jpg" \
  --resolution-tier 480p --aspect 16:9 --duration 5

# Choose Turbo for the same image-to-video mode
python3 scripts/phosor_client.py submit "The scene comes alive" \
  --model minimax/h3/image-to-video/turbo --image-url "images/img-xxx.jpg" \
  --resolution-tier 480p --aspect 16:9 --duration 5

# LLM chat with Qwen3.8 27B (synchronous, OpenAI-compatible; --stream for live text)
python3 scripts/phosor_client.py chat "Explain recursion in one paragraph." --max-tokens 300

# Check status / get result
python3 scripts/phosor_client.py status <request_id>
python3 scripts/phosor_client.py result <request_id>

# LoRA Upload (custom pre-trained)
python3 scripts/phosor_client.py upload-lora high_noise.safetensors low_noise.safetensors

python3 scripts/phosor_client.py save-lora <lora_id>

# Image Studio: AI product photography (secondary product surface, same API key)
python3 scripts/phosor_client.py upload-image product.jpg
python3 scripts/phosor_client.py studio-suite --image-url "<s3_url from upload>" \
  --layout-types "white_background,lifestyle_scene" --count-per-type 2
python3 scripts/phosor_client.py studio-status <job_id>
```

See [SKILL.md](SKILL.md#image-studio-product--model-photography) for the full Image Studio quick start (clothing/model suite, one-off edits like remove-bg/inpaint/translate).

For reference-to-video, use `minimax/h3/reference-to-video` or
`minimax/h3/reference-to-video/turbo` with one or more reference image/video inputs;
the full H3 mode table and limits are in [SKILL.md](SKILL.md#h3-model-map).

## Requirements

- Python 3.7+ (stdlib only, no pip install needed)
- `PHOSOR_API_KEY` environment variable

## Commands

Run `python3 scripts/phosor_client.py --help` for the available commands, including saved-task recovery.

## Links

- [Phosor AI](https://phosor.ai)
- [API Documentation](https://docs.phosor.ai)


## Price and model coverage

The package includes GPT Image 2 pricing, LTX 2.3 discovery/submit guidance and Qwen3.8 27B LLM chat.
See `SKILL.md` and `references/api.md` for units and tier qualifications.
Model API, Image Studio and Drama have separate availability and billing contracts.
A configured rate is not a promise that the corresponding model is open.
Check the version inside your downloaded package. Website and registry release availability may differ.

## Recover saved task records

After upgrading or changing API keys, run `pending-sources` to list saved task files.
Use `import-pending <file>` to check access with the current key and import accessible
records. Original files are preserved. This operation only queries task status;
it does not submit generation jobs. Failed access checks are reported separately.

Reference URL flags accept a JSON array as well as legacy comma-separated values. Use JSON when a URL contains a comma. The `list` command returns the task-ID mapping directly.
