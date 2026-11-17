# JubJub skill for OpenClaw

One launch to every platform you publish to, and an ownership record for each piece as it goes out. JubJub is media ownership and payment infrastructure, and this skill connects your OpenClaw agent to it over MCP.

## MCP endpoint

```
https://api.jubjubapp.com/v2/mcp
```

## What your agent can do

- **Publish** a video to TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, Mux and Farcaster in one launch, now or on a schedule.
- **Own the record.** When a piece goes out, JubJub writes its ownership record on Base. Your agent can read it and see who holds it.
- **Follow every destination.** Each launch reports a result per platform, and a failed destination can be sent again.
- **Search and buy media.** Catalogue search is free. Agents buy a piece's metadata, or the piece itself, per use over x402 or MPP.
- **Track results** per piece and across your whole catalogue.
- **Run the team.** Workspaces, versions, reviewers and approvals, comments and share links.

Public, destructive and financial actions always wait for your yes. The skill tells the agent which ones.

## Setup

1. Sign up free at [studio.jubjubapp.com/auth](https://studio.jubjubapp.com/auth).
2. Go to **Profile**, then **Agents**, and create a new agent (for example "OpenClaw").
3. Copy its key. It starts with `jjagent_`.
4. Add it to your OpenClaw config:

```yaml
skills:
  entries:
    - skill: jubjub
      apiKey: jjagent_YOUR_KEY_HERE
```

Or set it as an environment variable:

```bash
JUBJUB_API_KEY=jjagent_YOUR_KEY_HERE
```

5. Connect the platforms you publish to, in JubJub or by asking your agent ("connect my TikTok").

## Install

### ClawHub

```bash
clawhub install jubjub
```

### From GitHub

Paste this into your OpenClaw chat:

```
https://github.com/JubJub-app/jubjub-openclaw-skill
```

## Try saying

- "Publish my latest video to Instagram and TikTok."
- "Schedule this to YouTube and LinkedIn for Monday at 9am."
- "What happened with my last launch?"
- "Who holds the ownership record for this video?"
- "How did my videos do this month?"
- "Find 3 clips about street food in the JubJub catalogue."

## How payment works

- Using JubJub is free for people. Publishing, analytics, ownership reads, team work and catalogue search are free for agents too.
- Agents pay per use only to unlock a piece from the catalogue, over x402 (USDC on Base) or MPP (USDC on Tempo). The server quotes the price in its payment challenge before anything is charged.
- Any account can turn agent discovery and purchase off in its settings.
- JubJub earns a small fee on settled revenue, when money moves.

## Requirements

- A JubJub account ([sign up free](https://studio.jubjubapp.com/auth))
- The platforms you publish to, connected in JubJub
- OpenClaw with any supported model

## Support

- **Site:** [jubjubapp.com](https://jubjubapp.com)
- **Issues:** open a GitHub issue in this repo

## License

MIT
