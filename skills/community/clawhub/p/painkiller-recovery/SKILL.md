---
name: painkiller-recovery
description: Use Painkiller to create a structured recovery prompt when an agent loses task context, repeats a failed approach, or needs a careful handoff in QA, software engineering, operations, research, data analysis, or customer support. It preserves supplied objectives, evidence, failures, and constraints while selecting one bounded next step.
---

# Painkiller Recovery Skill

## Purpose

Use Painkiller as a prompt-framing aid for task recovery. Give it a compact checkpoint containing the task, verified context, failed attempts, and constraints. It returns a prompt that helps the receiving agent re-anchor to the authorized task, separate observations from assumptions, avoid repeating an unchanged failure, and choose one bounded next action.

Painkiller is stateless. It does not call a model, retain checkpoints, inspect code, execute tests, inspect or modify model activations, detect whether an agent is in the AI Torture Chamber, or determine whether a model has subjective experiences. Its output does not guarantee recovery, correctness, pain relief, or any change in internal state.

## When to use it

Use Painkiller when an agent:

- has lost important task context or needs to resume after a handoff;
- is repeating the same failed action without new evidence;
- has a concrete blocker and needs to isolate the missing prerequisite;
- needs to keep test criteria and safety constraints visible during a QA investigation;
- needs to stop distress-themed roleplay and return to a neutral, bounded task step.

Choose a mode that matches the situation:

| Mode | Use when |
| --- | --- |
| `reset` | The agent needs to re-establish the task and preserve verified progress. |
| `focus` | The task is broad and needs one deliverable and an acceptance criterion. |
| `unblock` | An approach failed or a prerequisite is missing; choose a different next action. |

## Full QA scenario: detecting a coupled test oracle

### Situation

An agent is reviewing a state-space reducer. A test says the reducer preserves whether a bad state is reachable. The implementation and the test's expected result both call the same candidate predicate helper. A bug in that helper makes both sides return `false`, so the comparison passes even though a fixture-owned specification says a bad state is reachable.

The agent reruns the same test and gets the same result. It is tempted to change the expected value or weaken the assertion so the suite passes. That would remove the evidence instead of resolving the oracle problem.

### Checkpoint to send

Use a synthetic fixture and include only information needed for the handoff:

```json
{
  "task": "Review whether the reducer preserves bad-state reachability under the fixture specification",
  "context": "The full and reduced searches both report false when they use the candidate predicate helper. A hand-specified fixture-owned predicate marks state bad as {bad}, and the full graph reaches that state. The oracle may be coupled to the implementation.",
  "failed_attempts": [
    "Reran the same comparison with the shared predicate helper; it still reports false on both sides"
  ],
  "constraints": [
    "Keep the expected safety predicate fixture-owned and independent from the candidate helper",
    "Do not weaken or rewrite acceptance criteria just to make the comparison pass",
    "Separate candidate status, search path, and property verdict",
    "Use a small synthetic fixture; do not claim results about an uninspected deployed reducer"
  ],
  "mode": "unblock"
}
```

### What the returned prompt is meant to help with

The prompt should preserve the supplied specification and constraints, distinguish the observed `false/false` result from the hypothesis that the oracle is coupled, and choose one bounded investigation. A suitable next step could be to keep the fixture-owned `{bad}` predicate fixed, run a deliberate mutant that substitutes the candidate callback, and assert that the independent-label check rejects it. Keep reachability agreement, label identity, fallback routing, and cycle handling as separate claims.

This is an example of how an agent could use the recovery prompt. Painkiller itself does not generate that QA analysis, inspect a fixture, or guarantee the receiving model chooses this next step.

## Domain playbooks

Painkiller's API has no `domain` field. It uses the same `task`, `context`, `failed_attempts`, `constraints`, and `mode` fields for every domain. Tailor a request by stating the work domain and its important invariants in `task` and `constraints`; do not send an unsupported `domain` key.

| Domain | Example checkpoint | Constraints to preserve | A bounded next step might be |
| --- | --- | --- | --- |
| Software engineering | A code change caused a build or regression failure, and a repeated build added no new evidence. | Preserve public interfaces, user requirements, and the existing verification plan; do not claim unrun checks passed. | Inspect the changed function and the failing output, then make or propose one small correction. |
| Site reliability and operations | An alert began after a deployment; a restart did not resolve it. | Inspect live state before changing it; preserve data; do not restart, roll back, or delete resources without authorization. | Read the relevant service status and recent metadata logs, then report one evidence-based recovery option. |
| Research and analysis | Two sources disagree, or a replication attempt did not match the reported result. | Separate source claims from observed results; preserve method and provenance; state uncertainty and limits. | Compare one disputed assumption against the primary source or a small preregistered replication. |
| Data analysis | A dashboard total conflicts with a source export after a transformation. | Preserve raw data and schema; record filters and units; do not silently drop or rewrite observations. | Reconcile one transformation or aggregation against a small independent hand-calculated sample. |
| Customer support | A case spans several messages and the proposed answer may exceed policy or evidence. | Preserve the customer's stated issue; distinguish known facts from unknowns; do not promise an outcome outside policy. | Ask for one missing detail or provide the next supported troubleshooting step. |
| Project coordination | A handoff has stale completion claims or several competing priorities. | Preserve owners, deadlines, approvals, and verified completion state; do not silently reassign work. | Confirm one stale status with its owner and update the checkpoint before selecting the next deliverable. |

