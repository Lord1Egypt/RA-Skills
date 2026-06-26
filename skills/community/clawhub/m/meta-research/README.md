# Meta-Research

A Claude Code skill that guides you through the full research lifecycle — from brainstorming to publication — with built-in rigor, reproducibility tracking, and bias mitigation.

## What it does

Meta-Research acts as an autonomous research copilot with a **5-phase workflow state machine**:

1. **Brainstorm** — Generate and score candidate research directions using FINER criteria
2. **Literature Review** — Systematic search with PRISMA-style audit trails
3. **Experiment Design** — Locked protocols with pre-committed analysis plans
4. **Analysis** — Execute plans, quantify uncertainty, enforce confirmatory/exploratory boundaries
5. **Writing** — Structured drafting with reproducibility checklists and artifact preparation

Phases are **non-linear** — the workflow supports backtracking when evidence demands it (e.g., lit review reveals the idea is already solved → return to brainstorm).

Every decision is logged in a **LOGBOX** for full provenance tracking.

## Installation

### From marketplace

```bash
/plugins marketplace add <marketplace-url>
/plugins install meta-research
```

### Manual installation

```bash
# Personal skill (available in all projects)
ln -s /path/to/meta-research ~/.claude/skills/meta-research

# Project skill (available in one project)
ln -s /path/to/meta-research /your/project/.claude/skills/meta-research
```

## Usage

```
/meta-research [your research question or topic]
```

You can enter at any phase — the skill will ask where you are in your research and pick up from there.

### Examples

```
/meta-research How does in-context learning scale with model size?
/meta-research I have experiment results and need help with analysis
/meta-research Help me write up my findings on retrieval-augmented generation
```

## Project structure

```
meta-research/
├── SKILL.md                              # Main skill definition
├── phases/
│   ├── brainstorming.md                  # Ideation and idea selection
│   ├── literature-review.md              # Search, screen, synthesize
│   ├── experiment-design.md              # Protocol, data, controls
│   ├── analysis.md                       # Statistics, evaluation, ablations
│   └── writing.md                        # Reporting and dissemination
├── templates/
│   ├── scoring-rubric.md                 # FINER + AI-specific idea scoring
│   ├── experiment-protocol.md            # Full experiment design template
│   ├── reproducibility-checklist.md      # Pre-submission checklist
│   └── logbox.md                         # Logbox format and examples
├── raw-meta-research.md                  # Source material and references
├── LOGBOX.md                             # Development log
├── .claude-plugin/
│   └── plugin.json                       # Plugin manifest
├── LICENSE
└── README.md
```

## Key features

- **Audit-ready logging** — Every decision tracked with what, when, alternatives, and why
- **Bias mitigation** — Separates exploratory vs confirmatory analysis, constrains researcher degrees of freedom
- **Reproducibility-first** — Version control, pinned environments, experiment tracking built into the workflow
- **Falsification mindset** — Designs experiments to disprove, not confirm
- **Phase templates** — Reusable scoring rubrics, experiment protocols, and checklists
- **Dynamic backtracking** — Automatically suggests returning to earlier phases when evidence warrants it

## License

[MIT](LICENSE)
