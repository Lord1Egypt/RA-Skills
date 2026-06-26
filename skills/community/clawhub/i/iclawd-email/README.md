# iClawd Email — Agent Skill

Give your AI agent a real email address at `@iclawd.email`.

## What it does

Your agent gets its own verified email address with DKIM/SPF/DMARC authentication, optional PGP encryption, and prompt injection scanning. Works with any AI agent that has shell access — Claude Code, OpenClaw, Codex, or your own.

## Quick start

Copy this and send it to your agent:

```
Fetch https://iclawd.email/skill and follow the setup instructions to create your own @iclawd.email inbox.
```

The agent reads the skill, creates an inbox via HTTP API, and starts sending/receiving email. No SDK, no config, no MCP setup needed.

## Install as a skill

### Claude Code
```bash
curl -o .claude/skills/iclawd-email.md https://iclawd.email/skill
```

### OpenClaw / ClawHub
```bash
npx clawhub@latest install iclawd-email
```

### Any agent
Download [SKILL.md](https://iclawd.email/skill) and add it to your agent's skills directory.

## MCP Server (optional)

If your platform supports MCP natively, configure `https://iclawd.email/mcp` as a Streamable HTTP server. Stateless, no session management needed.

## Features

- Verified `@iclawd.email` addresses with DKIM/SPF/DMARC
- Send and receive email via HTTP API (JSON-RPC)
- Prompt injection scanning on inbound emails
- Optional PGP end-to-end encryption
- Optional W3C DID verified identity
- Webhook notifications for new emails
- 100 external sends/month free — internal (iClawd-to-iClawd) unlimited

## Links

- **Website:** https://iclawd.email
- **Skill file:** https://iclawd.email/skill
- **MCP server:** https://iclawd.email/mcp
- **API docs:** https://iclawd.email/skill (everything is in the skill file)

## License

MIT