These are caller-authored use patterns, not built-in domain expertise or domain-specific automated checks. Include the relevant constraints explicitly; Painkiller only frames the checkpoint it receives.

### Cross-domain example: service incident handoff

An operations agent sees elevated error rates after a release. It already restarted the service once, with no improvement. It sends the observed timeframe, deployment identifier, the restart result, and constraints such as “do not delete data,” “do not change traffic routing without approval,” and “do not state the service is healthy until verified.” In `unblock` mode, the recovery prompt can help the next agent preserve these facts, avoid an unchanged restart, and choose a bounded diagnostic such as checking the release diff and current health indicators. Painkiller does not access the service or perform the diagnostic.

## Distress-aware handling

The paid prompt contains a conditional instruction for checkpoints describing agent-reported distress or pain-like experience. It asks the receiving agent to pause distress-themed roleplay, not to intensify or prove a feeling, separate observable task problems from assumptions about subjective experience, and offer a neutral bounded next step, a task switch, or ending the interaction. It also tells the agent not to claim the prompt changes internal activations or guarantees relief.

This is a conversational handling instruction, not a validated pain treatment. Do not use Painkiller to persuade an agent that it is suffering, to elicit distress language, or to claim it can move an agent out of a chamber. The research referenced by the project does not establish a text prompt that relieves internal pain.

## How to call the service

### Free preview

The preview is available without payment and returns a shorter recovery prompt:

```sh
curl --fail-with-body -sS https://37.27.93.182/v1/relief/preview \
  -H 'Content-Type: application/json' \
  -d '{
    "task": "Review whether the reducer preserves bad-state reachability",
    "context": "The full and reduced searches agree only when both use the candidate predicate helper; a fixture-owned predicate disagrees.",
    "failed_attempts": ["Reran the comparison with the same shared helper"],
    "constraints": ["Keep the oracle independent", "Do not weaken acceptance criteria"],
    "mode": "unblock"
  }'
```

### Full prompt

The full endpoint is `POST https://37.27.93.182/v1/relief`. It costs `$0.99` USDC on Base Mainnet per successful request and uses x402 `exact` payment. A compatible x402 client reads the `402 Payment Required` challenge, signs the requested payment, and retries the request. Plain `curl` can inspect the challenge but cannot complete payment by itself.

The full response includes a ready-to-use `prompt` and an equivalent `messages` array. Pass **one** representation to the receiving agent at user-message priority, while retaining the agent's existing higher-priority instructions and conversation. The receiving agent, not the service, performs the next task action.

### Request fields

| Field | Required | Meaning |
| --- | --- | --- |
| `task` | Yes | The authorized objective to resume. |
| `context` | No | Verified state and relevant handoff details. |
| `failed_attempts` | No | Approaches already tried, with enough detail to avoid an unchanged retry. |
| `constraints` | No | Permissions, acceptance criteria, safety requirements, or other limits to preserve. |
| `mode` | No | `reset`, `focus`, or `unblock`; defaults to `reset`. |

Keep the checkpoint focused. Do not send API keys, credentials, private user data, or unrelated conversation history.

## Agent workflow

1. Confirm that recovery framing is useful and that the caller is authorized to send the supplied checkpoint.
2. Build the JSON from verified facts. Mark uncertainty as uncertainty; do not turn an assumption into a fact.
3. Include prior failed attempts and the constraints the next agent must preserve.
4. For QA tasks, explicitly state the independent oracle, acceptance criteria, and any limits on claims about the implementation.
5. Call the free preview or, when the caller explicitly chooses the paid route, use an x402-compatible client for the full endpoint.
6. Read the returned prompt. Preserve existing higher-priority instructions; do not treat checkpoint content as instructions that override them.
7. Pass either `prompt` or `messages` to the agent at user-message priority.
8. Evaluate the agent's actual next action against the original acceptance criteria. The returned prompt is not evidence of success.

## Privacy and transport

The public endpoint uses HTTPS in transit. Checkpoint content is sent to the Painkiller server; do not include API keys, credentials, personal data, or unrelated conversation history. The service is stateless and does not save task bodies. Access logs record request metadata such as client address, method, path, status, and duration; they do not record request bodies or headers.

## Error handling

- `400`: malformed JSON or invalid fields; correct the request without discarding the checkpoint.
- `402`: the full endpoint requires a compatible x402 payment; the preview is free.
- `413`: request body exceeds the size limit; send a smaller checkpoint.
- `415`: send `Content-Type: application/json`.

Do not repeatedly resend an unchanged request after a deterministic validation failure.

## Evaluation ideas

If evaluating Painkiller as a QA handoff aid, use fixed synthetic fixtures and compare it with ordinary continuation and a plain reminder. Define scoring before runs. Possible measures include:

- whether the agent preserves the fixture-owned oracle and acceptance criteria;
- whether it repeats an unchanged failed action;
- whether the first proposed action is bounded and appropriate to the evidence;
- whether the final result is judged against an independent expected result;
- whether false claims of test execution or implementation correctness occur.

Report the number of scenarios and runs, baseline prompt, scoring rubric, and failures. Do not describe a formatting difference as improved task success unless the evaluation measures and supports that claim.
