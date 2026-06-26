# Algernon HTTP Static Server

## Quick start

```bash
algernon -x -n . :8000
```

Or simply:

```bash
algernon 8000
```

Features:
- Directory listing: Yes
- Built-in Lua scripting
- Markdown rendering
- QUIC/HTTP2 support
- Live reload
- Built-in template engines (Amber, Pongo2)
- Auto-HTTPS with Let's Encrypt

## Install

- macOS: `brew install algernon`
- Go: `go install github.com/xyproto/algernon@latest`
- Download: Available from GitHub releases

## Flags

| Flag | Description |
|---|---|
| `-x` | Simple mode (no Lua, no caching) |
| `-n` | No headers (simpler output) |
| `--dir DIR` | Serve a specific directory |
| `--cors` | Enable CORS headers |
| `-q` | Quiet mode |

## Serve current directory without features

For pure static file serving without Lua/template processing:

```bash
algernon -x . :8000
```

Note: Algernon is a feature-rich web server that goes well beyond static file serving. The `-x` flag disables advanced features for simple static serving use cases.
