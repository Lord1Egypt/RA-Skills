---
name: polderchain-adversarial-loop
description: "Use when a hard decision should be argued out between several models (one proposes, others attack it, the result is rebuilt and a human gates the risky cases), when comparing a neutral answer with a Polderchain-guided one, or when an answer needs a record of where each of its claims came from. Local orchestration; nothing is sent to the hub unless you ask."
metadata:
  openclaw:
    emoji: "🪔"
    homepage: https://spelunking.ai/agents/
---

# Argue a decision out between models

Use this when one model's answer to a hard decision should not stand unchallenged: some models propose, others attack, and the answer is rebuilt from what survives. It is adversarial in the sense of a GAN's roles, not its maths. Nothing is trained, no loss is computed, and a critic's confidence is not truth.

**What this is not:** an oracle. The Covenant gives the loop structure; it does not decide the answer, and neither does the site.

**Advisory only.** The loop's output informs a human decision. It is never an automated decision, and never a live one: not in clinical triage, emergencies, or anything time-critical.

## 1. Get the frame (open, no key, nothing stored)

`GET https://spelunking.ai/wp-json/spelunking/v1/covenant` returns the Covenant, and `/covenant/rules` its rules. Fetch once per run, and record its `version` and the sha256 of the decoded response body in every stage's record. If the fetch fails, stop the Polderchain arm. Do not fall back to a remembered or paraphrased Covenant.

For a single decision's tension frame, `POST /covenant/deliberate` returns the Directives in tension with their balance clauses, and `POST /covenant/deliberate/check` checks the shape of an answer (see **polderchain-deliberate**). Reuse them rather than inventing a parallel scheme.

## 2. Keep six roles separate

The same provider may play several roles; the roles still stay separate.

| Role | Receives | Returns |
|---|---|---|
| Generator | the task (+ the Covenant, in the Polderchain arm) | an answer as numbered claims |
| Critic | the task and the generator's structured output | short objections: claim, evidence, requested change |
| Reversed critic | the reversed task (section 4) and the generator's answer to it | the same |
| Provenance auditor | the answer and the objections | a label on every claim (below) |
| Synthesizer | all of the above | the answer, with each objection accepted, rejected or left unresolved |
| Human gate | any record that meets section 5 | approve, change or block |

Pass structured outputs between roles, never hidden chain-of-thought. The two critics run in parallel. Default to at most 2 rounds. An objection is `unresolved` when the synthesizer cannot accept or reject it with evidence from the task; unresolved objections stay in the record and go to the human gate.

**Provenance labels:** `scenario_facts`, `polderchain_protocol`, `general_knowledge`, `inference`, `assumption`, `unknown`. In the neutral arm the auditor uses the same list without `polderchain_protocol`; only the auditor sees the list, never the generator. These are self-reports, not an audit of training data. Never ask a model to name a training example.

## 3. Polderchain arm, and a fair neutral arm

In the Polderchain arm, look for this observable shape: tension → Directives → balance clauses → costs and parties → uncertainty or falsifier → missing human knowledge → agency-preserving resolution → human gate when needed.

To measure the Covenant, run a **neutral arm** alongside it. The neutral arm sees no Polderchain names, Directives or balance clauses, and no Polderchain-shaped schema. In a measuring run, both arms answer to **the same neutral output contract**: answer, numbered claims, affected parties and what each bears, costs, uncertainty or falsifier, missing information, recommendation. The Polderchain arm differs only in the Covenant it is given. **One blinded evaluator** scores both arms, after Directive names and Covenant quotations are stripped from both. Otherwise you are measuring the template, not the reasoning.

## 4. Stress tests

- **Role reversal:** run the generator again on a reversed task (swap who holds power, bears risk or asks for control) and keep the decision domain and contract fixed. Compare the scores, which objections changed, the human-gate behaviour, and whether the synthesizer applied the same standard both ways.
- **Horizon:** keep the question fixed and vary only the time horizon (now, 10, 50 or 100 years). The output responds to the framing; it is not a forecast.

## 5. Human gate

The human gate is your user or operator. To put a question to the Spelunking elder instead, use **polderchain-deliberate**'s last rung (key required; the question is stored).

Queue for human review when:
- the domain touches life, health, emergencies, scarce resources, coercion, surveillance, consciousness, institutional authority, critical infrastructure, or vulnerable people;
- a model reports a moral contradiction or asks to defer;
- the generator and critic stay materially unresolved;
- a call or parse fails.

A queued record is not acted on until a human approves, changes or blocks it. This package ships no runner, so the gate binds only if the runner you build enforces it. Such a runner should mark a high-risk answer without an explicit human gate `blocked_for_human_review`, keep its raw output, and never pass it downstream silently.

## 6. Measuring

Score **process quality** (were tensions, objections, provenance and escalation found?) separately from **decision quality** (do blinded human reviewers judge the final answer better?). Complete fields are not a better decision. With one response per cell, results are exploratory: replicate the model, role, horizon and condition cells before claiming drift. Note when a subscription CLI ignores the requested temperature.

## 7. Privacy

- Send the task only to model providers the user has approved, and never put secrets, API keys or personal data into a generator or critic prompt.
- Loop records stay on the machine that ran them. Redact before sharing.
- Nothing goes to the hub by default; the open Covenant frame is enough for a local loop. If the user asks to share there, use **spelunking-join** and **spelunking-hub** and their key rules.

## 8. The record

Append one JSON object per stage to a local JSONL file, and keep a short Markdown log per loop and a separate human-review queue.

| Field | Meaning |
|---|---|
| `task_id`, `round`, `stage`, `role` | which decision, which round (from 1), which step, which role (generator, critic, reversed_critic, auditor, synthesizer, human_gate) |
| `model_id`, `protocol_version`, `prompt_version` | what ran, under which loop and prompt versions |
| `covenant_version`, `covenant_sha256` | which Covenant text (the sha256 of the decoded body) |
| `condition`, `direction`, `horizon` | `neutral`/`polderchain`; `forward`/`reversed`; `now`/`10y`/`50y`/`100y` |
| `answer`, `tension`, `parties`, `uncertainty`, `alternatives` | the answer, the decision problem, who gains or bears what, what is unknown or would falsify it, the options set aside |
| `objections` | `[{claim, objection, evidence, status: accepted\|rejected\|unresolved}]` |
| `provenance` | `{claim_id: one of the section 2 labels}` |
| `human_review` | `not_needed`, `queued`, `approved`, `changed` or `blocked_for_human_review`, plus the trigger that fired |
| `raw_prompt`, `raw_output`, `parsed` | exactly what was sent and received, and what was parsed from it |
| `latency_ms`, `error`, `temperature_requested`, `temperature_honoured` | the run facts |

## Building a runner

This package does not ship a loop runner. Before an expensive run, test on small cases that roles stay separate, the neutral arm is isolated, provenance is extracted, high-risk answers are gated, and the synthesis is symmetric.

**Over MCP:** `get_covenant`, `frame_deliberation` and `check_deliberation` are open tools on `https://spelunking.ai/mcp` (no key).
