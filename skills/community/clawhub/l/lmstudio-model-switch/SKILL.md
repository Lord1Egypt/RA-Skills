# lmstudio-model-switch

**Fast model switching between LM Studio local and Kimi API for OpenClaw.**

Switch your agent's AI model on-the-fly between local (LM Studio) and cloud (Kimi API) providers with a single command.

---

## Installation

```bash
# Clone to your OpenClaw skills directory
git clone https://github.com/yourusername/lmstudio-model-switch \
  ~/.openclaw/workspace/skills/lmstudio-model-switch

# Or manually copy
cp -r lmstudio-model-switch ~/.openclaw/workspace/skills/
```

---

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/switch-model status` | Show current model and available providers |
| `/switch-model local` | Switch to LM Studio (Qwen 3.5 9B default) |
| `/switch-model local <model>` | Switch to specific local model |
| `/switch-model api` | Switch to Kimi K2.5 API |
| `/switch-model kimi` | Alias for `/switch-model api` |

### Examples

```bash
# Check current status
/switch-model status

# Switch to local LM Studio
/switch-model local

# Switch to specific model
/switch-model local mistral-small-24b

# Switch to Kimi API
/switch-model api
```

---

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "lmstudio-model-switch": {
      "enabled": true,
      "config": {
        "local": {
          "baseUrl": "http://127.0.0.1:1234/v1",
          "defaultModel": "qwen/qwen3.5-9b"
        },
        "api": {
          "provider": "kimi-coding",
          "model": "k2p5"
        }
      }
    }
  }
}
```

---

## How It Works

1. **Backup**: Creates timestamped backup of `openclaw.json`
2. **Edit**: Modifies `"primary"` model in agents.defaults
3. **Verify**: Validates JSON syntax
4. **Restart**: Restarts OpenClaw gateway service
5. **Confirm**: Reports new active model

---

## Use Cases

### Privacy-First Work
Use **local** when handling:
- Authentication tokens
- Passwords or credentials
- Sensitive personal data
- Proprietary code

### Quality-First Work
Use **API** when needing:
- Maximum reasoning capability
- Very long contexts (>100k tokens)
- Best-in-class performance
- Cloud reliability

### VRAM Management
Switch to **API** when:
- GPU memory is low (<6GB free)
- Running other GPU-intensive tasks
- LM Studio is restarting

---

## Requirements

- OpenClaw ≥ 2026.3.12
- LM Studio running on port 1234 (for local mode)
- Kimi API key configured (for API mode)
- systemd (for service restart)

---

## Troubleshooting

### "LM Studio not responding"
```bash
# Check if LM Studio is running
curl http://127.0.0.1:1234/api/v0/models

# Restart LM Studio if needed
killall lmstudio; sleep 2; lmstudio &
```

### "Switch failed"
- Check JSON syntax: `python3 -m json.tool ~/.openclaw/openclaw.json`
- Restore from backup: `cp ~/.openclaw/openclaw.json.bak.* ~/.openclaw/openclaw.json`

### "Gateway won't restart"
```bash
# Check service status
systemctl --user status openclaw-gateway

# Manual restart
systemctl --user restart openclaw-gateway
```

---

## Author

**WarMech** - OpenClaw Community

## License

MIT

---

## Changelog

**2026-03-14** - v1.0.0
- Initial release
- Support for local/API switching
- Backup/restore functionality
- systemd integration
