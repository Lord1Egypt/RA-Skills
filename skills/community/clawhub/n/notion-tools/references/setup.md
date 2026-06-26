# Setup

## Environment assumptions

- The examples assume macOS and `zsh`
- Prefer a runtime-provided `NOTION_KEY`
- Use `~/.config/notion/api_key` only as an optional local fallback
- Export `NOTION_VERSION=2025-09-03`

## Preferred credential flow

Use `NOTION_KEY` directly when the runtime or caller already provides it.

```bash
export NOTION_KEY="ntn_your_key_here"
export NOTION_VERSION=2025-09-03
```

Read the secret only when a Notion API call is actually needed, and never echo the full token back to the user.

## Optional local fallback setup

If `NOTION_KEY` is not already available in a local shell workflow, keep a fallback token file:

```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```

## Load variables

```bash
export NOTION_VERSION=2025-09-03

if [ -z "${NOTION_KEY:-}" ] && [ -f ~/.config/notion/api_key ]; then
  export NOTION_KEY="$(cat ~/.config/notion/api_key)"
fi
```

This preserves `NOTION_KEY` when it is already present and touches the local file only as a fallback.

## JSON inspection

If `jq` is installed, use it to inspect JSON responses.

On macOS:

```bash
brew install jq
```

If `jq` is unavailable, run the same `curl` commands without `| jq`, or use `python3 -m json.tool` only when pretty printing is needed.
