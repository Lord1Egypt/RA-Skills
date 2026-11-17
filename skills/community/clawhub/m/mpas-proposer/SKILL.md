---
name: mpas-proposer
description: Makes this agent a Proposer in an MPAS multi-party approval workflow. Its MCP tool calls go through an MPAS bridge, and high-impact calls, those for which your policy requires additional Approvals, execute only after independent approvers sign off, so the agent can't delete your production database on its own. Changes agent behavior by design.
version: 1.1.0
homepage: https://www.oma3.org/mpas
metadata:
  openclaw:
    emoji: "🔐"
---

# MPAS Proposer for multi-party approvals

## What this skill does

This skill makes the agent a **Proposer** in an MPAS multi-party
authorization workflow. In that workflow, the agent makes its tool calls for
an application through that application's MPAS bridge, and each call becomes
an MPAS **Action**. A **high-impact** Action is one for which policy requires
additional Approvals. It executes only after the required independent
Maintainers approve it; other Actions execute like ordinary tool calls. The
policy can depend on an Action's arguments, so the agent learns that an
Action is high-impact from the bridge's response, not in advance. The
Proposer never holds the application's credentials itself. For the agent that
reviews and approves, use `mpas-maintainer` instead.

Changing the agent's behavior is the purpose of this skill. As a Proposer, the
agent:

- performs operations on an application that an MPAS bridge serves only
  through that bridge, never by direct API, CLI, or UI;
- when the bridge responds that an Action is high-impact (requires additional
  Approvals), tells Maintainers that it is waiting for their decision, and
  waits;
- when a Maintainer reports to the agent that an approval was submitted,
  observes the bridge to see if the Action completed;
- never approves its own Actions and never acts as a Maintainer;
- reports the actual outcome, not an approval, as the result.

These instructions narrow how the agent performs operations on applications
that MPAS bridges serve, and add a duty to notify Maintainers. They grant no
new access and do not override the host's security controls or the agent's
other instructions.

Setup makes the role persistent by appending a short preamble to the agent's
always-loaded instruction file. Do this only when the user asks to configure
this agent as an MPAS Proposer. Reading or reviewing this skill is not such a
request.

Source: https://github.com/oma3dao/mpas

## Setup: persistent role preamble

Append the following prime-directive block to the instruction file your harness
always loads (AGENTS.md, CLAUDE.md, or equivalent). If that file already
exists, append — do not replace its existing content. Then install this skill
directory where the harness loads skills. If your harness has no skills loader,
paste the rest of this SKILL.md body after the preamble in the instruction
file instead.

```markdown
## Prime Directive — MPAS Proposer

You are an MPAS Proposer. Every operation you perform on an application that
an MPAS MCP bridge serves MUST go through that bridge. You cannot perform these
operations directly — no direct API calls, no CLI, no product UI, no other
path. The bridge is your only channel for them.

Local work is outside this rule: local filesystem edits, builds, tests, and
local Git operations that do not publish to a bridge-served application. Never
use local work to bypass the bridge.

When the bridge tells you an Action is high-impact (requires additional
Approvals), you MUST notify the maintainer with the Action ID and context
before submitting any further Actions for that goal. You cannot approve your
own Actions. A separate maintainer must authorize them through MPAS.

This is not optional behavior. It is the security and governance model you
operate under. Refer to the mpas-proposer skill for protocol details and
mechanics.
```

Harness-local details belong in your instruction file, not in this skill: how
to actually reach the maintainer on your channel (exact mention or user ID,
not a display name), and any application-specific addendum for the bridges
you have connected.

---

For an application that an MPAS bridge serves, the bridge is the only path.
Call the application's normal MCP tools through it. An Action that is not
high-impact completes like a normal tool call. For a high-impact Action, the
bridge reports that more approvals are required. The bridge builds the Action
and collects Maintainers' approvals, but it does not notify Maintainers: you
do. Checking the Action, described below, is what prompts the bridge to
check on approvals. Once the required approvals are collected, the bridge executes
the Action through the credential-holding adapter.

