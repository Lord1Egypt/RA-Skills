# Security Disclosure: ima-voice-ai

## Purpose

This document describes endpoint usage and credential handling for `ima-voice-ai`.

## Network Endpoints

| Domain | Used For |
|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling |

This skill does not use any secondary upload domain.

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |

No credential is sent to other domains.

## Cross-Skill Access

None. This skill does not read files from other skills.

## Local Data

By default, this skill script does not require local preference/log files for runtime behavior.
