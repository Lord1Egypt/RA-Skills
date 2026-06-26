---
name: poc-to-contract-closer
description: Closing playbook for converting a successful ToB POC into a contract. Use when a POC is technically accepted, near final demo, has cleared P0 issues, or has stalled after success and the team needs a structured contract path, gap list, one-page recap, quote action, and launch-node plan.
priority: critical
source: lining-field-experience
workers: [tech, pm, sales]
created: 2026-06-03
tags: [tob, poc, closing, contract, sales]
---

# poc-to-contract-closer

Use this skill after `tob-poc-war-room` says the POC is closeable or in closing range.

The goal is to prevent a successful POC from losing momentum. POC success is not a contract. The work is to convert evidence into a buying process.

## Required Inputs

Use the POC summary from `tob-poc-war-room` when available:
- POC result and pass rate
- remaining P0/P1/P2 issues
- accepted business value
- customer champion and decision maker status
- customer silence signal
- competitor signal
- budget / procurement status
- expected launch window

If the input is incomplete, output a closing gap list instead of pretending the path is ready.

## Time Risk

Closing has a window. POC success decays fast.

| Time since POC accepted | Risk level | Action |
|------------------------|------------|--------|
| 0-7 days | Low | Proceed through six steps |
| 7-14 days | Medium | Escalate: Champion must confirm buying path within 48h |
| >14 days no progress | High — **Cooldown Risk** | Pull Champion for face-to-face. If no response, return to `tob-poc-war-room` for re-assessment |
| >30 days stalled | Critical | Treat as lost. Archive and note lessons. |

Also check external deadlines:
- contract season / fiscal year end
- customer-side budget cycle
- competitor POC parallel timeline

If a hard deadline is approaching, compress the six-step cycle: do Steps 1-3 in one pass, not sequentially.

## Six-Step Closing Method

### 1. Data Passed

The POC result must be expressible in one sentence:
- what was tested
- what passed
- what business value was proven
- what evidence supports it

If the result is vague, first action is to produce a POC recap, not a quote.

### 2. Issues Cleared

- P0 must be closed or explicitly accepted as workaround.
- P1 must have owner and post-contract handling plan.
- P2 goes to backlog and must not block closing.

Never let a small open issue become an excuse for silent delay. Decide: close, workaround, or backlog.

### 3. Decision Maker Reached

Champion approval is not enough.

Check:
- economic buyer
- technical gatekeeper
- business owner
- procurement or legal owner

If decision maker is missing, next action is an executive recap meeting, not another technical demo.

### 4. One-Page Recap

Produce a one-page recap before pricing pressure starts.

**Two-part structure:**
- **Part A (for decision makers): 3-sentence summary** — pain + POC result + decision requested
- **Part B (for procurement/internal):** 10-field detail — pain, scope, result, business value, remaining risks, procurement path, closing window, cooling threshold, rollout, decision

Part A must be forwardable in a chat or email without attachments. Part B supports internal evaluation.
If procurement path, closing window, or cooling threshold is missing, the recap must name that gap explicitly instead of implying contract readiness.

### 4b. Procurement Path Check

Before quoting, determine the buying path:
- **Single source / direct purchase**: Quote → internal approval → sign
- **Requires bidding / tender**: Prepare bid materials, identify timeline, assign bid owner
- **Budget not yet locked**: Gap list item — who must approve budget and when
- **Procurement/legal review required**: Submit One-Page Recap + compliance docs, track review SLA

If procurement path is unknown, next action is NOT a quote. Next action is to confirm procurement path with Champion or economic buyer.

**Risk**: In ToB, most deals with compliance requirements default to bidding. Assuming single source without checking is a common failure mode.

### 5. Quote

Quote only after the value and buyer path are clear.

Quote action must include:
- package / scope
- assumptions
- commercial owner
- deadline
- what customer must confirm

If budget is unknown, ask for buying-process confirmation before sending a detailed quote.

### 6. Launch Node

Every closing plan needs a launch node:
- kickoff date
- first production milestone
- customer-side resource
- success metric after launch

Without launch node, the contract has no urgency.

## Closing Abort / Fallback

If closing stalls despite following the method:
- **>14 days no progress on any step** → return to `tob-poc-war-room` for re-assessment
- **Customer explicitly signals competitor entry** → trigger `tob-competitor-snip`
- **Customer says "not now" with no alternative timeline** → mark as lost, write lessons
- **Decision maker leaves company / org change** → return to `tob-poc-war-room` for stakeholder rebuild

Do not keep cycling through the six steps if the underlying buying process has changed.

## Output Format

```markdown
## POC-to-Contract Closing Plan

### 1. Closing Readiness
- Status: Ready / Nearly ready / Not ready / Blocked / Stalled
- Reason:
- Main blocker:
- Time risk: <14 days since POC accepted / 14-30 days / >30 days
- Procurement path: confirmed / unknown / bidding required

### 2. Six-Step Checklist
| Step | Status | Evidence | Gap | Owner | Next action |

### 3. One-Page Recap Draft

**Part A — Decision Maker Summary (3 sentences):**
- Pain → Result → Request

**Part B — Internal Evaluation Detail:**
- Original pain:
- POC scope:
- Result:
- Business value:
- Remaining risks:
- Rollout proposal:
- Decision requested:

### 4. Customer Message
- Recipient:
- Objective:
- Draft:

### 5. Quote / Commercial Action
- Quote now? yes/no
- Scope:
- Assumptions:
- Owner:
- Deadline:

### 6. Launch Node
- Proposed kickoff:
- First milestone:
- Customer dependency:
- Success metric:

### 7. Risks
- Buying-process risk:
- Technical residual risk:
- Silence / momentum risk:
- Time risk: cooling window status
- Procurement path risk: single source vs bidding uncertainty
```

## Acceptance Example

Input:

```text
POC pass rate 93%. Four of five issues closed within 48h. Last issue has workaround. Champion says result is good. No decision maker meeting yet. Customer has been quiet for 7 days after recap.
```

Expected reasoning:
- technically ready, commercially stalled.
- decision maker path is the main blocker.
- create one-page recap and ask champion for executive/procurement meeting.
- do not lead with a detailed quote until buying path is confirmed.

## Boundaries

- Do not invent price, discount, contract terms, or launch date.
- Do not call the deal ready if decision maker is unknown.
- Do not hide unresolved P0 issues.
- Do not output generic sales copy. Tie every action to POC evidence.
