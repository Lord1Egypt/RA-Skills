---
name: mac-multi-instance-deployment
description: Public-safe Mac multi-instance deployment skill for generic OpenClaw-style workspace layout, boundary notes, sample config, and pack validation.
version: 1.0.4
---

# Mac Multi-Instance Deployment / Mac 多实例部署

Keep a generic Mac multi-instance workspace public-safe.

## Checklist

- `main`: routing and shared docs
- `workbench`: active edits and tests
- `publish`: release bundles
- `archive`: snapshots and references
- `private`: secrets and runtime state
- Use placeholder paths in `config/local-multi-instance.example.env`
- Review `references/instances.md`
- Run `./validate_repo.sh`
- Run `./generate_public_pack.sh --dry-run`

## Guardrails

- Use generic labels only.
- Keep one workspace root per role.
- Keep private files out of public packs.
- Keep runtime state local.
