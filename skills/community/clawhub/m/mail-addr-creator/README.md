# OpenClaw version

This package is the OpenClaw-adapted version of the original ChatGPT skill.

## What changed

- Removed ChatGPT-only metadata file `agents/openai.yaml`
- Kept the reusable skill structure that OpenClaw supports: `SKILL.md`, `scripts/`, and `references/`
- Reworded instructions from ChatGPT/Codex-specific phrasing to OpenClaw usage
- Replaced Windows PowerShell examples with portable `bash` / `python3` examples
- Added OpenClaw install path notes

## Install

Project-local:

```bash
mkdir -p skills
cp -R cloudflare-mail-address-creator skills/
```

Global:

```bash
mkdir -p ~/.moltbot/skills
cp -R cloudflare-mail-address-creator ~/.moltbot/skills/
```

## Notes

OpenClaw skills are folder-based and centered on `SKILL.md`. Supporting scripts and docs can live alongside it.
