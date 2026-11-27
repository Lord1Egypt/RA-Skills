---
name: imagies
description: Use a self-hosted Imagies server to crop, resize, convert or tile still images, match text with CLIP, detect objects with YOLO, or generate images. Use when the user requests these operations on their Imagies instance over REST or MCP.
homepage: https://github.com/psyb0t/docker-imagies
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [curl]
      env: [IMAGIES_URL]
permissions:
  network: "Connect to the configured Imagies instance."
  shell: "Run curl for REST uploads and downloads."
  filesystem: "Read the requested input images and write the requested outputs."
---

# Imagies

## Security & safety

Send images, prompts and tokens only to the configured, trusted instance. Use HTTPS outside localhost. Staged files are shared by authenticated callers. Delete files only when requested.

## When to use

Use Imagies for still-image editing, CLIP matching, YOLO detection and image generation. Stage local inputs over REST before calling an MCP tool.

## When NOT to use

Use a video tool for timed edits and frame extraction. Use Imagies on the extracted stills.

## Usage

Upload with `POST /v1/images` and the raw image body. Keep the response's `id`.

| Tool | Arguments |
| --- | --- |
| `transform` | `spec` with `image_id` and crop, resize or format options |
| `montage` | `spec` with image IDs and grid options |
| `match` | `spec` with image IDs and text queries |
| `detect` | `spec` with image IDs and optional confidence threshold |
| `generate` | `model` from `GET /v1/models`, `prompt` and optional `size` |

Download results with `GET /v1/images/{image_id}`. Use `GET /v1/engines` to check which vision engines have local weights. Generation also requires an installed model.

See [setup and REST examples](references/setup.md).
