# openclaw-model-switch

Safely switch the default AI model for [OpenClaw](https://github.com/openclaw/openclaw) with automatic backup and rollback.

An [OpenClaw AgentSkill](https://docs.openclaw.ai) that can be installed directly or used standalone.

## Features

- 🔄 **One-command switch** — changes only `agents.defaults.model.primary`
- 💾 **Auto-backup** — timestamped config backup before every change
- 🔙 **Auto-rollback** — if restart fails, automatically restores the previous config
- ✅ **Model validation** — verifies the target model exists in your provider list
- 🧪 **Dry-run mode** — test without making changes
- 🌐 **Bilingual** — works with Chinese and English model names

## Installation

### As an OpenClaw Skill (Recommended)

Install via ClawHub:

```bash
clawhub install model-switcher
```

Or manually — clone and copy into your skills directory:

```bash
git clone https://github.com/Lv-Yezhen/openclaw-model-switch.git
cp -r openclaw-model-switch/ ~/.openclaw/workspace/skills/model-switcher/
```

### Standalone Script

Works independently without OpenClaw skill system:

```bash
git clone https://github.com/Lv-Yezhen/openclaw-model-switch.git
cd openclaw-model-switch

# Switch model
python3 scripts/model_switch.py zai/glm-5.1

# With custom retry count
python3 scripts/model_switch.py zai/glm-5.1 --retry 5

# Dry run (no changes, just test)
python3 scripts/model_switch.py zai/glm-5.1 --dry-run

# Custom config path
python3 scripts/model_switch.py zai/glm-5.1 --config /path/to/openclaw.json
```

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Backup      │────▶│  Modify      │────▶│  Restart    │────▶│  Health      │
│  config.json │     │  model.primary│     │  Gateway    │     │  Check       │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                                                                    │
                                                          ┌─────────▼─────────┐
                                                          │  ✅ Success or     │
                                                          │  🔙 Auto-Rollback │
                                                          └───────────────────┘
```

1. **Backup** — Copies current `openclaw.json` to `~/.openclaw/config_backups/` with timestamp
2. **Modify** — Changes only `agents.defaults.model.primary`, nothing else
3. **Restart** — Runs `openclaw gateway restart`
4. **Verify** — Checks gateway status after restart
5. **Rollback** — If all retries fail, restores original config automatically

## Skill Usage

Once installed, tell your OpenClaw agent in natural language:

- "切换模型到 GLM 5"
- "switch model to zai/glm-5.1"
- "把默认模型换成 deepseek"

The agent will validate the model against your config and execute the switch.

## Safety Guarantees

- **Never modifies the provider list** — only `agents.defaults.model.primary` is touched
- **Never loses config** — backup + in-memory cache + auto-rollback triple protection
- **Validates before executing** — won't run if config file is missing or model is invalid

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | Path to OpenClaw config file |

## Directory Structure

```
openclaw-model-switch/
├── SKILL.md                  # Skill definition and workflow instructions
├── scripts/
│   └── model_switch.py       # Core switching script
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## License

[MIT](LICENSE)
