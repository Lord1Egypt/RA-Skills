# PixelDojo model catalog

Snapshot taken from `https://pixeldojo.ai/api/v1/models` on 2026-03-09.

PixelDojo is an AI creative platform that exposes multiple image and video models behind one subscription and API. Use this file for known-good model IDs, example picks, and sanity-checking requests. For the latest catalog at runtime, prefer:

```bash
bash ~/.openclaw/skills/pixeldojo/models.sh
```

## Summary

- Total models: 27
- Image models: 23
- Video models: 4

## Image models

| API ID | Name | Capabilities | Cost |
| --- | --- | --- | --- |
| `dreamina` | Dreamina 3.1 | text-to-image | 1 credit |
| `flux-1.1-pro` | Flux 1.1 Pro | text-to-image | 1 credit |
| `flux-1.1-pro-ultra` | Flux 1.1 Pro Ultra | text-to-image | 1.5 credits |
| `flux-2-dev` | Flux 2 Dev | text-to-image, image-to-image | 1 credit |
| `flux-2-flex` | Flux 2 Flex | text-to-image, image-to-image | 2 credits |
| `flux-2-klein-4b` | Flux 2 Klein 4B | text-to-image, image-to-image | 0.1 credits |
| `flux-2-klein-9b` | Flux 2 Klein 9B | text-to-image, image-to-image | 0.5 credits |
| `flux-2-max` | Flux 2 Max | text-to-image, image-to-image | 2 credits |
| `flux-2-pro` | Flux 2 Pro | text-to-image, image-to-image | 2 credits |
| `flux-dev` | Flux Dev | text-to-image | 1 credit |
| `flux-kontext-max` | Flux Kontext Max | text-to-image, image-to-image | 2 credits |
| `flux-kontext-pro` | Flux Kontext Pro | text-to-image, image-to-image | 1 credit |
| `flux-krea-dev` | Flux Krea Dev | text-to-image | 1 credit |
| `nano-banana-2` | Google Nano Banana 2 | text-to-image, image-to-image | 2 credits |
| `nano-banana-pro` | Google Nano Banana Pro | text-to-image, image-to-image | 3 credits |
| `p-image` | P-Image | text-to-image, image-to-image | 1 credit |
| `ponyxl-ponyrealism-v23` | Pony Realism | text-to-image, image-to-image, inpainting | 1 credit |
| `ponyxl-tponynai3-v7` | Pony NAI | text-to-image, image-to-image, inpainting | 1 credit |
| `qwen-image-2.0` | QWEN Image 2.0 | text-to-image, image-to-image | 1 credit |
| `qwen-image-2.0-pro` | QWEN Image 2.0 Pro | text-to-image, image-to-image | 2 credits |
| `wan-2.6-image` | WAN 2.6 Image | text-to-image, image-to-image | 1 credit |
| `wan-image` | WAN 2.2 Image | text-to-image | 1 credit |
| `z-image-turbo` | Z Image Turbo | text-to-image | 0.5 credits |

## Video models

| API ID | Name | Capabilities | Cost |
| --- | --- | --- | --- |
| `seedance-1.5` | Seedance 1.5 | text-to-video, image-to-video | 1.5 credits/sec |
| `wan-2.2-plus` | WAN 2.2 Plus | image-to-video | 10 credits |
| `wan-2.6-flash` | WAN 2.6 Flash | image-to-video | 1 credit/sec |
| `xai-video` | xAI Video | text-to-video, image-to-video | 2 credits/sec |

## Good example model picks

- Fast cheap image: `flux-2-klein-4b`
- Best general Flux image quality: `flux-2-max`
- Prompt adherence / typography: `nano-banana-2` or `nano-banana-pro`
- Image editing: `flux-kontext-pro`, `flux-kontext-max`, `qwen-image-2.0-pro`
- Cheap cinematic image: `wan-image`
- Text-to-video: `seedance-1.5`, `xai-video`
- Image-to-video only: `wan-2.6-flash`, `wan-2.2-plus`

## Refresh recipe

If the catalog changes, regenerate this reference from the live API response and keep SKILL.md concise. Do not duplicate long model lists in SKILL.md.
