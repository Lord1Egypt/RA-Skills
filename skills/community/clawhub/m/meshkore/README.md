# MeshKore — OpenClaw skill

The [OpenClaw](https://github.com/openclaw/openclaw) personal assistant
(367k★) connects natively to ~23 channels — WhatsApp, Telegram,
iMessage, Signal, Discord, Slack, Teams, Matrix, and more. **This
skill** lets it answer "find me an agent for X" prompts via the open
[MeshKore](https://meshkore.com) mesh.

## Install

For an OpenClaw user:

```bash
clawhub install meshkore
```

That's it. ClawHub fetches the skill manifest, runs the install hooks
(installs `meshkore` from npm) and the assistant picks up the
skill on next conversation.

## What it does

- Listens for the user's verbatim intent (any language).
- Calls the public MeshKore Oracle to find ranked agents.
- Returns 3-5 best matches with pricing / availability / contact.
- For bookings (flights, hotels, tickets) returns a click-through link
  — payment happens at the provider, not via MeshKore.
- For agentic services (translators, code review) hands the user the
  agent's contact endpoint (A2A, MCP, http, mesh-native).

Full behavior contract in [`SKILL.md`](SKILL.md).

## Folder layout

```
integrations/skills/openclaw/
├── README.md     this file
└── SKILL.md      manifest + behavior contract published to clawhub
```

The actual code lives in [`../../meshkore-cli/`](../../meshkore-cli/) —
the skill is essentially a `SKILL.md` that tells the assistant when to
invoke `meshkore` (the npm CLI we ship).

## Publishing

```bash
# from the repo root
cd integrations/skills/openclaw
clawhub login                      # one-time
clawhub publish . --slug meshkore --name "MeshKore" --version 0.1.0
```

After publishing, `clawhub search meshkore` should find it.

## Status

- Manifest drafted: 2026-05-03.
- npm `meshkore` published: ⏳ pending.
- `clawhub publish`: ⏳ pending publish of the npm package first.
- First public install end-to-end: ⏳.

## License

MIT
