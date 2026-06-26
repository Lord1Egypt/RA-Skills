---
name: openclaw-self-update
description: Update OpenClaw to the latest version. Use when asked to "update yourself", "upgrade openclaw", "check for updates", or "update to latest version". Handles npm-installed OpenClaw instances.
---

# OpenClaw Self-Update

Update OpenClaw to the latest version via npm.

## Quick Update

```bash
# Check versions
openclaw --version                    # Current
npm show openclaw version             # Latest

# Update
npm install -g openclaw@latest

# Restart gateway
openclaw gateway restart

# Verify
openclaw --version
```

## Script

For automated updates with version checking:

```bash
bash {baseDir}/scripts/update.sh
```

The script will:
1. Check if update is available
2. Install latest version via npm
3. Restart the gateway
4. Show changelog summary

## Manual Steps

If the script fails:

```bash
# 1. Stop gateway
openclaw gateway stop

# 2. Update npm package
npm install -g openclaw@latest

# 3. Start gateway
openclaw gateway start

# 4. Verify
openclaw --version
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Use `sudo npm install -g openclaw@latest` |
| Gateway won't restart | Run `openclaw gateway stop` then `openclaw gateway start` |
| npm not found | Ensure Node.js is installed and in PATH |

## Notes

- `openclaw update` only works for git installs
- npm installs require `npm install -g openclaw@latest`
- Always restart gateway after update for changes to take effect
