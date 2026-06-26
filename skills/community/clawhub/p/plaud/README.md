# OpenClaw Skill Plaud Note Taking

An OpenClaw skill for Plaud note taking workflows through Plaud MCP and the Plaud CLI.

## What it helps agents do

- List recent Plaud recordings
- Find recordings by date or keyword
- Read transcripts and summaries
- Extract topics, decisions, speakers, and action items
- Draft follow-up notes from recordings
- Export summaries and transcripts
- Diagnose Plaud MCP or CLI authentication

## Requirements

- OpenClaw
- Node.js 20 or newer
- Plaud MCP configured, or Plaud CLI installed

## Plaud MCP setup

```bash
openclaw mcp set plaud '{"command":"npx","args":["-y","@plaud-ai/mcp@latest"]}'
```

Then authenticate through the Plaud MCP login flow.

## Plaud CLI setup

```bash
npm install -g @plaud-ai/cli@latest
plaud login
plaud me
```

## Telegram command

The recommended Telegram command is a single router command:

```text
/plaud [action] [target]
```

Supported actions:

```text
/plaud
/plaud recent
/plaud last
/plaud find <query>
/plaud summary [id|last|query]
/plaud actions [id|last|query]
/plaud transcript [id|last|query]
/plaud export [id|last|query]
/plaud status
/plaud login
```

If no action is provided, `/plaud` shows compact help plus recent recordings. If the text after `/plaud` is not a known action, it is treated as a search query.

### Registering the Telegram command in OpenClaw

This skill declares:

```yaml
user-invocable: true
```

With OpenClaw `commands.nativeSkills: "auto"`, Telegram can expose the skill directly as `/plaud`. This is additive. It does not require replacing existing custom commands such as `/commands`, `/menu`, or other configured entries.

If native skill commands are disabled in your OpenClaw config, enable them rather than overwriting `channels.telegram.customCommands`.

## Skill install

Install from ClawHub:

```bash
clawhub install plaud
```

Or inspect it first:

```bash
clawhub inspect plaud
```

Manual install:

```bash
git clone https://github.com/antoniosilveira/openclaw-skill-plaud-note-taking.git plaud
```

Then place the `plaud` folder in your OpenClaw skills directory or install it through your preferred OpenClaw skill workflow.

The skill folder is the repository root. The required skill file is `SKILL.md`.

## ClawHub

This skill is currently published on ClawHub as `plaud`.

- Install: `clawhub install plaud`
- Inspect: `clawhub inspect plaud`
- Update: `clawhub update plaud`

Note: ClawHub reserves the `openclaw-` slug namespace, so `openclaw-skill-plaud-note-taking` cannot be used as the ClawHub slug unless the registry grants access to that namespace.

## Helpful links

- [Plaud website](https://www.plaud.ai/)
- [Plaud MCP documentation](https://docs.plaud.ai/documentation/plaud_app/mcp)
- [Plaud CLI documentation](https://docs.plaud.ai/documentation/plaud_app/cli)
- [Plaud documentation index](https://docs.plaud.ai/llms.txt)

## License

MIT-0
