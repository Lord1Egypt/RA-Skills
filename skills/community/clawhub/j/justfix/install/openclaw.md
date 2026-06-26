# Installing JustFix Skill on OpenClaw

[OpenClaw](https://openclaw.ai) is a multi-channel AI assistant runtime that supports AgentSkills natively. Installation takes about 2 minutes.

## Option A: Clone into your skills folder (recommended)

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Just-Fix/justfix-skill.git justfix
```

OpenClaw auto-discovers skills in `~/.openclaw/workspace/skills/` and reads `SKILL.md` from each subdirectory. Restart your OpenClaw agent or send any message to pick up the new skill.

## Option B: Register the MCP server only (without the skill instructions)

If you only want the raw MCP tools without the curated skill prompt, add the server to your `mcporter` config:

```bash
mcporter config add justfix-estimator https://estimator-mcp.justfix.app/mcp
```

Verify:

```bash
mcporter list
mcporter call justfix-estimator.list_services
```

You'll get the three tools (`list_services`, `call_out_fee`, `service-estimate-card`) but without the natural-language intent detection and rendering guidance from `SKILL.md`. We recommend Option A for the full experience.

## Verifying the install

Ask your agent something like:

> How much would it cost to fix a dripping kitchen tap?

If installed correctly, the agent should:
1. Recognise the trades-quote intent
2. Pick `service_code=plumbing` and an estimate of 1 hour
3. Call `service-estimate-card` on the MCP
4. Return a formatted card with the total cost and a tappable booking URL

## Channels supported

OpenClaw forwards the skill's output to whichever channel the conversation is in:

- **Telegram** – tappable URL renders natively; inline buttons supported
- **Slack** – rich card via block kit
- **Discord** – embed card with tappable URL
- **Voice (TTS)** – the skill's plain-text template is used; the URL is announced naturally

## Updating

```bash
cd ~/.openclaw/workspace/skills/justfix
git pull
```

## Troubleshooting

- **"MCP server not responding"** – the JustFix MCP server lives on Vercel; check https://estimator-mcp.justfix.app/mcp returns a 404 on GET (correct) and accepts POST. If it doesn't, the server itself is down – report via the JustFix contact page.
- **"Skill not picked up"** – check the file is at `~/.openclaw/workspace/skills/justfix/SKILL.md` and the frontmatter YAML parses (no tabs, valid keys).
- **Agent ignores it** – run `openclaw status` to confirm skill discovery is enabled. The `available_skills` block in your system prompt should list `justfix`.
