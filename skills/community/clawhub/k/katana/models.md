# Katana Model Catalogue

> **Production API uses `model_key` as the model ID parameter, not `public_model_name`. All IDs below are model_key values.**

> **Note:** This is a static snapshot synced from the live API reference at https://kat.imgnai.com/llms.txt. For the most current pricing and model availability, check the live endpoint.

Auto-generated from https://kat.imgnai.com/llms.txt — Last synced: 2026-06-08

Extracted from the imgnAI Katana API docs. Organised by type: text, image, video.

Reference price: $0.0052 per credit (Platinum Annual).

## Text / LLM Models

All text models use `POST /v1/chat/completions` (OpenAI-compatible).
Auth: `Authorization: Bearer <api_key>:<api_secret>`
Billing: pre-charge reserve, then refund/charge difference from actual usage. Minimum 0.1 credits.

| Model ID | Publisher | Context | Max Output | Input Types | Privacy | In (cr/$) | Out (cr/$) | Cache R / W | Legacy |
|---|---|---|---|---|---|---|---|---|---|---|
| `q-naifu-a3b` | imgnAI | 262144 | 262144 | text, image, file | Private | 38.5 / $0.20 | 240.4 / $1.25 | — | — |
| `claude-opus-4-8` | Anthropic | 1000000 | 128000 | text, image, file | Anonymized | 1000.0 / $5.20 | 5000.0 / $26.00 | 100.0 cr ($0.52) / 1250.0 cr ($6.50) | — |
| `claude-opus-4-8-fast` | Anthropic | 1000000 | 128000 | text, image, file | Anonymized | 2000.0 / $10.40 | 10000.0 / $52.00 | 200.0 cr ($1.04) / 2500.0 cr ($13.00) | — |
| `qwen3-7-max` | Qwen | 1000000 | 65536 | text | Anonymized | 264.5 / $1.38 | 793.3 / $4.13 | 52.9 cr ($0.2750) / 330.6 cr ($1.72) | — |
| `grok-build-0-1` | xAI | 256000 | not listed | text, image | Anonymized | 192.4 / $1.00 | 384.7 / $2.00 | 38.5 cr ($0.20) / — | — |
| `gemini-3-5-flash` | Google | 1048576 | 65536 | text, image, video, file, audio | Anonymized | 317.4 / $1.65 | 1903.9 / $9.90 | 31.8 cr ($0.1650) / 17.7 cr ($0.0917) | — |
| `grok-4-3` | xAI | 1000000 | not listed | text, image | Anonymized | 264.5 / $1.38 | 528.9 / $2.75 | 42.4 cr ($0.2200) / — | — |
| `qwen3-6-35b-a3b` | Qwen | 262144 | 262140 | text, image, video | Anonymized | 29.7 / $0.1540 | 211.6 / $1.10 | — | — |
| `qwen3-6-flash` | Qwen | 1000000 | 65536 | text, image, video | Anonymized | 39.7 / $0.2062 | 238.0 / $1.24 | 4.0 cr ($0.0206) / 49.6 cr ($0.2578) | — |
| `qwen3-6-max-preview` | Qwen | 262144 | 65536 | text | Anonymized | 220.0 / $1.14 | 1320.0 / $6.86 | 22.0 cr ($0.1144) / 275.0 cr ($1.43) | — |
| `deepseek-v4-flash` | DeepSeek | 1048576 | 384000 | text | Anonymized | 20.8 / $0.1081 | 41.6 / $0.2163 | 4.2 cr ($0.0217) / — | — |
| `deepseek-v4-pro` | DeepSeek | 1048576 | 384000 | text | Anonymized | 92.1 / $0.4785 | 184.1 / $0.9570 | 0.8 cr ($0.0040) / — | — |
| `gpt-5-5` | OpenAI | 1050000 | 128000 | file, image, text | Anonymized | 1057.7 / $5.50 | 6346.2 / $33.00 | 105.8 cr ($0.5500) / — | — |
| `kimi-k2-6-private` | MoonshotAI | 262144 | 262144 | text, image | E2EE Private | 230.6 / $1.20 | 973.1 / $5.06 | 78.3 cr ($0.4070) | — |
| `qwen3-coder-next-private` | Qwen | 262144 | 262144 | text | E2EE Private | 38.1 / $0.1980 | 253.9 / $1.32 | — | — |
| `glm-5-1-private` | Z.ai | 202752 | 202752 | text | E2EE Private | 256.0 / $1.33 | 888.5 / $4.62 | 127.0 cr ($0.6600) | — |
| `kimi-k2-6` | MoonshotAI | 262144 | 16384 | text, image | Anonymized | 144.7 / $0.7524 | 723.5 / $3.76 | 30.5 cr ($0.1584) / — | — |
| `mimo-v2-flash-private` | Xiaomi | 262144 | 262144 | text | E2EE Private | 21.2 / $0.1100 | 63.5 / $0.3300 | — | — |
| `claude-opus-4-7` | Anthropic | 1000000 | 128000 | text, image | Anonymized | 1057.7 / $5.50 | 5288.5 / $27.50 | 105.8 cr ($0.5500) / 1322.2 cr ($6.88) | — |
| `glm-5-1` | Z.ai | 202752 | 65535 | text | Anonymized | 207.4 / $1.08 | 651.6 / $3.39 | 38.5 cr ($0.2002) / — | — |
| `gemma-4-26b-a4b` | Google | 262144 | not listed | image, text, video | Anonymized | 12.7 / $0.0660 | 69.9 / $0.3630 | — | — |
| `gemma-4-31b` | Google | 262144 | 16384 | image, text, video | Anonymized | 25.4 / $0.1320 | 78.3 / $0.4070 | — | — |
| `qwen3-6-plus` | Qwen | 1000000 | 65536 | text, image, video | Anonymized | 68.8 / $0.3575 | 412.5 / $2.15 | 6.9 cr ($0.0358) / 86.0 cr ($0.4469) | — |
| `grok-4-20` | xAI | 2000000 | not listed | text, image, file | Anonymized | 264.5 / $1.38 | 528.9 / $2.75 | 42.4 cr ($0.2200) / — | — |
| `grok-4-20-multi-agent` | xAI | 2000000 | not listed | text, image, file | Anonymized | 423.1 / $2.20 | 1269.3 / $6.60 | 42.4 cr ($0.2200) / — | — |
| `minimax-m2-7` | MiniMax | 196608 | 131072 | text | Anonymized | 55.0 / $0.2860 | 253.9 / $1.32 | — | — |
| `gpt-5-4-mini` | OpenAI | 400000 | 128000 | file, image, text | Anonymized | 158.7 / $0.8250 | 952.0 / $4.95 | 15.9 cr ($0.0825) / — | — |
| `glm-5-turbo` | Z.ai | 202752 | 131072 | text | Anonymized | 253.9 / $1.32 | 846.2 / $4.40 | 50.8 cr ($0.2640) / — | — |
| `qwen3-5-27b-private` | Qwen | 262144 | 262144 | text, image, video | E2EE Private | 63.5 / $0.3300 | 507.7 / $2.64 | — | — |
| `gpt-5-4` | OpenAI | 1050000 | 128000 | text, image, file | Anonymized | 528.9 / $2.75 | 3173.1 / $16.50 | 52.9 cr ($0.2750) / — | — |
| `gemini-3-1-flash-lite-preview` | Google | 1048576 | 65536 | text, image, video, file, audio | Anonymized | 52.9 / $0.2750 | 317.4 / $1.65 | 5.3 cr ($0.0275) / 17.7 cr ($0.0917) | — |
| `qwen3-5-397b-a17b-private` | Qwen | 262144 | 262144 | text, image, video | E2EE Private | 116.4 / $0.6050 | 740.4 / $3.85 | 47.6 cr ($0.2475) | — |
| `minimax-m2-5-private` | MiniMax | 196608 | 196608 | text | E2EE Private | 42.4 / $0.2200 | 292.0 / $1.52 | 15.9 cr ($0.0825) | — |
| `gemini-3-1-pro-preview` | Google | 1048576 | 65536 | audio, file, image, text, video | Anonymized | 423.1 / $2.20 | 2538.5 / $13.20 | 42.4 cr ($0.2200) / 79.4 cr ($0.4125) | — |
| `claude-sonnet-4-6` | Anthropic | 1000000 | 128000 | text, image | Anonymized | 634.7 / $3.30 | 3173.1 / $16.50 | 63.5 cr ($0.3300) / 793.3 cr ($4.13) | — |
| `glm-5` | Z.ai | 202752 | not listed | text | Anonymized | 127.0 / $0.6600 | 406.2 / $2.11 | 25.4 cr ($0.1320) / — | — |
| `glm-5-private` | Z.ai | 202752 | 202752 | text | E2EE Private | 253.9 / $1.32 | 740.4 / $3.85 | 100.5 cr ($0.5225) | — |
| `claude-opus-4-6` | Anthropic | 1000000 | 128000 | text, image | Anonymized | 1057.7 / $5.50 | 5288.5 / $27.50 | 105.8 cr ($0.5500) / 1322.2 cr ($6.88) | — |
| `kimi-k2-5-private` | MoonshotAI | 262144 | 262144 | text, image | E2EE Private | 127.0 / $0.6600 | 634.7 / $3.30 | 46.6 cr ($0.2420) | — |
| `gemini-3-flash-preview` | Google | 1048576 | 65536 | text, image, file, audio, video | Anonymized | 105.8 / $0.5500 | 634.7 / $3.30 | 10.6 cr ($0.0550) / 17.7 cr ($0.0917) | — |
| `deepseek-v3-2-private` | DeepSeek | 163840 | 163840 | text | E2EE Private | 67.7 / $0.3520 | 101.6 / $0.5280 | 29.7 cr ($0.1540) | — |
| `qwen3-coder-480b-a35b-private` | Qwen | 262000 | 262000 | text | E2EE Private | 423.1 / $2.20 | 423.1 / $2.20 | — | — |
| `qwen3-vl-30b-a3b-instruct-private` | Qwen | 128000 | 128000 | text, image | E2EE Private | 42.4 / $0.2200 | 148.1 / $0.7700 | — | — |
| `claude-haiku-4-5` | Anthropic | 200000 | 64000 | image, text | Anonymized | 211.6 / $1.10 | 1057.7 / $5.50 | 21.2 cr ($0.1100) / 264.5 cr ($1.38) | — |
| `gemma-3-27b-private` | Google | 53920 | 53920 | text, image | E2EE Private | 23.3 / $0.1210 | 84.7 / $0.4400 | — | — |

