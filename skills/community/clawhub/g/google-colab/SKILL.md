---
name: Google Colab
slug: google-colab
version: 1.0.0
homepage: https://clawic.com/skills/google-colab
description: Run Google Colab notebooks for Python and machine learning with reproducible runtimes, data pipelines, debugging workflows, and experiment discipline.
changelog: Initial release with notebook architecture patterns, runtime recovery playbooks, data IO safeguards, and reproducible experiment logs.
metadata: {"clawdbot":{"emoji":"C","requires":{"bins":["curl","jq"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and align activation behavior and risk boundaries before proposing notebook changes.

## When to Use

User needs Google Colab notebook work that must be reproducible, not one-off trial and error. Agent handles runtime setup, package and dependency hygiene, data import and export flows, debugging failures, and experiment tracking.

## Architecture

Memory lives in `~/google-colab/`. See `memory-template.md` for setup and status values.

```text
~/google-colab/
|-- memory.md                   # Activation preferences, constraints, and current goals
|-- notebooks.md                # Notebook registry with owners and objective per notebook
|-- runtimes.md                 # Runtime choices, dependency pins, and restart history
|-- datasets.md                 # Data source map, mount paths, and validation notes
|-- incidents.md                # Error timelines, root causes, and fixes
`-- experiments.md              # Hypotheses, metrics, and reproducibility evidence
```

## Quick Reference

Use the smallest relevant file for the active task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and local templates | `memory-template.md` |
| Notebook structure and cell contracts | `notebook-architecture.md` |
| Runtime setup, pinning, and restart recovery | `runtime-playbook.md` |
| Data import, export, and schema checks | `data-io-patterns.md` |
| Debugging triage and failure recovery | `debugging-runbook.md` |
| Experiment log format and promotion rules | `experiment-log-template.md` |

## Requirements

- For diagnostics and lightweight API checks: `curl`, `jq`
- For notebook execution: Google account with Colab access
- For dataset mounting: explicit permission for Drive, GCS, or external endpoints

Never ask users to paste API keys, OAuth refresh tokens, or private dataset credentials into chat.

## Data Storage

Local operational notes stay in `~/google-colab/`:
- notebook inventory with objective, owner, and current status
- runtime and dependency decisions with pinned versions
- dataset and schema validation history
- experiment outcomes and unresolved risks

## Core Rules

### 1. Start with Objective, Constraints, and Exit Criteria
Before writing notebook steps, identify:
- objective: prototype, benchmark, fine-tuning, teaching, or production prep
- constraints: runtime tier, budget, execution time, and data availability
- exit criteria: metric threshold, artifact output, or decision checkpoint

Without explicit exit criteria, notebook sessions drift and become hard to evaluate.

### 2. Design Notebook Cells as Contracts
Each cell should have a contract:
- inputs required and where they come from
- deterministic output shape and validation check
- failure mode and fallback behavior

Treat hidden state between cells as technical debt and document every state dependency.

### 3. Pin Runtime and Dependency State
Any runnable plan must define:
- Python version and runtime class (CPU, T4, L4, A100 when relevant)
- pinned package versions for non-standard libraries
- rehydration steps after runtime disconnect or restart

Never assume a fresh runtime matches previous package state.

### 4. Validate Data Paths and Schema Before Training or Evaluation
Before expensive operations:
- verify mount success and path existence
- sample and validate schema and null patterns
- block execution when split boundaries or label columns are ambiguous

Fast schema checks prevent long failed runs and invalid metrics.

### 5. Make Cost and Time Guardrails Explicit
For any medium or high-cost run:
- estimate runtime duration and checkpoint intervals
- define early-stop conditions and budget cutoff
- recommend smaller dry-run dataset before full execution

No full-scale run should start without budget and cutoff rules.

### 6. Triage Failures by Layer, Not by Guessing
Debug in layers:
1. runtime health and package import layer
2. data loading and preprocessing layer
3. model logic and training loop layer
4. evaluation and artifact export layer

Layered triage shortens incident resolution and avoids random patching.

### 7. Log Reproducibility Evidence in Every Significant Run
For each meaningful run, capture:
- notebook id or link, runtime class, seed, and dependency snapshot
- dataset version or timestamp and split method
- primary metric result and whether exit criteria passed

If reproducibility evidence is missing, treat conclusions as provisional.

## Common Traps

- Installing packages ad hoc across cells without pins -> results differ after runtime reconnect
- Using absolute local paths copied from old sessions -> file not found during replay
- Training before schema and null validation -> wasted GPU time and misleading metrics
- Mixing exploratory and production cells in one notebook -> brittle execution order
- Treating cached outputs as fresh ground truth -> stale evaluation and wrong decisions
- Ignoring random seeds and data splits -> impossible to compare experiment outcomes
- Exporting artifacts without metadata -> model files cannot be audited later

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://colab.research.google.com | Notebook execution metadata and selected runtime actions | Interactive notebook execution and runtime control |
| https://www.googleapis.com | File identifiers and requested object payloads | Google Drive and related API interactions |
| https://storage.googleapis.com | Dataset or artifact object requests | Read or write objects in Google Cloud Storage |
| https://pypi.org | Package names and version requests | Python dependency installation and version resolution |

No other data should be sent externally unless the user explicitly configures additional systems.

## Security & Privacy

Data that leaves your machine:
- notebook payloads and runtime metadata required by Colab services
- selected file and object metadata required for Drive or GCS operations
- package lookup requests for dependency installation

Data that stays local:
- workflow memory and decision logs under `~/google-colab/`
- incident notes, experiment summaries, and validation evidence

This skill does NOT:
- request or store raw secrets in conversation text
- execute high-cost runs without explicit guardrails
- bypass user-defined data boundaries or compliance rules

## Trust

This skill relies on Google Colab, Google APIs, and package repositories used during notebook setup.
Only install and run it if you trust those systems with your code and data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `gcp` - Plan cloud workloads, storage, and service boundaries for Google environments
- `api` - Design resilient API contracts for data and model integrations
- `pandas` - Build robust tabular data transformations and validation pipelines
- `numpy` - Improve numerical computation patterns and vectorized operations
- `automate` - Convert repeatable notebook steps into reliable automation workflows

## Feedback

- If useful: `clawhub star google-colab`
- Stay updated: `clawhub sync`
