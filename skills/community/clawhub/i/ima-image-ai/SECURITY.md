# Security Disclosure: ima-image-ai

## Purpose

This document explains endpoint usage, credential flow, and local data behavior for `ima-image-ai`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | All requests |
| `imapi.liveme.com` | Upload-token request for local image inputs | Only when `image_to_image` includes local files |
| `*.aliyuncs.com` / `*.esxscloud.com` | Presigned binary upload + media CDN delivery | Returned by upload-token API |

For remote HTTPS images, the script can pass URLs directly without upload-token calls.

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local image uploads |

No API key is sent to presigned upload hosts during binary upload.

## Cross-Skill Reads

This skill runs standalone.
If `ima-knowledge-ai` is installed, the agent may optionally read:

- `~/.openclaw/skills/ima-knowledge-ai/references/*`

for workflow and visual-consistency guidance only.

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |

No API key is written into repository files.
