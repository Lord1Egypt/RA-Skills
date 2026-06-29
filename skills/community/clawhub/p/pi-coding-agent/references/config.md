# Pi Configuration Reference

## settings.json

### Global Config

File: `~/.pi/agent/settings.json`

### Project Config

File: `.pi/settings.json` (overrides global)

### Main Settings

```json
{
  "model": "anthropic/claude-sonnet-4-20250514",
  "thinkingLevel": "medium",
  "theme": "dark",
  "compactThreshold": 0.8,
  "autoCompact": true,
  "steeringMode": "one-at-a-time",
  "followUpMode": "one-at-a-time",
  "transport": "auto",
  "toolExecution": "parallel",
  "enableInstallTelemetry": true,
  "npmCommand": ["mise", "exec", "node@20", "--", "npm"]
}
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Gemini API key |
| `PI_SKIP_VERSION_CHECK=1` | Skip startup version check |
| `PI_TELEMETRY=0` | Disable install/update telemetry |
| `PI_OFFLINE=1` | Disable all startup network operations |
| `PI_ALLOW_LOCKFILE_CHANGE=1` | Allow lockfile changes to be committed |

## Keybindings Customization

File: `~/.pi/agent/keybindings.json`

Overrides default keybindings.

## Common Command Reference

| Command | Description |
|---------|-------------|
| `/login` / `/logout` | OAuth provider authentication |
| `/model` | Switch model |
| `/scoped-models` | Configure Ctrl+P cycling models |
| `/settings` | Interactive settings |
| `/resume` | Browse and resume a previous session |
| `/new` | New session |
| `/name <n>` | Set session name |
| `/session` | Session details (file, ID, tokens, cost) |
| `/tree` | Session tree navigation |
| `/fork` | Fork a new session from a past message |
| `/clone` | Copy current branch to a new session |
| `/compact [prompt]` | Manual compaction with optional custom instructions |
| `/copy` | Copy last reply to clipboard |
| `/export [file]` | Export to HTML |
| `/share` | Upload to GitHub Gist for sharing |
| `/reload` | Reload extensions/skills/prompts/context |
| `/hotkeys` | Show all keyboard shortcuts |
| `/changelog` | Version history |
| `/quit` | Exit |

## Platform Notes

- Windows: [docs/windows.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/windows.md)
- Termux (Android): [docs/termux.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/termux.md)
- tmux: [docs/tmux.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/tmux.md)
- Terminal config: [docs/terminal-setup.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/terminal-setup.md)
- Shell aliases: [docs/shell-aliases.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/shell-aliases.md)