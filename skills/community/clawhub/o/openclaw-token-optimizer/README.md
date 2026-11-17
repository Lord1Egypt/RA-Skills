# Token Optimizer for OpenClaw & Hermes

[![Version](https://img.shields.io/badge/version-4.1.1-brightgreen.svg)](CHANGELOG.md)
[![MissionDeck](https://img.shields.io/badge/MissionDeck-ai-blueviolet)](https://missiondeck.ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)

Built by [MissionDeck.ai](https://missiondeck.ai) · [GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) · [ClawHub](https://clawhub.ai/asif2bd/skills/openclaw-token-optimizer)

**Find where your AI agent may be wasting tokens—and get a clear, safe improvement plan.**

Large instructions, poorly matched models and repetitive AI tasks can all add overhead.
Token Optimizer helps your OpenClaw or Hermes agent investigate those opportunities and
explain what is worth changing. It does not silently change your setup or promise savings
it has not measured.

## Start by asking your agent

Once the skill is installed, say:

> “Use Token Optimizer to check my setup and suggest the three most useful improvements.”

You can also ask:

- “Are my scheduled tasks using AI when a simple script would do?”
- “Which instruction files are taking up the most context?”
- “Review my model choices for everyday tasks.”
- “Check my Hermes profile for unnecessary recurring AI work.”

**You do not need to begin with terminal commands.** A tool-enabled agent uses its known
host runtime, current agent or active profile to perform read-only checks. It asks only
when information is missing or ambiguous. The skill cannot add terminal access to an
agent that does not have it.

## What you will get

- **A clear verdict:** what was inspected and what deserves attention.
- **Prioritized suggestions:** a few useful next steps, with evidence and caveats.
- **No surprise changes:** your models, schedules and instruction files stay untouched.
- **Honest limits:** missing spending data stays unknown, not a misleading zero.

For example, it may flag an agent task running every few minutes for review, or identify
large instruction files. Neither proves waste by itself; your agent explains the trade-off
before recommending a change. Actual savings require a comparable before/after measurement.

## One skill, two platforms

**OpenClaw:** inspects the native model catalog/status and scheduled jobs. Optional known
config files add deeper checks. Recognizes agent tasks, commands, heartbeats and system events.

**Hermes Agent:** reads the active profile's configuration and scheduled jobs. Traces model
choices including saved creation-time defaults, skips paused jobs, and recognizes no-agent
scripts. This is file-based auditing—not native model discovery or authentication testing.

**Both:** can inspect selected instruction sizes, duplicate content and supplied usage
figures. Model recommendations need a user policy and sufficient availability evidence.

The agent selects the runtime from trusted context. If both platforms are installed and
no active runtime is known, it asks rather than guessing. Your chosen profile takes priority.

## Install

Ask your agent to install the ClawHub skill **openclaw-token-optimizer** through its normal
skill installer, or use the ClawHub CLI:

```bash
clawhub install openclaw-token-optimizer --version 4.1.1
```

The slug stays the same for both platforms. Keep the bundled scripts and references with
SKILL.md. Python 3.10+ is required; YAML input additionally needs PyYAML, usually available
in the Hermes Python environment. Nothing is installed automatically by the audit.

OpenClaw is tested on 2026.9.4. Hermes compatibility is tested against a pinned upstream
cron-storage implementation in an isolated profile, without starting an agent or scheduler.
See [Hermes compatibility](references/HERMES.md) and [agent quick start](references/QUICKSTART.md).

## Frequently asked before starting

**Will this reduce my bill automatically?** No. It finds candidates for improvement; actual
savings depend on the changes you choose and how they perform on matched workloads.

**Will it break my working setup?** The bundled analyzer does not edit configuration,
activate models, execute jobs or restart anything. OpenClaw read commands may contact
configured services or update native caches.

**Do I need to prepare exports?** Not for a normal audit when the host has the required
read tools and known profile. Exports are an alternative for offline use; Hermes's separate
model-routing function requires normalized catalog/status evidence.

**Does it measure my complete API spending?** Not automatically. Native usage collection
and budget alerts are not included. Missing or incomplete data is labeled clearly.

---

The sections below are for advanced users and maintainers. Your agent can handle these
steps for an ordinary audit.

## Advanced: run the OpenClaw audit yourself

```bash
python3 scripts/optimizer.py audit --live --agent YOUR_AGENT --json
```

Replace `YOUR_AGENT` with your actual agent ID. To include config-level findings, provide
an explicit local JSON file with `--config /path/to/config.json`. Its contents are not echoed.

Generate a review plan with the same inputs:

```bash
python3 scripts/optimizer.py plan --live --agent YOUR_AGENT --json
```

The plan contains review actions, not automatic fixes. Model absence and missing metadata
are reasons to investigate—not proof that a model or job is broken.

## Choose a model using your policy

```bash
python3 scripts/optimizer.py route --live --agent YOUR_AGENT \
  --policy assets/config.example.json --tier research --json
```

The bundled policy illustrates routine, balanced, research, coding and background tiers.
Adapt it to your available providers and quality/cost preferences. It is not a universal
ranking or live pricing database. Recommendations never activate a model.

Add `--image`, `--tools` or `--context-tokens 8000` when the task requires those capabilities.
Unknown capability metadata blocks the recommendation. In particular, many native catalogs
do not expose `supportsTools`; lack of that field does not mean the model lacks tools.
A separately authorized exact-route canary is needed before activation.

## Inspect context size and duplicate instructions

```bash
python3 scripts/optimizer.py context /path/to/SOUL.md /path/to/AGENTS.md --json
```

Only explicitly named files are read. Reports show character counts, approximate tokens
(character count divided by four), and duplicate content. They do not print file contents.
Use OpenClaw's native `/context list` and `/context detail` to establish actual injected
context. Do not remove essential agent instructions based on file size alone.

## Check supplied usage without false zeros

```bash
python3 scripts/optimizer.py budget --json
python3 scripts/optimizer.py budget --usage usage.json --limit 10 --json
```

`usage.json` accepts an aggregate such as `{"costUSD":2.5,"complete":false}`.
Without data, the result is unknown/null. **Automatic native usage ingestion, daily/weekly
alerts and measured billing comparisons are not included in v4.1.1.**

## Offline audit and input formats

```bash
python3 scripts/optimizer.py audit --catalog catalog.json --status status.json \
  --config config.json --jobs jobs.json --json
```

Native JSON shapes:

- Catalog: `{ "models": [{ "key": "provider/model", "available": true, "input": "text+image", "contextWindow": 32000 }] }`
- Status: `{ "allowed": ["provider/model"], "auth": { "missingProvidersInUse": [], "modelRouteIssues": [] } }`
- Config: `{ "agents": { "defaults": { "model": "provider/model" }, "entries": {} } }`
- Automations: `{ "jobs": [] }`
- Optional normalized sessions via `--sessions`: `{ "sessions": [{ "agentId": "example", "model": "provider/model" }] }`

Inputs must be JSON, not JSON5. Missing inputs and paginated automation responses are
explicitly marked as incomplete coverage. Tool capability may be supplied as
`supportsTools: true` only when backed by trustworthy metadata.

## Safety and operational limits

The pure analysis core has no I/O. Explicit live mode invokes fixed native read commands:

- `openclaw --version`
- `openclaw models list --agent ID --all --json`
- `openclaw models status --agent ID --json`
- `openclaw cron list --all --json` (audit/plan only)

These commands may contact your configured Gateway or providers and update native caches.
The optimizer does not run paid inference probes, upload reports, install other software,
or write your configuration. Native reads have a 45-second timeout; inputs have an 8 MiB
size limit. Selected identifiers and basenames can still be private—review reports before sharing.

Exit **0** means analysis completed, not that no issues exist. Exit **2** means invalid
input or a failed native read. Reports go to stdout; `--json` supports downstream tooling.
`plan` intentionally emits no schema-blind patches. See [SECURITY.md](SECURITY.md).

## Automation support

Native **heartbeat** and **systemEvent** jobs are now recognized. The optimizer no longer
reports them as unknown or subjects them to agent-turn-only model/timeout/context checks.
Unknown future payload kinds remain visible. Recognition is not a full audit of those
jobs' effective runtime settings.

## Frequently asked questions

### Does this automatically reduce OpenClaw API costs?

No. It identifies review candidates. Savings depend on which changes you safely apply
and must be measured on comparable workloads. There is no guaranteed savings percentage.

### Does it work with OpenAI, Anthropic and other model providers?

Routing uses your supplied/native catalog and policy instead of a fixed vendor list.
Eligibility depends on your model availability, allowlist and capability evidence.
Catalog availability alone is not proof that an exact authentication route will succeed.

### Will it change my models, cron jobs or heartbeat schedule?

No. All v4 commands are diagnostic. No restart is required to run the CLI.

### Is the ClawHub package verifiable?

Yes. From the extracted package directory:

```bash
sha256sum -c SHA256SUMS.txt
```

`LICENSE.txt` and `SHA256SUMS.txt` survive registry clients that filter extensionless files.
Hashes verify integrity, not safety. Check the version-specific ClawHub security review too.

## Development and migration

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
```

Tests are in the GitHub source, not the installed skill bundle. CI covers Python
3.10/3.12/3.13. From v3, use the new CLI arguments: old script names are migration shims,
not the former prompt classifiers or template installers. Existing state files are left
untouched. MIT licensing is retained. See [CHANGELOG.md](CHANGELOG.md).

## MissionDeck.ai — Your Agent Command Center

[MissionDeck.ai](https://missiondeck.ai) is the related multi-agent coordination dashboard.
This optimizer runs locally, requires no MissionDeck account and has no cloud upload integration.

## More by Asif2BD

Browse [Asif2BD on ClawHub](https://clawhub.ai/asif2bd) for other OpenClaw skills.

[MissionDeck.ai](https://missiondeck.ai) · [OpenClaw documentation](https://docs.openclaw.ai/) · [Source code](https://github.com/Asif2BD/OpenClaw-Token-Optimizer)
