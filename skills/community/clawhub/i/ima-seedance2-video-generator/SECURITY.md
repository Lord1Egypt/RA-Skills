# Security Disclosure: ima-seedance2-video-generator

## Purpose

This document explains endpoint usage, credential flow, and local data behavior for `ima-seedance2-video-generator`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | All requests |
| `imapi.liveme.com` | Upload-token request + binary upload | Only for local/non-HTTPS reference media inputs (image / video / audio) |
| `*.aliyuncs.com` / `*.esxscloud.com` | Presigned binary upload + media CDN delivery | Returned by upload-token API |
| User-provided remote media URLs | Reference-media probe, metadata extraction, and remote video cover-frame download | Only when the user passes `http(s)` image / video / audio URLs |

For HTTPS reference media URLs, the script passes URLs directly and does not need upload-token calls, but it may still fetch those URLs directly to validate media limits or to extract a video cover frame.

## Optional Environment Variables

The skill also reads several optional environment variables:

| Variable | Purpose | Security impact |
|---|---|---|
| `IMA_STDOUT_MODE` | Control stdout event-stream mode (`events` / `mixed` / `auto`) | Local output-only; no credential impact |
| `IMA_AUTO_CONSENT` | Auto-approve compliance verification prompts in non-interactive runs | Local behavior-only; no credential impact |
| `IMA_DEBUG` | Enable verbose debug logging | Local logging-only; no credential impact |

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local/non-HTTPS image, video, and audio uploads |
No API key is sent to presigned upload hosts (`aliyuncs/esxscloud`) during binary upload.

The script validates `task_type`, media counts, and reference-media metadata before task creation to reduce accidental credential/domain usage. User-provided remote media URLs are fetched without the API key.

## Upload Signing Constants

`APP_ID` and `APP_KEY` in script source are request-signing constants for upload APIs, not repository secrets.

## Cross-Skill Reads

This skill is self-contained for core API execution and does not require reading files from other skills.

## Model Scope

User-facing model names:

- **`Seedance 2.0`** (canonical: `ima-pro`) — Quality priority, 300~900s
- **`Seedance 2.0 Fast`** (canonical: `ima-pro-fast`) — Speed priority, 120~600s

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |
| System temp directory | Short-lived probe downloads and extracted video cover frames | Deleted after probe/upload flow completes |

No API key is written into repository files or the published pack.
