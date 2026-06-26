# Installing JustFix Skill on Codex CLI

[Codex CLI](https://github.com/openai/codex) is OpenAI's terminal-based coding assistant. It supports MCP servers via its `~/.codex/config.toml`.

## Step 1: Register the MCP server

Edit `~/.codex/config.toml` and add:

```toml
[mcp_servers.justfix-estimator]
command = "npx"
args = ["-y", "mcp-remote@latest", "https://estimator-mcp.justfix.app/mcp"]
```

This wraps the streamable-HTTP MCP server in the `mcp-remote` proxy (Codex's MCP client expects stdio).

## Step 2: Drop the skill into Codex's instructions folder

```bash
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git clone https://github.com/Just-Fix/justfix-skill.git justfix
```

Then add a reference in your `~/.codex/AGENTS.md` or project `AGENTS.md`:

```markdown
## Available Skills

- **justfix** – quote UK trades jobs. See `~/.codex/skills/justfix/SKILL.md` for the full skill.
```

Codex CLI reads `AGENTS.md` at session startup and picks up the skill reference automatically.

## Step 3: Verify

Open a Codex CLI session:

```bash
codex
```

Then ask:

> What does JustFix charge for a boiler service?

Codex should call `call_out_fee` and `service-estimate-card` and return the quote.

## Notes

- Codex CLI is primarily a coding tool. The JustFix skill is useful here mainly for developers building on the JustFix MCP.
- The `mcp-remote` proxy is reliable but adds a small startup latency (~200ms). The actual MCP call is fast.
- No auth required.
- Booking URL renders as plain text in the terminal.

## Updating

```bash
cd ~/.codex/skills/justfix
git pull
```
