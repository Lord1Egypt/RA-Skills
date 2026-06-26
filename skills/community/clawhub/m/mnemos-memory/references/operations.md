# Operations

Use this file when the user asks how Mnemos actually works in daily use, wants automation, or needs troubleshooting guidance.

## Automatic memory reality check

- Claude Code has the shipped automatic path today.
- The bundled hooks ingest high-signal user prompts and tool failures with `mnemos-cli autostore-hook`.
- The same hooks run `mnemos-cli consolidate` on `PreCompact` and `Stop`.
- Codex, Cursor, and generic MCP hosts do not get the same deterministic hook layer by default. They usually rely on:
  - the agent calling `mnemos_retrieve`, `mnemos_store`, and `mnemos_consolidate`
  - repo/user policy text such as `AGENTS.md`
  - host-specific automation added by the user

Do not hide this gap. If the user wants parity outside Claude Code, say so plainly.

Hard auto-capture remains host-dependent. Do not promise it for Codex, Cursor, OpenClaw, or generic MCP hosts unless verified hooks/extensions are actually installed.

## Storage guidance

- SQLite: the shipped persistent store and the recommended setup.
- `sqlite-vec` and FTS5 already cover semantic and full-text retrieval inside the same local database.

## Retrieval quality guidance

- Use a real embedding provider for production quality.
- Treat `simple` embeddings as development-only.
- If retrieval quality looks poor, check:
  - embedding provider choice
  - scope and `scope_id`
  - whether the expected SQLite database path is configured
  - whether the expected memories were ever ingested

## Inspection and troubleshooting

Start with:

```bash
mnemos-cli doctor
mnemos-cli stats
mnemos inspect <chunk-id>
```

Useful MCP tools:

- `mnemos_health`
- `mnemos_stats`
- `mnemos_inspect`
- `mnemos_list`

If setup is host-related, prefer the control plane:

```bash
mnemos ui
```
