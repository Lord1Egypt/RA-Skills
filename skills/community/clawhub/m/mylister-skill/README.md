# MyLister.dev Skill

Agent skill for natural language control of [MyLister.dev](https://app.mylister.dev) task management.

## Setup

```bash
# Install dependencies
npm install

# Build
npm run build

# Set environment variables
export LISTER_BASE_URL="https://api.mylister.dev"
export LISTER_PRODUCTION_BASE_URL="https://api.mylister.dev"
export LISTER_STAGING_BASE_URL="https://staging-api.mylister.dev"
export LISTER_API_KEY="your-api-key-here"
export LISTER_PRODUCTION_API_KEY="your-production-key"
export LISTER_STAGING_API_KEY="your-staging-key"
export LISTER_CONTACTS='{"Sarah":"sarah@example.com","mom":"mom@example.com"}'
```

The API key is read from the environment and sent as `X-API-Key`. Never commit an API key to this repository or place it in a prompt. On Windows PowerShell, use:

Get your key in [MyLister.dev Settings](https://app.mylister.dev/settings) under the **API Key** tab.

```powershell
$env:LISTER_BASE_URL = "https://api.mylister.dev"
$env:LISTER_PRODUCTION_BASE_URL = "https://api.mylister.dev"
$env:LISTER_STAGING_BASE_URL = "https://staging-api.mylister.dev"
$env:LISTER_API_KEY = "your-api-key-here"
$env:LISTER_PRODUCTION_API_KEY = "your-production-key"
$env:LISTER_STAGING_API_KEY = "your-staging-key"
$env:LISTER_CONTACTS = '{"Sarah":"sarah@example.com","mom":"mom@example.com"}'
```

## Install In Agent Hosts

This repository is an [Agent Skills-compatible](https://agentskills.io/) skill. The root `SKILL.md` contains the agent instructions, while the TypeScript client in `dist/` performs the API calls. Because `dist/` is built locally and is not committed, use the clone/build flow below for this repository.

### OpenClaw

Install the built skill into the shared OpenClaw skills directory:

```bash
git clone https://github.com/mgoettel13/MyLister-Skill.git /tmp/MyLister-Skill
cd /tmp/MyLister-Skill
npm ci
openclaw skills install . --as lister --global
```

For a workspace-only install, omit `--global`. Start a new OpenClaw session, then ask naturally, for example: `Add "Call Mama" to my today list`.

OpenClaw also supports `openclaw skills install git:mgoettel13/MyLister-Skill@main`, but a direct Git skill install does not run this repository's build step. Build first, then install the local directory as shown above. See the [OpenClaw skills documentation](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md).

### Hermes

Hermes keeps installed skills in `~/.hermes/skills/`. Clone and build the skill there:

```bash
git clone https://github.com/mgoettel13/MyLister-Skill.git ~/.hermes/skills/lister
cd ~/.hermes/skills/lister
npm ci
hermes skills list
```

Start a new Hermes session and use `/lister` or describe the task normally. Hermes can also install a standalone `SKILL.md` URL with `hermes skills install`, but the clone/build flow is required here so the Node API client is available. See the [Hermes skills guide](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills) and [CLI reference](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md).

### Codex

For the current repository, install it as a **standalone Codex skill**:

```bash
git clone https://github.com/mgoettel13/MyLister-Skill.git "$CODEX_HOME/skills/lister"
cd "$CODEX_HOME/skills/lister"
npm ci
```

If `CODEX_HOME` is not set, use the Codex skills directory shown by your installation, commonly `~/.codex/skills/lister`. Restart Codex or start a new session, set `LISTER_API_KEY` in the environment, and ask for a MyLister action. Codex can then load the root `SKILL.md` and run the bundled CLI.

### Claude Code

Claude Code supports project skills in `.claude/skills/` and personal skills in `~/.claude/skills/`. Install it for all projects with:

```bash
git clone https://github.com/mgoettel13/MyLister-Skill.git ~/.claude/skills/lister
cd ~/.claude/skills/lister
npm ci
```

Or clone it into `<your-project>/.claude/skills/lister` for that project only. Start Claude Code from the relevant project and ask naturally, or invoke `/lister`. See the [Claude Code skills documentation](https://code.claude.com/docs/en/slash-commands).

## Usage

### CLI
```bash
node dist/index.js add "call Notary" to my today list
node dist/index.js get priority items
node dist/index.js mark item 123 done
node dist/index.js remove item 456
node dist/index.js update item 789 to "new title"
```

### As Module
```typescript
import { handleCommand } from './dist/index.js';

const response = await handleCommand('add "buy groceries" to my today list');
console.log(response);
```

## Supported Commands

| Command | Example |
|---------|---------|
| Add item | `add "task" to my [list] list` |
| Add item with note | `add "task" to my [list] list with note "details"` |
| Add project item | `add "task" to my project list starts 2026-09-01 due 2026-09-05 for 3 hours assigned to user@example.com` |
| Get items | `get my [list] list` |
| Priority items | `get priority items` |
| Mark done | `mark item [id] done` |
| Remove item | `remove item [id]` |
| Update item | `update item [id] to "new text"` |
| Move item | `move item [id] to my [list] list` |
| Add note | `note for item [id]: "text"` |
| Item comments | `comment on item [id]: "text"` |
| Note comments | `comment on note [note_id] for item [id]: "text"` |
| Export item | `export item [id] as html` |
| Email item / list / priority | `email item [id] to Sarah` / `send my work list to Mom` / `send priority items to Alex` |
| Reorder notes | `reorder notes for item [id] in order: [note_id], [note_id]` |
| Attach file | `attach file "C:\\docs\\plan.pdf" to item [id]` |
| Upload media | `upload image "C:\\images\\brief.png" to item [id]` |
| File URL | `get file URL for [file_key] expires 3600` |
| API environment | `switch to production` / `switch to staging` |
| API base URL | `set API base URL to https://api-staging.mylister.dev` |
| API key | `set API key to abc123` |
| Reminders | `add "task" to my today list reminder tomorrow at 9am` |
| Notebook lists | `create a new list called Journal notebook` |
| Project lists | `create a new project list called Website Launch` |
| Change list type | `update my Launch list to project` |
| Move completed | `move completed to bottom of my today list` |

## API

- **API documentation:** [MyLister API docs](https://api.mylister.dev/docs)
- **Base URL:** `https://api.mylister.dev` (or override with `LISTER_BASE_URL`, `LISTER_PRODUCTION_BASE_URL`, `LISTER_STAGING_BASE_URL`)
- **Production/staging keys:** Set `LISTER_PRODUCTION_API_KEY` / `LISTER_STAGING_API_KEY` when envs use different credentials.
- **Auth:** API key via `X-API-Key`
- **Endpoints:** `/v1/lists`, `/v1/items`, `/v1/items/priority`, item/note comments, item exports, note reorder, attachments, media uploads, file URLs, health, and version

## License

MIT
