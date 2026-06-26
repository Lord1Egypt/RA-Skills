# Troubleshooting

## Common Issues

### "API Key not found"

Set environment variable:
```bash
export MINIMAX_API_KEY="your-api-key"
```

Add to shell profile for persistence:
```bash
echo 'export MINIMAX_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### "uvx not found"

Install uvx:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "MCP server offline"

Check network and API key:
```bash
curl -H "Authorization: Bearer $MINIMAX_API_KEY" https://api.minimaxi.com/v1/models
```

### Webchat images don't work

**This is expected.** MiniMax-M2.7 doesn't accept image inputs natively.

**Solutions:**
- Send images via Telegram (bot saves locally)
- Use local file paths: `python3 scripts/understand_image.py /path/to/image.jpg "describe"`

### Timeout errors

Increase timeout in script or check network speed.

## Image Paths

| Path | Description |
|------|-------------|
| `~/.openclaw/media/inbound/` | Telegram image storage |
