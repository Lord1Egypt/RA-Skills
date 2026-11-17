# TOOLS.md - Local Notes

> _On current OpenClaw a workspace `TOOLS.md` is not loaded at startup (`openclaw doctor --fix` folds one into `AGENTS.md`). Put these notes in the `## Tools` section of `AGENTS.md`; this file shows what belongs there._

> _Template. The real file is infrastructure-dense (hostnames, ports, SSH recipes, service inventories) and can't ship. Its job: skills define HOW tools work; this file holds what's unique to YOUR setup. Sanitized excerpts from the real one live in `docs/war-stories.md` — that's what this file's entries actually look like after months of real use._

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → XXX.XXX.X.XXX, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## What the real file grows into (three months in)

Not just nicknames — operational memory. The entries that earn their place are the ones written the day something bit you:

- **Tool quirks with reproduction steps** — "do not call `start` then `open`; `open` auto-starts and you get the double-window bug"
- **Environment landmines** — which hosts lack which binaries, what needs root, what the agent's shell can't see that yours can
- **Stable-path patterns** — symlink dirs that survive version bumps so systemd units never point at a versioned path
- **Things deliberately NOT touched** — services that self-regenerate their own config, flagged rather than hand-edited

Each entry should answer: "what will future-me waste 20 minutes rediscovering?" Write it the same day. This file is the cheapest insurance in the whole workspace.
