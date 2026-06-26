---
name: log-analyzer
description: >
  Securely analyze system and application logs with automatic sensitive data redaction.
  Supports OpenClaw gateway logs (journalctl), RAG indexing logs, and query logs.
  Finds errors, summarizes patterns, and searches across sources.
  Triggers on "check logs", "show errors", "analyze logs", "cosa è successo",
  "log errors", "any errors", "search logs".
  NOT for: reading arbitrary files, accessing logs outside whitelisted paths.
---

# Log Analyzer

Secure log analysis with automatic redaction of tokens, keys, and passwords.

## Usage

```bash
# Error summary across all sources (default)
python3 scripts/analyzer.py

# Specific source
python3 scripts/analyzer.py --source openclaw      # Gateway logs
python3 scripts/analyzer.py --source rag            # RAG indexing logs
python3 scripts/analyzer.py --source queries        # RAG query logs

# Search across all logs
python3 scripts/analyzer.py --search "OOM"

# Show only errors
python3 scripts/analyzer.py --source openclaw --errors

# More lines
python3 scripts/analyzer.py --source openclaw --last 500
```

## Log Sources

| Source | Type | Path |
|--------|------|------|
| `openclaw` / `gateway` | journalctl | `openclaw-gateway` unit |
| `rag` | file | `~/.local/share/local-rag/index-batch.log` |
| `queries` | file | `~/.local/share/local-rag/queries.log` |

## Security

- **ALLOWED_SOURCES only**: Cannot read arbitrary log files
- **Auto-redaction**: Tokens, API keys, passwords, age keys are replaced with `[REDACTED]`
- **Read-only**: Never modifies log files
- **No network**: All local
- **Safe in groups**: Sanitized output contains no secrets

## Error Detection

Automatically detects: `ERROR`, `FATAL`, `OOM`, `SIGKILL`, `FAILED`, `timeout`, `refused`, `denied`, `traceback`, `exception`, `segfault`
