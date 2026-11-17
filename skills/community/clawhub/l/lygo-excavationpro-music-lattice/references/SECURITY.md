# lygo-excavationpro-music-lattice — SECURITY

**Signature:** Δ9Φ963-EXCAVATIONPRO-MUSIC-LATTICE-SECURITY-v1.0.0

## Trust boundary

Install only when `LYGO_STACK_ROOT` points to a **user-controlled, trusted** `lygo-protocol-stack` clone (for stack CLI).  
Public HTTPS links in `MUSIC_PORTAL.json` need no stack.

## Scope (skill scripts)

| Class | Allowed |
|-------|---------|
| **Read** | Skill mirror files; optional `LYGO_STACK_ROOT` music_catalog JSON; public HTTPS GETs for status |
| **Write** | None in skill scripts by default |
| **Network** | Optional read-only HEAD/GET of public portal + HF resolve URLs in `portal_status.py` |
| **Publish** | Never automatic — HF upload, git push, ClawHub publish require **explicit human request** |

## Human approval required

| Operation | Gate |
|-----------|------|
| Status / verify / map links | No consent |
| Local vault scan / encode / hub rebuild | Human OK (local disk) |
| HF stream publish | Explicit user request + HF token they control |
| Kernel egg plant | `lygo-kernel-egg-planter` + `--i-consent` |
| git push / Pages | Explicit user request |

## Prohibited

- Auto-posting music or links to social without user OK  
- Uploading masters/WAVs to third parties without consent  
- Putting secrets, tokens, or absolute private paths into eggs or skill JSON  
- Claiming “platform-proof” without distinguishing **public streams** vs **local masters**

## Content policy note

Public stream pack is steward-encoded 160kbps. Masters remain on steward disks. Agents must not redistribute full masters beyond what the steward already published.

## SkillSpector

See `references/SKILLSPECTOR_AUDIT.md`.
