---
name: harness-control-layer
description: Use this skill when designing or operating a Harness-style control layer for OpenClaw setups with many skills, memory surfaces, safety-sensitive tools, playbooks, and verification requirements. It helps route tasks to the right skill or memory/context layer, preflight risky actions, define completion checks, and promote repeated incidents into reusable playbooks or skills.
---

# Harness Control Layer

Use this skill to make large OpenClaw setups more deterministic. Harness should sit above existing OpenClaw surfaces as an operational control layer. It should route, classify, verify, and record. It should not replace memory, context, skills, or execution policy.

## Core Boundary

Harness should not become:

- a second memory backend,
- a second context engine,
- an Obsidian/wiki clone,
- an exec-policy bypass,
- a hidden autonomous permission system.

Harness should decide which official layer should handle the task and how completion should be verified.

## Routing Workflow

For each user task:

1. Classify the task intent.
2. Select the likely handling layer.
3. Preselect the top 1-3 candidate skills or playbooks.
4. Check whether the task includes risky operations.
5. Define objective verification before execution.
6. Execute through normal OpenClaw tools, permissions, and approvals.
7. Record incidents and promote repeated workflows into playbooks or skills.

Use this high-level flow:

```text
task intake
 -> skill routing
 -> memory/context routing
 -> safety preflight
 -> execution
 -> evaluation
 -> incident/lesson recording
 -> skill/playbook promotion
```

## Memory And Context Boundaries

Route by responsibility:

| Task type | Primary surface |
|---|---|
| Durable user preference or decision | `memory-core` / active memory |
| Long conversation recall or compaction recovery | `lossless-claw` / context engine |
| Human-readable knowledge note | `memory-wiki` or Obsidian |
| Operational incident, repair flow, or verification record | Harness |
| Reusable procedure | OpenClaw skill or playbook |

Do not store the same fact in every layer. Pick the layer that owns the responsibility.

## Skill Routing

When many skills exist, avoid unrestricted scanning. Generate a short candidate list first:

```text
user task -> harness skill router -> top 1-3 candidate skills -> model chooses/executes
```

Prefer skills whose description, tags, or registry metadata match:

- task intent,
- required tools,
- target system,
- risk level,
- verification needs,
- known failure mode.

If the match is weak, ask a focused clarification or fall back to a general workflow.

## Safety Preflight

Run preflight thinking before actions such as:

- delete,
- overwrite,
- move,
- recursive cleanup,
- wildcard deletion,
- cross-drive operations,
- service restart,
- config mutation,
- credential or token handling.

For high-risk operations, require:

- exact target path or service,
- backup or rollback path when practical,
- expected blast radius,
- verification command,
- normal OpenClaw approval or sandbox enforcement.

Harness can classify and explain risk. It must not bypass official execution policy.

## Verification

Treat "done" as "verified".

Before execution, define checks such as:

- command exits successfully,
- service health endpoint returns OK,
- port is listening,
- expected file exists,
- rendered artifact opens,
- test passes,
- UI state is visible,
- logs no longer show the known error.

After execution, run the checks. If verification is impossible, say that explicitly and describe the remaining risk.

## Incident Learning

Record useful incidents in a compact structured form:

```json
{
  "task": "openclaw upgrade",
  "symptom": "gateway restart failed",
  "root_cause": "systemd service used stale node binary",
  "fix": "point ExecStart to the active Node runtime",
  "verification": "gateway status ok and expected port listening",
  "reuse_rule": "check service ExecStart early after upgrades",
  "should_update_playbook": true
}
```

Promote repeated incidents in this order:

```text
incident note -> playbook -> skill -> registry metadata
```

## ClawHub Metadata Suggestions

When publishing skills that should work with Harness routing, include concise metadata where supported:

- intents,
- keywords,
- negative keywords,
- preferred_when,
- avoid_when,
- risk level,
- sensitive actions,
- verification checks,
- playbook or incident support.

This helps routing layers select candidates without loading every skill into context.

