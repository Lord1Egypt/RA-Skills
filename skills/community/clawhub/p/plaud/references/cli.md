# Plaud CLI Reference

## Install

```bash
npm install -g @plaud-ai/cli@latest
```

## Auth

```bash
plaud login
plaud me
plaud logout
```

The CLI stores tokens at `~/.plaud/tokens.json`. Plaud MCP uses a separate token file, commonly `~/.plaud/tokens-mcp.json`.

## Browse

```bash
plaud files
plaud files --page 1 --page-size 20
plaud recent
plaud recent --days 30
plaud today
```

## Search

```bash
plaud search "keyword"
plaud search "weekly" --from 2026-04-01 --to 2026-04-30
plaud search "onboarding" --max 10
```

## Read one recording

```bash
plaud file <id>
plaud summary <id>
plaud transcript <id>
plaud audio <id>
```

## Export

```bash
plaud summary <id> -o summary.md
plaud transcript <id> -o transcript.txt
```

## Troubleshooting

- `AUTH_FAILED`: run `plaud login`.
- `plaud: command not found`: reopen shell or confirm npm global bin is on PATH.
- Local OAuth callback uses `localhost:8199`.
