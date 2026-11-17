# mumo — Hermes Agent skill

**Multi-model deliberation for Hermes.** When your local agent needs more than its backbone model can offer on a hard call, mumo runs a panel of frontier models (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) in parallel and returns each model's full response plus typed cross-model reactions — what each model keeps, challenges, or wants explored in the others' claims. Use it for architecture decisions, design reviews, pre-launch pressure tests, and any contested choice.

mumo is a tool the native Hermes agent calls — not another autonomous agent. You stay in control of the conversation; mumo just produces the panel output.

## Install

### Skills hub (recommended)

```bash
hermes skills install clawhub/mumo-hermes
```

The slug is `mumo-hermes` — the bare `clawhub/mumo` slug is the OpenClaw variant of this skill (different tool-name prefix and setup steps), so install this one. Hermes prompts for your `MUMO_API_KEY` at install time and saves it to `~/.hermes/.env`; you add the MCP server block yourself (below). Sign up at [mumo.chat](https://mumo.chat) and create a platform key at [Settings → API Keys](https://mumo.chat/settings/api-keys) (keys start with `mmo_live_`) before installing.

### Local install via git clone

```bash
git clone https://github.com/mumo-chat/mumo-hermes \
  ~/.hermes/skills/software-development/mumo
```

That places `SKILL.md` at `~/.hermes/skills/software-development/mumo/SKILL.md`, which is where Hermes' skill scanner expects it. mumo lives under `software-development/` alongside skills that share its shape — `writing-plans`, `plan`, `requesting-code-review` — all of which are "force yourself to think harder before acting" methodologies.

Then add the MCP server config: open `~/.hermes/config.yaml` and merge the contents of `config/mumo.yaml` under your `mcp_servers:` key. The block references `${MUMO_API_KEY}` rather than embedding the key, so put the key in `~/.hermes/.env` instead.

Create the file and restrict it *before* putting anything in it, so the key is never written into a world-readable file:

```bash
touch ~/.hermes/.env && chmod 600 ~/.hermes/.env
```

Then open `~/.hermes/.env` in your editor and add a line:

```
MUMO_API_KEY=mmo_live_your_key_here
```

Edit the file rather than appending from the shell: a command containing the literal key is recorded in your shell history, and running it twice silently stacks a duplicate entry.

`.env` is where Hermes expects secrets to live, which keeps the mumo block in `config.yaml` free of a live credential. **Fully exit and restart Hermes** afterward (the `/reload-mcp` slash command is unreliable across versions).

After restart, the eight mumo tools register as `mcp_mumo_create_deliberation`, `mcp_mumo_wait_for_round`, `mcp_mumo_append_round`, `mcp_mumo_get_session`, `mcp_mumo_list_sessions`, `mcp_mumo_list_models`, `mcp_mumo_share_session`, `mcp_mumo_get_credit`.

Confirm the connection end to end before spending anything on a panel:

```bash
hermes mcp test mumo
```

That opens a real connection and lists the tools it finds. `hermes mcp list` only reports what is saved in your config — it does not prove the key resolved. If the test fails, the masked `Authorization:` line it prints tells you whether `${MUMO_API_KEY}` resolved at all.

## Invoke

Hermes skills are explicitly called, not auto-triggered. Two ways:

```
/mumo "Postgres or MongoDB for our event store given 50k events/day,
       a Postgres-experienced team, and a 3-month runway?
       What would we regret 6 months in?"
```

Or naturally: *"Ask mumo to compare Postgres and MongoDB for our event store..."*

Either way, Hermes loads the skill, calls `create_deliberation`, waits for the round, reads the cross-model claim map, and synthesizes for you. You can stop there, or push back via typed snippets (`KEEP` / `EXPLORE` / `CHALLENGE` / `CORE` / `SHIFT`) and append another round.

## When mumo is worth the deliberation tax

The skill encodes the trigger taxonomy in detail. In short, reach for mumo when:

- **Architecture decisions with non-obvious tradeoffs**
- **Plan or design review before commitment**
- **Pre-launch pressure tests**
- **Stuck debugging after repeated failed attempts**
- **Pre-commit adversarial review on risky diffs** (auth, payments, migrations)
- **Strategy questions with multiple defensible framings**
- **Explicit user requests**

Skip mumo for routine refactors, formatting, syntax help, or anything where "just write a test" is cheaper than discussion.

## What's in this repo

- **`SKILL.md`** — the canonical skill teaching Hermes when to invoke mumo, the deliberation loop, how to read claim maps, snippet doctrine, and verification discipline.
- **`config/mumo.yaml`** — the MCP server config block to merge into `~/.hermes/config.yaml` (only needed for git-clone installs; a hub install handles this automatically).
- **`playbooks/`** — four cognitive-shape playbooks loaded on demand: `contested-decision`, `design-review`, `uncertainty-expansion`, `red-team`.
- **`reference/`** — five reference docs: `claim-maps`, `snippets`, `model-selection`, `synthesis`, `operating-notes`.

## Related skills

- [`writing-plans`](../writing-plans) — write implementation plans before building
- [`plan`](../plan) — pause to externalize a plan before executing
- [`requesting-code-review`](../requesting-code-review) — get a structured review before commit

All of these share mumo's shape: structured methodology to think harder before acting.

## Links

- Product — https://mumo.chat
- Install guide — https://mumo.chat/install/hermes
- MCP reference — https://mumo.chat/docs/mcp
- REST API — https://mumo.chat/docs/api
- Hermes Agent — https://hermes-agent.nousresearch.com
- Issues — https://github.com/mumo-chat/mumo-hermes/issues

## License

MIT