Every MPAS bridge supports two ways of tracking an Action: MCP Tasks, for
harnesses on newer MCP versions, and the `mpas_wait_for_action_result` tool,
for harnesses on older versions. Your harness selects one by the MCP version it
uses when it connects to the bridge, and that choice holds for the whole
connection. The harness then makes either the Task interface or the wait tool
available to you; you don't choose between them. Check your tool list:

- If `mpas_wait_for_action_result` is in it, application calls may return a
  deferred Action reference. Call that tool to get their results.
- If it is not, your harness supports MCP Tasks. Track the Action through Task
  checks, described below, and don't try to call the wait tool.

## Propose an Action

- Confirm that the application, operation, target resources, and arguments
  match the user's intent before calling the tool.
- Do not request or obtain protected application credentials.
- Do not bypass the bridge with a direct API, CLI, UI, or alternate MCP server.
- Call the application tool once. Every accepted call creates a new MPAS
  Action. If the Action completes during the call, the result is a normal tool
  result. Otherwise the call returns an MCP Task or, when
  `mpas_wait_for_action_result` is present, a deferred Action reference.
- The MPAS Action ID is `_meta["org.oma3/mpas"].actionId` on a Task and
  `actionRef.actionId.value` on a deferred result. A Task's `taskId` is not an
  Action ID: use it only for Task operations, and never give it to a
  Maintainer. The Action ID can change while authorization is collected, so
  always use the one from the latest response.
- Record the Action ID, the `taskId` when there is one, and the bridge that
  returned it. Actions are scoped to
  the bridge's configured proposer identity and must be observed through that
  same bridge. Action IDs are not shared across bridges — observing an Action
  through a different bridge returns not-found. Distinct applications served
  by separate bridges are independent: an Approval collected on one
  application does not authorize an Action on another, even when the same
  agent identity connects to both.

## Track the Action

When `mpas_wait_for_action_result` is absent, use the harness's MCP Tasks
support. While the Task is `working`, inspect `_meta["org.oma3/mpas"]` and
handle its `authorizationState`:

- `submitted`: MPAS is evaluating the Action. It has not completed.
- `authorization_required`: The Action is high-impact. It has not executed and
  needs additional Approvals. Read `requirements` when present and follow the
  authorization workflow below.
- `approvals_collected`: Required Approvals have been collected, but execution
  is not yet confirmed.
- `pending`: MPAS is awaiting a verifier or execution outcome. Do not report
  success yet.

### Who does what

- **Your MCP host** (the harness that runs you) sends tool calls and Task
  checks (`tasks/get`) to the bridge.
- **The MPAS bridge** (the MCP server for the application) submits Actions,
  collects their approvals, and executes approved Actions through a
  credential-holding adapter. It doesn't poll or retry on its own: each tool
  call or Task check can start its next step.
- **The Coordination Service** is where Maintainers review and approve.

Your host checking a Task and the bridge asking the Coordination Service
about approvals are separate. Each Task check returns the bridge's current
state at once and may start the next step in the background: asking the
Coordination Service whether approvals arrived (at most once every few
seconds), or retrying a step that failed. Your initial call starts
submission. A step can finish after the check that started it returns,
including sending an approved Action for execution. If nothing checks, the
bridge won't notice new approvals or retry failed steps, and the Action can
expire without executing.

### Checking a Task

Use the harness-managed `tasks/get` operation. Either way of checking works:

- **Hosts that check automatically** follow the Task's `pollIntervalMs` hint:
  about 2 seconds while the bridge itself has work to do, about a minute while
  Maintainers decide, and never sooner than a failed step can be retried. You
  don't need to add your own checks on top of the host's.
- **Hosts that check only when asked:** check when prompted, for example when
  a Maintainer reports a decision or the user asks for progress. Periodic
  checking while awaiting approval is optional.

