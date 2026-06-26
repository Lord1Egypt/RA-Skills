# Runtime Contract

## Purpose
Define the smallest truthful runtime contract for the MVP of `openclaw-consensus`.

The MVP runtime should feel like a native OpenClaw skill, not a second provider platform. OpenClaw remains the source of truth for provider/model availability and authentication. This project only selects from that existing pool and orchestrates the 2-round deliberation workflow.

## Core UX principle
The user should not have to configure API keys, provider auth, or a second model registry inside this project.

The runtime should assume:
- OpenClaw already knows which providers/models are configured and usable
- the skill can select from that configured pool
- the user experience should focus on the brief and model choice, not setup duplication

## MVP input contract
### Required input
- `brief`
  - the question, scenario, or problem to deliberate on

### Optional input
- `models`
  - explicit shortlist selected from the models/providers already configured in OpenClaw
  - this should be treated as effectively required in MVP; the runtime should not silently choose a default model set
- `run_root`
  - output directory for artifacts
  - if omitted, the runtime should generate a deterministic local run directory
- `label`
  - optional human-readable run label

## Model/provider assumption
For MVP, the runtime should not own provider credentials.

Instead, it should:
- inspect or receive the available OpenClaw-configured model pool
- allow explicit selection from that pool
- reject models not available through the active OpenClaw environment
- reject runs that do not specify a valid model shortlist in MVP

## Selection rules
### MVP behavior
The runtime should require explicit model selection from the OpenClaw-configured pool.

It should not:
- silently choose a default set
- guess what the user meant
- substitute a missing model with another model automatically

### Good UX constraints
- prefer 3-4 models max in MVP
- prefer strong general reasoning models only
- avoid weak or trivial models that add noise without useful contrast
- fail clearly if fewer than 2 suitable configured models are selected and available

## Runtime workflow
### Step 1 — initialize run
The runtime should:
- capture the original brief
- capture the selected model list
- create the run directory
- write initial run metadata

### Step 2 — round 1
For each selected model:
- send the exact same original brief in unchanged form
- request an independent first-pass answer
- instruct the model to state assumptions, note uncertainty, and separate fact from inference where possible
- write the round-1 output to disk

### Step 3 — round 2
For each selected model:
- provide the original brief
- provide one orchestrator-built round-2 prompt shared identically across all selected models
- include the concatenated round-1 outputs from all selected models as one merged quoted/delimited block
- instruct the model to reassess conflicts, rethink weak claims, research fuzzy areas more deeply, and produce one final answer with quality prioritized over speed
- write the round-2 output to disk

### Step 4 — final orchestration
The orchestrator should review all round-2 outputs and write a final synthesis that clearly separates:
- consensus
- disagreement
- unresolved uncertainty
- escalation points
- final synthesis / best overall answer

For MVP, the orchestrator should use the same model as the active OpenClaw session model.
The skill should not ask the user to configure a separate orchestrator model.

## Output contract
The runtime output should be useful without extra interpretation.

The final report should help the user quickly see:
- what seems stable across providers
- what remains contested
- what still looks source-sensitive or unclear
- what specific narrow areas may justify expert review

## UX rules
- no duplicate provider auth setup
- no domain modes in MVP
- no hidden extra rounds
- no vague “processing” without visible artifact structure
- no pretending that consensus guarantees correctness

## Failure behavior
The runtime should fail clearly when:
- fewer than 2 suitable configured models are selected and available
- no explicit model shortlist is provided in MVP
- a selected model is not available in OpenClaw's configured pool
- one or more round outputs cannot be produced
- the final synthesis cannot be generated

Failure output should remain readable and artifact-preserving where possible.

## MVP boundary reminders
This contract explicitly excludes:
- provider-specific auth setup in this repo
- repo-local `.env` model configuration as the primary path
- domain modes
- local CLI / Ollama routing
- dynamic rounds or convergence loops
- web UI

## Design note
OpenClaw owns model/provider configuration.
OpenClaw Consensus owns deliberation workflow, artifact writing, and final synthesis.
