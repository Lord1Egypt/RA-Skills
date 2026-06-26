---
name: portable-context-os
description: >
  Buildable Bring Your Own Context system for AI agents. Use for: creating user-owned or org-owned context vaults, scaffolding typed memory systems, generating MCP-native context layers, building portable bundle workflows, migrating context across runtimes, and auditing long-running agent memory systems.
---

# Portable Context OS

Use this skill to **build**, audit, or migrate a **Bring Your Own Context** system for agents. Treat durable context as infrastructure that should outlive any one model, chat product, or agent runtime.

Use this skill when the user wants any of the following:

1. A real **context vault** or external memory layer for agents.
2. A move from vendor-native memory to **user-owned or organization-owned context**.
3. Chat history, artifacts, and preferences turned into **typed memory objects**.
4. An **MCP-native** or otherwise model-agnostic context interface.
5. A portable bundle that can move working context between runtimes.
6. An audit of whether an existing memory system is brittle, noisy, or weakly governed.

Do **not** use this skill for simple one-chat personalization. Use it when the problem is architectural, portable, or long-running.

## Core rule

Do not stop at guidance when the user wants a working system. Build the workspace, generate the MCP server, validate the output, and leave behind runnable artifacts.

## The six paradigm shifts

Apply these shifts before building anything.

1. **Move from prompt state to context infrastructure.** Treat durable context as a system layer, not as hidden prompt residue.
2. **Move from vendor memory to owned context.** Separate memory ownership from model usage.
3. **Move from chat logs to typed memory objects.** Store preferences, workflows, artifacts, state, and evaluations as distinct classes.
4. **Move from full-context loading to just-in-time retrieval.** Route only what the active task needs.
5. **Move from personalization to governed memory contracts.** Add review, permissions, deletion, auditability, and portability.
6. **Move from static agents to context flywheels.** Improve memory schema, routing quality, and evaluation after every run.

## Workflow decision

Choose the path that matches the task.

| Situation | Action |
|---|---|
| Building a new context system | Follow the **Creation workflow** and run the builder script |
| Auditing an existing agent or product | Follow the **Audit workflow** |
| Packaging or migrating context between tools or teams | Follow the **Migration workflow** |

## Creation workflow

Follow these steps in order.

### Step 1: Map the context surface

Identify the ownership mode first: personal, team, or enterprise.

Then map the six minimum design inputs:

1. Primary actor.
2. Core workflows.
3. Artifact types.
4. Memory types.
5. Governance constraints.
6. Portability target.

Read `references/context_architecture.md` before proposing any storage or retrieval design.

### Step 2: Define the memory taxonomy

Do not allow the system to collapse into one generic memory blob.

Define at least these categories unless there is a clear reason not to:

- identity memory
- preference memory
- workflow memory
- domain memory
- relationship memory
- artifact memory
- execution memory
- evaluative memory

Use `templates/memory_object.md` to define each memory object class.

### Step 3: Build the runtime, not just the documents

Specify the following components explicitly:

- context vault
- retrieval router
- writeback or update engine
- artifact store
- policy layer
- interface layer such as MCP, API, or CLI

Use `templates/context_manifest.yaml` to record the architecture and ownership model.

When the user wants a real system, run:

```bash
python /home/ubuntu/skills/portable-context-os/scripts/init_context_os.py <output_dir> --name <system_name> --ownership <personal|team|enterprise> --goal <goal> --source-runtime <source> --target-runtime <target>
```

This builder must generate all of the following inside the target workspace:

| Output | Purpose |
|---|---|
| `context_manifest.yaml` | Architecture, ownership, routing, and runtime definition |
| `governance_policy.md` | Memory rules and policy surface |
| `eval_scorecard.md` | Evaluation and feedback-loop baseline |
| `feedback_log.md` | Retrieval misses, corruption risks, governance failures, portability failures |
| `memory_objects/` | Typed memory storage |
| `artifacts/` | First-class artifact store |
| `tools/build_context_bundle.py` | Local bundle rebuild utility |
| `mcp_server/server.py` | Working MCP server scaffold |
| `mcp_server/requirements.txt` | Runtime dependency list |

### Step 4: Define governance before automation

Write rules for:

- memory creation
- human review
- redaction
- retention
- forgetting or deletion
- export and import
- access control
- audit trail

Use `templates/governance_policy.md` and read `references/evaluation_and_governance.md`.

