# How to Run

Ways to run the PosteAhora CLI, from a one-off command to CI automation.

## 1. Install globally

```bash
npm install -g @posteahora/cli
# or
pnpm install -g @posteahora/cli
```

Then use the `posteahora` command anywhere:

```bash
posteahora --help
posteahora accounts
```

## 2. Run without installing (npx)

```bash
npx @posteahora/cli --help
npx @posteahora/cli accounts
```

## 3. In scripts / CI

Authenticate with an environment variable instead of the saved config:

```bash
export POSTEAHORA_API_KEY=pah_live_xxxxxxxx
posteahora post "Nightly digest" --to twitter:a1b2
```

Example GitHub Actions step:

```yaml
- name: Publish release note
  env:
    POSTEAHORA_API_KEY: ${{ secrets.POSTEAHORA_API_KEY }}
  run: |
    npx -y @posteahora/cli post "New release is live 🚀" \
      --to twitter:${{ vars.X_ACCOUNT_ID }} \
      --to linkedin:${{ vars.LINKEDIN_ACCOUNT_ID }}
```

## 4. From an AI agent

- **This skill** wraps the CLI (`allowed-tools: Bash(posteahora:*)`) — the agent
  runs `posteahora` commands directly.
- Prefer MCP? Use [`@posteahora/mcp`](https://github.com/posteahora/mcp) instead.

## Requirements

- Node.js **18 or newer** (native `fetch`).
- A PosteAhora API key (**Settings → API & integrations**).

## Configuration

| Setting | Resolution order |
|---------|------------------|
| API key | `--key` → `POSTEAHORA_API_KEY` → `~/.posteahora/config.json` |
| Base URL | `POSTEAHORA_API_URL` (default `https://api.posteahora.com/functions/v1/api`) |

## Verify it works

```bash
posteahora --version
posteahora auth          # shows auth status
posteahora accounts      # a real API call
```
