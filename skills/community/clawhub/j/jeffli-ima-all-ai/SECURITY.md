# Security Disclosure: ima-all-ai

## Purpose

This document explains endpoint usage, credential flow, and local data behavior for `ima-all-ai`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | All requests |
| `imapi.liveme.com` | Upload-token request for local image inputs | Only image/video tasks with local image paths |
| `*.aliyuncs.com` / `*.esxscloud.com` | Presigned binary upload + media CDN delivery | Returned by upload-token API |

For remote image URLs (`http(s)://...`), the script passes URLs directly and does not need upload-token calls.

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local image uploads |

No API key is sent to presigned upload hosts (`aliyuncs/esxscloud`) during binary upload.

## Input Safety Guards

The script validates task/image compatibility before task creation:

- `text_to_image`, `text_to_video`, `text_to_music`, `text_to_speech`: no input images
- `image_to_image`, `image_to_video`, `reference_image_to_video`: at least 1 image
- `first_last_frame_to_video`: exactly 2 images

## Upload Signing Constants

`APP_ID` and `APP_KEY` in script source are upload-signing constants (not repository secrets).

## Cross-Skill Reads

This skill is self-contained for core API execution.
If `ima-knowledge-ai` is installed, the agent may optionally read:

- `~/.openclaw/skills/ima-knowledge-ai/references/*`

for workflow decomposition, visual-consistency, and mode-selection guidance only.

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |

No API key is written into repository files.