### Step 5: Validate the generated MCP server

Do not declare success after file generation alone. Validate that the generated server loads and can inspect the workspace.

Run:

```bash
python <workspace>/mcp_server/server.py --dry-run
```

If the user wants the server fully runnable in the current environment, install runtime dependencies and validate again.

### Step 6: Build a portable bundle

Run:

```bash
python <workspace>/tools/build_context_bundle.py <workspace>
```

Use the generated bundle manifest for handoff, migration, or review.

### Step 7: Customize the seeded workspace

Replace placeholder values, refine routing rules, add real memory objects, and populate the artifact store. Treat the generated workspace as a working starter system, not as final truth.

## Audit workflow

Use this path when the user already has an agent, product, or memory system.

1. Read `references/evaluation_and_governance.md`.
2. Identify where durable context currently lives.
3. Determine whether the memory is platform-scoped, user-scoped, or organization-scoped.
4. Identify whether retrieval is typed and just-in-time or indiscriminate and prompt-heavy.
5. Check whether artifacts, preferences, and execution state are separated.
6. Check whether deletion, export, and audit semantics are real or only nominal.
7. Produce a gap analysis against the six paradigm shifts.
8. Convert the findings into a revised `context_manifest.yaml` and `eval_scorecard.md`.
9. If the user wants a fix, build a replacement workspace and MCP server with `init_context_os.py`.

## Migration workflow

Use this path when the user wants to move context across models, tools, teams, or employers.

1. Identify the source memories and artifacts.
2. Separate raw exports from live operational context.
3. Normalize the memories into typed objects.
4. Redact or re-scope organization-bound memories when ownership changes.
5. Package the result as a portable bundle.
6. Define what the receiving agent may read, update, or not retain.
7. If the target environment needs an active interface, generate a new MCP server-backed workspace and import the normalized materials into it.

Use `scripts/build_context_bundle.py` after normalizing the source materials.

## Generated MCP server expectations

The generated MCP server should expose a usable BYOC interface rather than a placeholder.

At minimum, the generated server should support:

| Capability | Why it matters |
|---|---|
| Describe context system | Confirms the server sees the manifest and workspace |
| List memory objects | Enables typed retrieval |
| Get memory object | Enables precise inspection |
| Upsert memory object | Enables writeback into the context vault |
| Delete or tombstone memory object | Enables governance and forgetting |
| List artifacts | Preserves artifacts as first-class memory |
| Build portable bundle | Keeps portability live, not theoretical |
| Append feedback log | Maintains the self-improving loop |

Prefer tools for state changes, resources for readable workspace files, and prompts for controlled memory-review flows.

## Self-improving feedback loop

Activate this loop whenever the skill runs.

1. Record **retrieval misses**: what the agent needed but did not retrieve.
2. Record **memory corruption risks**: stale, duplicated, or over-generalized memories.
3. Record **governance failures**: missing deletion paths, weak permissions, weak auditability.
4. Record **portability failures**: what could not move cleanly between runtimes.
5. Update the context manifest, memory taxonomy, routing rules, and server defaults.
6. Re-run the evaluation scorecard before declaring the design stable.

## Output requirements

When using this skill, produce deliverables that are inspectable, editable, and runnable.

At minimum, aim to leave behind:

| Deliverable | Purpose |
|---|---|
| `context_manifest.yaml` | Architecture, ownership, interfaces, and routing summary |
| memory object definitions | Typed memory model |
| governance policy | Rules for creation, retention, access, and deletion |
| evaluation scorecard | Retrieval, portability, and trust metrics |
| portable bundle manifest | Reviewable handoff and migration artifact |
| working MCP server scaffold | Live interface into the owned context system |

## Resources

Read resources only when needed.

- Read `references/context_architecture.md` when designing the system shape.
- Read `references/paradigm_shifts.md` when the user wants the deeper conceptual framing or a strategy memo.
- Read `references/evaluation_and_governance.md` when auditing trust, deletion, portability, or evaluation.
- Use `templates/` files as editable starting points.
- Run `scripts/init_context_os.py` to build a new workspace **and** MCP server.
- Run `scripts/build_context_bundle.py` to summarize and package a workspace.

## Working rule

Optimize for **owned, typed, governed, portable context**. Do not optimize for the illusion of memory if the resulting system still traps the user inside one runtime.
