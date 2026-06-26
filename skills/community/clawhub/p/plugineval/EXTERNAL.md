# External Dependencies

This skill uses evaluation scripts that are part of the Nova OpenClaw infrastructure, not bundled with the skill.

## Included Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `skill-eval.py` | `~/.openclaw/workspace/scripts/` | Layer 1, 2, 3 evaluation |
| `vet-skill.sh` | `~/.openclaw/workspace/scripts/` | Combined security + quality |
| `clawdefender.sh` | `~/.openclaw/workspace/scripts/` | Security scanning |

## Installation

These scripts are automatically available when using the Nova OpenClaw workspace setup.

If running standalone:
1. Clone: https://github.com/Donmeusi/openclaw-config
2. Copy scripts from `scripts/` to your PATH
3. Ensure Python 3.9+ and dependencies are installed

## Migration Note

Version 2.0.0 will embed these scripts directly. This skill (v1.3.0) is a transitional release.

## LLM Judge

Layer 2 evaluation uses **local Ollama** with `gemma4:e4b` model. No external API calls.

```bash
# LLM Judge runs locally
ollama run gemma4:e4b --eval "{skill_content}"
```

**Privacy:** Skill content never leaves your machine.

---

**See Also:** `plugineval-core` (coming in v2.0.0) will be self-contained.
