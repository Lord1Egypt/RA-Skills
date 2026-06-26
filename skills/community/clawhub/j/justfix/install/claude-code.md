# Installing JustFix Skill on Claude Code

[Claude Code](https://docs.anthropic.com/claude/claude-code) is Anthropic's CLI for software engineering tasks, but it also supports MCP servers and AgentSkills via its plugin system.

## Step 1: Register the MCP server

In your project (or globally for all projects):

```bash
claude mcp add justfix-estimator https://estimator-mcp.justfix.app/mcp --transport http
```

Or for global use:

```bash
claude mcp add --scope user justfix-estimator https://estimator-mcp.justfix.app/mcp --transport http
```

Verify:

```bash
claude mcp list
```

You should see `justfix-estimator` listed with three tools.

## Step 2: Add the skill to your Claude Code skills folder

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/Just-Fix/justfix-skill.git justfix
```

Claude Code picks up skills from `~/.claude/skills/` automatically.

## Step 3: Verify

Start a Claude Code session:

```bash
claude
```

Then ask:

> Quote me for a 2-hour electrical job to install some sockets.

Claude Code should call `service-estimate-card` with `service_code=electrical`, `estimate=2`, and return a quote card with a tappable booking URL.

## Notes

- Claude Code is primarily a coding tool, but the JustFix skill works for any Claude Code session. Useful if you're a developer building integrations with JustFix and want to test the MCP from your IDE.
- The booking URL renders as plain text in the terminal but is tappable in IDE integrations (VS Code Claude plugin, JetBrains plugin).
- No auth required.

## Updating

```bash
cd ~/.claude/skills/justfix
git pull
```
