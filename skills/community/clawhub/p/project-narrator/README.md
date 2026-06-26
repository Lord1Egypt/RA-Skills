# project-narrator

**Your project's single source of truth — a living document that can reconstruct everything from scratch.**

> *Bus factor of 1? Not anymore.*

## What is this?

An OpenClaw skill that generates, audits, and maintains a `PROJECT-NARRATIVE.md` file — capturing your entire project's architecture, decisions, infrastructure, and state in one document.

Not just documentation. A **disaster recovery prompt.** Hand it to any developer (or AI agent) and they can rebuild your project.

## Install

```bash
clawhub install project-narrator
```

Or copy the files directly into your project.

## Usage

| Command | What it does |
|---------|-------------|
| `narrator generate` | Scan workspace → generate PROJECT-NARRATIVE.md |
| `narrator audit` | Compare narrative against reality → flag drift |
| `narrator update` | Incrementally update from git history |
| `narrator report` | Health report without modifying anything |

## What the narrative captures

- **Architecture** — what's built, how it connects
- **Infrastructure** — where it runs, what services it uses
- **Pipeline/Workflow** — what runs when, in what order
- **API Routes** — every endpoint, auth requirements
- **Scripts** — every script, what it does, what calls it
- **Design Principles** — WHY decisions were made (the most important section)
- **Known Issues** — what went wrong and what was tried
- **Changelog** — significant changes over time
- **Credentials & IDs** — where secrets live (not the secrets themselves)

## Scripts

Two standalone Python scripts (stdlib only, zero dependencies):

- **`scripts/generate.py`** — Scans your workspace and generates a narrative scaffold
- **`scripts/audit.py`** — Reads your narrative, checks references against reality, flags issues

```bash
python3 scripts/generate.py --workspace /path/to/project
python3 scripts/audit.py /path/to/PROJECT-NARRATIVE.md
```

## Origin

Built during the development of [AgentWyre](https://agentwyre.ai), an AI intelligence wire service where maintaining accurate project state across dozens of cron jobs, API endpoints, and daily pipelines proved that living documentation isn't optional — it's infrastructure.

## License

MIT
