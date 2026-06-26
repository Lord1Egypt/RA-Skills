# Product Spec — OpenClaw Consensus

## Working title
OpenClaw Consensus

## Product definition
A focused OpenClaw skill for 2-round cross-model deliberation. It runs one brief through multiple LLM providers, gives them a single reconciliation round, and then synthesizes consensus, disagreements, uncertainties, and escalation points.

## Primary user
OpenClaw users who need a more trustworthy way to examine complex questions across multiple models before deciding, escalating, or paying for expert help.

## Why this should exist
Single-model answers can look confident while still hiding blind spots, shallow sourcing, or provider-specific bias. OpenClaw has a real edge here: it can coordinate multiple providers in one environment, preserve the artifacts, and synthesize the result into something more decision-useful than a one-shot answer.

## OpenClaw-specific edge
- one orchestration layer across multiple LLM providers
- same brief, same bounded workflow, different model priors
- durable artifact trail across both rounds
- one final synthesis that highlights alignment and conflict
- future expansion path to other provider routes, without changing the core product idea

## Workflow
### Round 1 — independent answers
Each selected model receives the same brief and answers independently. Each answer should state assumptions, note uncertainty, and distinguish facts from inference.

### Round 2 — reconciliation
Each selected model receives:
- the original brief
- the concatenated round-1 answers from all selected models
- an instruction to reassess conflicts, rethink weak claims, research fuzzy areas more deeply, and produce one final answer with quality prioritized over speed

### Final orchestration
The orchestrator reviews all round-2 answers and produces a final report with:
- consensus points
- disagreement points
- unresolved uncertainty
- escalation points worth human expert review
- final synthesis / best overall answer

## MVP scope
### In scope
- OpenClaw-native skill
- generic mode only
- fixed 2-round flow
- API-backed providers only
- 3-4 provider slots max
- durable local artifacts
- orchestrator final synthesis

### Out of scope
- domain-specific modes
- web UI or browser product
- local CLI or Ollama routing
- execution workflows
- more than 2 rounds
- dynamic swarm behavior
- expert-replacement claims

## Output contract
The final output should make it obvious:
- what all selected models agree on
- where material disagreement remains
- what still looks uncertain or source-sensitive
- what narrow points are worth escalating to a lawyer, accountant, engineer, or other expert

## Success criteria for MVP
- the product is easy to explain in one paragraph
- the workflow is bounded and truthful
- the final artifact is more useful than a single-model answer for complex questions
- the repo clearly demonstrates OpenClaw's cross-provider orchestration advantage

## Positioning note
For the initial repo, positioning should be technical-mechanism-first because the first audience is already OpenClaw users. Use cases belong in examples, docs, and later content — not in the core definition.