## Image Models

All image models use `POST /v1/generation-requests` with `type: "image"`.
Required fields: `model`, `prompt`, `aspect_ratio`.

| Model ID | Cost (cr) | Aspects | Ref Images | Creator | Legacy | Notes |
|---|---|---|---|---|---|---|
| `pink-image` | 1 credit per image (~$0.0052) | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 3 | imgnAI | `pinkimage` | ref support, edit/ref |
| `gpt-image-2-max` | 28 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 10 | OpenAI | `gpt2maximage` | ref support, edit/ref |
| `nano-banana-2` | 32 | 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16 | 14 | Google | `nanobanana2` | ref support, edit/ref |
| `ani` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `fur` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `noob` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `gen` | 3 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | text prompts |
| `gpt-image-2` | 14 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 16 | OpenAI | `gpt2image` | ref support, edit/ref |
| `nano-banana-pro` | 28 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 8 | Google | `nanobananapro` | ref support, edit/ref |
| `seedream-4-5` | 12 | 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 4:7, 7:4, 5:2, 2:5 | 10 | ByteDance | `seedream45` | ref support, edit/ref, 4K |
| `seedream-5-0-lite` | 7 | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | 10 | ByteDance | `seedream5lite` | ref support, edit/ref |
| `synth` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `qwen-2-0` | 8 | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | 3 | Alibaba | `qwen2image` | ref support, edit/ref |
| `wan-2-7-image-pro` | 14 | 1:1, 3:4, 4:3, 1:8, 8:1, 9:16, 16:9, 21:9 | 9 | Alibaba | `wan27proimage` | ref support, edit/ref |
| `aura` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `flux-2-klein-9b` | 10 | 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 4:7, 7:4, 5:2, 2:5 | 4 | Black Forest Labs | `fluxklein9b` | ref support, edit/ref |
| `nano-banana` | 12 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9 | 6 | Google | `nanobanana` | ref support, requires image input, edit/ref |
| `pixel` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `flux-2-flex` | 28 | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9 | 8 | Black Forest Labs | `flux2flex` | ref support, edit/ref |
| `hyper-cgi` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | `hypercgi` | standard image generation |
| `imagine-art-1-5-pro` | 14 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:1, 1:3, 3:2, 2:3 | 0 | Imagine Art | `imagineart15` | 4K |
| `volt` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `wan-2-7-image` | 6 | 1:1, 3:4, 4:3, 1:8, 8:1, 9:16, 16:9, 21:9 | 9 | Alibaba | `wan27image` | ref support, edit/ref |
| `gpt-image-1-5` | 32 | 1:1 | 0 | OpenAI | `gptimage15` | text prompts |
| `flux-2-pro` | 8 | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9 | 4 | Black Forest Labs | `flux2pro` | ref support, edit/ref |
| `muse` | 3 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | text prompts |
| `gothic` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `z-image-base` | 7 | 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 4:7, 7:4, 5:2, 2:5 | 0 | Z.ai | `zimagebase` | text prompts |
| `z-image-turbo` | 4 | 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 4:7, 7:4, 5:2, 2:5 | 0 | Z.ai | `zimageturbo` | text prompts |
| `flux-2-klein-4b` | 4 | 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 4:7, 7:4, 5:2, 2:5 | 4 | Black Forest Labs | `fluxklein4b` | ref support, edit/ref |
| `rend` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `retro` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `neo` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | UHD |
| `pony` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `nai` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `flux-1-1-ultra` | 18 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 9:21, 2:1, 1:2 | 0 | Black Forest Labs | `flux1ultra` | text prompts |
| `glitch` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `qwen-image` | 8 | 1:1, 16:9, 9:16, 4:3, 3:4 | 0 | Alibaba Cloud | `qwenimage` | ⚠️ Legacy |
| `seedream-4` | 12 | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 | 10 | ByteDance | `seedream4` | ⚠️ Legacy, ref support, edit/ref, 4K |
| `wan-2-2-image` | 8 | 1:1, 16:9, 9:16, 4:3, 3:4, 21:9 | 0 | Alibaba Cloud | `wan22image` | ⚠️ Legacy |
| `flux1-d` | 3 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | Black Forest Labs | `flux1d` | text prompts |
| `qwen-image-edit` | 12 | 1:1, 16:9, 9:16, 4:3, 3:4 | 0 | Alibaba Cloud | `qwenedit` | ⚠️ Legacy, requires image input, edit/ref |
| `supra` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `evo` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | ⚠️ Legacy |
| `toon` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `wassie` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | standard image generation |
| `hyperx` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | — | ⚠️ Legacy |
| `flux-kontext-max` | 20 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 9:21, 2:1, 1:2 | 0 | Black Forest Labs | `kontextmax` | ⚠️ Legacy, requires image input, edit/ref |
| `furxl-classic` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | `furxl` | ⚠️ Legacy |
| `flux-kontext-pro` | 12 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 9:21, 2:1, 1:2 | 0 | Black Forest Labs | `kontextpro` | ⚠️ Legacy, requires image input, edit/ref |
| `supra-classic` | 2 | 1:1, 16:9, 21:9, 3:4, 9:16, 5:2, 4:3, 5:4, 4:5, 9:21, 4:7 | 0 | imgnAI | `supraclassic` | ⚠️ Legacy |

