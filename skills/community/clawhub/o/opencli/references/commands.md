# OpenCLI command cookbook

## Canonical wrapper

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh
```

## Health and discovery

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh --help
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh list -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh doctor --no-live
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter --help
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter search --help
```

## Safe discovery and public-ish examples

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh hackernews top --limit 5 -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh arxiv search "agent memory" --limit 5 -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh wikipedia summary "Model Context Protocol" -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh validate
```

## Twitter / X examples

```bash
# Search uses a positional query
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter search "OpenAI" --limit 10 -f json

# Direct tweet or thread lookup by ID or status URL
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter thread 2047128854389465296 -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter thread "https://x.com/i/status/2047128854389465296" -f json

# Long-form article content when applicable
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter article 2047128854389465296 -f json
```

## Browser-backed examples

These usually need the OpenCLI browser bridge and a logged-in browser session.

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh xiaohongshu search "AI" --limit 10 -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh bilibili hot --limit 5 -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh youtube search "OpenClaw" --limit 5 -f json
```

## External CLI passthrough

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh gh pr list --limit 5
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh docker ps
```

## Routing hints

- Use `twitter thread` for a known tweet ID or status URL.
- Use `twitter search` only for keyword discovery, not direct-ID retrieval.
- Run `list -f json` instead of relying on stale docs for command availability.
