# Installing JustFix Skill on Hermes

[Hermes](https://github.com/anthropic-experimental/hermes) is an AI assistant harness similar to OpenClaw, running Anthropic's Claude. It uses the same AgentSkills format.

## Installation

```bash
cd ~/.hermes/skills
git clone https://github.com/Just-Fix/justfix-skill.git justfix
```

Hermes discovers skills under `~/.hermes/skills/`. Restart Hermes or send a fresh message to pick up the new skill.

## Register the MCP server (if Hermes doesn't auto-discover from SKILL.md frontmatter)

Add to `~/.hermes/config.yaml` under the `mcp_servers` section:

```yaml
mcp_servers:
  justfix-estimator:
    url: https://estimator-mcp.justfix.app/mcp
    transport: streamable-http
```

Then restart Hermes.

## Verifying

Ask:

> What services does JustFix offer?

Hermes should call `list_services` and return the 13 categories. If it doesn't, check:

1. `ls ~/.hermes/skills/justfix/SKILL.md` exists
2. The skill is listed in your skill index (Hermes usually logs this on startup)
3. The MCP server is reachable: `curl https://estimator-mcp.justfix.app/mcp` returns a 404 on GET (correct – the endpoint only accepts POST)

## Channel notes

Hermes inherits the channel-agnostic markdown template from SKILL.md. Telegram inline buttons, Slack blocks, and Discord embeds all work the same as in OpenClaw.

## Updating

```bash
cd ~/.hermes/skills/justfix
git pull
```