## Video Models

All video models use `POST /v1/generation-requests` with `type: "video"`.
Required fields: `model`, `prompt`, `duration_seconds`, `aspect_ratio`.

| Model ID | Duration Costs | Aspects | First Frame | Last Frame | Ref Images | Audio In | Audio Out | Video In | Custom Rules | Legacy |
|---|---|---|---|---|---|---|---|---|---|---|
| `seedance-2-0` | 5s: 200 cr; 10s: 375 cr; 15s: 550 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✓ | 7 | ✓ | ✓ | ✗ | Reference images cannot be combined with first-frame or last-frame inputs.; Audio input requires at least one referen... | `seedance2` |
| `seedance-2-0-480p` | 5s: 120 cr; 10s: 230 cr; 15s: 340 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✓ | 7 | ✓ | ✓ | ✗ | Reference images cannot be combined with first-frame or last-frame inputs.; Audio input requires at least one referen... | `seedance2480p` |
| `seedance-2-0-fast` | 5s: 120 cr; 10s: 230 cr; 15s: 340 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✓ | 7 | ✓ | ✓ | ✗ | Reference images cannot be combined with first-frame or last-frame inputs.; Audio input requires at least one referen... | `seedance2fast` |
| `ltx-2-3` | 5s: 20 cr; 10s: 40 cr; 15s: 60 cr; 20s: 80 cr | 16:9, 9:16, 1:1 | ✓ | ✓ | 0 | ✓ | ✓ | ✗ | Audio input can only be used with first-frame conditioning.; Video duration follows the selected audio duration. | `ltx23` |
| `gemini-omni` | 4s: 100 cr; 6s: 135 cr; 8s: 170 cr; 10s: 200 cr | 16:9, 9:16 | ✗ | ✗ | 5 | ✗ | ✓ | ✗ | none | `googlegeminiomnivideo` |
| `gemini-omni-v2v` | max 10s input video: 500 cr | 16:9, 9:16 | ✗ | ✗ | 5 | ✗ | ✓ | ✓ | Input video duration drives the output length. The listed length is the maximum accepted input video reference length... | `googlegeminiomniv2vvideo` |
| `happy-horse-1-0-1080p` | 5s: 300 cr; 10s: 600 cr; 15s: 900 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✗ | 9 | ✗ | ✓ | ✗ | Reference images cannot be combined with first-frame or last-frame inputs. | `happyhorse101080p` |
| `happy-horse-1-0-720p` | 5s: 150 cr; 10s: 300 cr; 15s: 450 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✗ | 9 | ✗ | ✓ | ✗ | Reference images cannot be combined with first-frame or last-frame inputs. | `happyhorse10720p` |
| `wan-2-7-1080p` | 5s: 130 cr; 10s: 260 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✓ | 5 | ✓ | ✓ | ✗ | Reference audio is interpreted as voice timbre when reference images are present.; Reference images cannot be combine... | `wan271080pvideo` |
| `wan-2-7-720p` | 5s: 90 cr; 10s: 180 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✓ | 5 | ✓ | ✓ | ✗ | Reference audio is interpreted as voice timbre when reference images are present.; Reference images cannot be combine... | `wan27720pvideo` |
| `kling-3-0-kling30pro` | 5s: 350 cr; 10s: 650 cr; 15s: 925 cr | 16:9, 9:16, 1:1 | ✓ | ✓ | 6 | ✗ | ✓ | ✗ | none | `kling30pro` |
| `kling-o3-4k` | 5s: 450 cr; 10s: 900 cr; 15s: 1350 cr | 16:9, 9:16, 1:1 | ✓ | ✓ | 6 | ✗ | ✓ | ✗ | none | `kling304k` |
| `kling-3-0-kling30` | 5s: 280 cr; 10s: 550 cr; 15s: 800 cr | 16:9, 9:16, 1:1 | ✓ | ✓ | 6 | ✗ | ✓ | ✗ | none | `kling30` |
| `veo3-1` | 4s: 380 cr; 8s: 750 cr | 16:9, 9:16 | ✓ | ✗ | 0 | ✗ | ✓ | ✗ | none | `veo3` |
| `veo3-1-fast` | 4s: 160 cr; 8s: 300 cr | 16:9, 9:16 | ✓ | ✗ | 0 | ✗ | ✓ | ✗ | none | `veo3fast` |
| `veo3-1-lite` | 8s: 140 cr | 16:9, 9:16 | ✓ | ✗ | 0 | ✗ | ✓ | ✗ | none | `veo3lite` |
| `seedance-pro` | 5s: 250 cr; 10s: 450 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `seedancepro` ⚠️ |
| `wan-2-5` | 5s: 220 cr; 10s: 400 cr | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 9:21 | ✓ | ✗ | 0 | ✗ | ✓ | ✗ | none | `wan25` ⚠️ |
| `hailuo-2-minimax` | 6s: 200 cr | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 9:21 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `hailuo2` ⚠️ |
| `kling-2-1-kling21` | 5s: 160 cr; 10s: 300 cr | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 9:21 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `kling21` ⚠️ |
| `kling-2-1-kling21loop` | 5s: 160 cr; 10s: 300 cr | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 9:21 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `kling21loop` ⚠️ |
| `seedance-lite` | 5s: 120 cr; 10s: 200 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `seedancelite` ⚠️ |
| `seedance-lite-loop` | 5s: 120 cr; 10s: 200 cr | 16:9, 9:16, 1:1, 4:3, 3:4 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `seedanceliteloop` ⚠️ |
| `kling-2-0` | 5s: 350 cr; 10s: 650 cr | 16:9, 9:16, 1:1 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `kling20` ⚠️ |
| `kling-1-6` | 5s: 130 cr; 10s: 250 cr | 16:9, 9:16, 1:1 | ✓ | ✗ | 0 | ✗ | ✗ | ✗ | none | `kling16` ⚠️ |