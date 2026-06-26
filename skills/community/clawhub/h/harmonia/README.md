# harmonia — OpenClaw Skill

> Check PyTorch, Transformers, and CUDA compatibility in one command.

An [OpenClaw](https://github.com/openclaw/openclaw) skill that integrates [harmonia](https://github.com/ahmed-eladl/harmonia) into your AI agent. Ask your agent to diagnose ML dependency issues, check GPU/CUDA setup, or find compatible package versions.

## Install

```bash
clawhub install harmonia
```

Or manually: copy the `SKILL.md` into your OpenClaw workspace `skills/harmonia/` directory.

## What it does

Tell your OpenClaw agent things like:

- "Check my ML environment for issues"
- "What version of torchaudio works with torch 2.5.1?"
- "I'm getting a CUDA mismatch error"
- "Set up PyTorch for Python 3.11 with CUDA 12.1"
- "Show me the PyTorch compatibility matrix"

The agent runs `harmonia check`, `harmonia suggest`, `harmonia doctor`, or `harmonia matrix` and gives you actionable results.

## What harmonia detects

| Check | Details |
|---|---|
| OS / glibc | Distro, version, wheel compatibility |
| Python | Version, virtualenv, EOL warnings |
| GPU | Model, VRAM, count via nvidia-smi |
| CUDA | Driver ↔ toolkit ↔ torch CUDA mismatch |
| PyTorch | torch ↔ torchvision ↔ torchaudio lock |
| Transformers | torch min, accelerate, tokenizers |
| Known conflicts | Real-world bug patterns with fixes |

## Links

- **harmonia on PyPI**: [harmonia-ml](https://pypi.org/project/harmonia-ml/)
- **harmonia on GitHub**: [ahmed-eladl/harmonia](https://github.com/ahmed-eladl/harmonia)
- **OpenClaw**: [openclaw/openclaw](https://github.com/openclaw/openclaw)

## License

MIT
