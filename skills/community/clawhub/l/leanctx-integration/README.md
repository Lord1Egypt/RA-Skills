# LeanContext Integration for OpenClaw

LeanContext integration layer that automatically compresses tool outputs to reduce token usage by 60-99%.

## Installation

```bash
openclaw skills install leanctx-integration
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "leanctx": {
      "enabled": true,
      "compression": {
        "threshold": 100,
        "languages": ["ts", "js", "py", "svelte", "go", "rs"]
      },
      "cache": {
        "enabled": true,
        "maxSize": "100MB"
      },
      "exclude": {
        "paths": ["node_modules", ".git", "dist"],
        "commands": ["cat", "echo"]
      }
    }
  }
}
```

## Features

- **File Read Compression**: AST-aware compression for code files
- **Shell Output Compression**: Pattern matching for common commands
- **Session Caching**: Re-reads cost ~13 tokens
- **Metrics Dashboard**: Real-time token savings tracking

## Usage

Once installed, LeanContext automatically intercepts:
- `read` tool calls → Compressed file content
- `exec` tool calls → Compressed shell output

No code changes required - works transparently!

## Metrics

Check your session savings:
```bash
openclaw skills run leanctx-integration --metrics
```

Output:
```
SESSION v287 42 min active
  Tool calls      847
  Tokens saved    412,830
  Cache hits      73%
  Avg compression 91.4%
  Est. cost saved $1.24
```