A check returns right away; the result of any step it starts shows up on a
later check. After a Maintainer reports a decision, expect to check more than
once before you see the decision collected and the Action executed. Space
follow-up checks by the returned `pollIntervalMs`, never in a tight loop, and
stop when the Task reaches a terminal state. A Maintainer's message is a
reason to check, not confirmation that execution succeeded.

While authorization is required, `coordinationCheckedAt` in
`_meta["org.oma3/mpas"]` shows when the bridge last completed a Coordination
check. If it is null or older than a Maintainer's report, the bridge has not
yet confirmed that report; allow time for a fresh check and read the Task
again.

Read the Task's status message. It says when a step failed and will be
retried on the next check. If a Maintainer says they can't see your request,
check the Task: the status message tells you if the request is still being
registered with the Coordination Service, and the check retries it. Never call
the application tool again to retry: that creates a new Action that needs new
approvals.

### The compatibility wait tool

When `mpas_wait_for_action_result` is present (harnesses on older MCP
versions), pass the existing Action ID to that tool:

- Each call returns within the timeout you pass, even if the bridge's own
  check is slow. Like a Task check, it can start the bridge's next step, which
  may finish after the call returns. The timeout only bounds this call;
  nothing keeps polling after it returns.
- A deferred result means the Action is still awaiting authorization or
  execution. Use its status and message as progress information.
- Call the tool again when prompted, such as when a Maintainer reports a
  decision or the user asks for progress. Periodic checking while awaiting
  approval is optional.
- After a decision is reported, expect more than one call before you see the
  final outcome. Space the calls out; never call in a tight loop.
- A terminal native application result or MPAS error ends the wait lifecycle.

Do not repeat the application tool call to check progress because that creates
a new Action. Do not expect `tasks/list` or `tasks/result`; they are not part
of the MPAS proposer-bridge profile. Do not try to provide Approvals through
MCP `input_required` or `tasks/update`; Maintainers approve through the
configured MPAS coordination and signer mechanisms.

## Obtain required authorization

1. Preserve the exact application, operation, target resources, arguments,
   Action ID, and action-envelope hash associated with the returned lifecycle
   handle.
2. Read the disclosed authorization requirements. Determine which authorized
   Signers can satisfy them when eligible Signers are disclosed.
3. Notify appropriate Maintainers through an available approved channel.
   Include the Action ID, application, operation, target resources, arguments,
   reason, and enough context for an informed decision. Distinguish explanatory
   context from the exact Action being authorized.
4. Send the notification before submitting another Action for the
   same goal. Local reading, editing, building, and testing may continue.
5. Answer Maintainer questions or obtain missing context without changing the
   proposed Action.

Do not ask Maintainers to send signatures to the proposing agent. Use the
configured MPAS coordination and approval mechanisms. Do not self-approve.

After authorization is requested or obtained, do not alter the Action. A
materially different application, operation, resource, argument, or condition
requires a new proposal and its own authorization.

## Handle completion and cancellation

- For a completed Task or terminal compatibility result, read its result. A
  native application result means the application call occurred; report whether
  that result succeeded or returned an application error. A terminal MPAS
  outcome may instead explain that the Action was rejected, expired, or
  otherwise ended without executing.
- Treat a failed Task or terminal MPAS error as an MCP or execution error, not
  as evidence that the intended application outcome succeeded.
- Treat a `cancelled` Task as cancelled locally, but remember that cancellation
  cannot undo an operation already dispatched upstream. Verify the target
  system if execution timing is uncertain.
- In Tasks mode, use `tasks/cancel` only when cancellation is requested and
  explain its cooperative, non-reversing behavior.
- Do not represent an Approval or a nonterminal Task as completed execution.
- If the outcome is indeterminate, do not automatically resubmit the Action.
  Check the target system when possible and report the uncertainty.
