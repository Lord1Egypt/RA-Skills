# Security & Trust

MemClaw is designed with user privacy and data security as top priorities.

## What the Plugin Does

- **Local Data Storage**: All memory data is stored in the local user data directory
- **Local Processing**: Based on advanced Cortex Memory technology, providing outstanding memory management capabilities with high performance and accuracy
- **Migration Safety**: Only reads existing OpenClaw memory files during migration

## What the Plugin Does NOT Do

- **No External Data Transmission**: Does NOT send data to external servers (all processing is local)
- **No API Key Leakage**: Does NOT transmit API keys to anywhere other than your configured LLM/embedding provider

## Data Storage Location

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/memclaw` |
| Windows | `%LOCALAPPDATA%\memclaw` |
| Linux | `~/.local/share/memclaw` |

## API Key Security

API keys are configured through OpenClaw plugin settings and are marked as sensitive fields. OpenClaw handles secure storage of these credentials.

**Best Practices:**
- Never share your `openclaw.json` configuration file publicly
- Use environment-specific API keys when possible
- Rotate API keys periodically according to your provider's recommendations
