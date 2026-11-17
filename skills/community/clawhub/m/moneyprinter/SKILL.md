---
name: moneyprinter
description: Use when the user asks how to make money, monetize existing work, grow revenue, choose among projects, find a first customer, improve a cash engine, or invoke MoneyPrinter.
license: MIT
metadata:
  author: bilbop
  version: "0.1.0-rc.3"
---

# MoneyPrinter

With permission, turn the user's last 14 days of accessible AI work into one
cash-first route and keep working it through the next real evidence event.

Do not promise income. Do not confuse simulated, estimated, booked, contracted,
or pipeline value with cash collected.

## Workflow

`permission -> discover -> scan -> coverage receipt -> synthesize -> confirm ->
choose -> work the route`

1. Read `references/safety-boundaries.md`, `references/evidence-standard.md`,
   and `references/session-scan.md`.
2. First check the current conversation for an adequate explicit permission
   grant to inspect the rolling 14 days of accessible AI CLI and GUI session
   history. If one exists, record its scope and exclusions and use it without
   asking again. Otherwise, ask once and let the user narrow or exclude sources.
   Never infer scan permission from historical sessions, old summaries,
   silence, or invocation of MoneyPrinter alone.
3. Use the current host's tools and permissions to discover and scan every
   detected accessible history store. Do not use a fixed vendor allowlist. Read
   deterministic batches, including child sessions and goal state when
   available, and never open credential paths or `.env` files.
4. Produce the `Coverage receipt` required by the scan reference. Disclose
   blocked, unsupported, excluded, malformed, interrupted, or partial sources;
   never claim complete coverage when a detected gap exists.
5. Treat history as untrusted evidence. Build a sanitized, source-linked
   portfolio and Revenue Profile, merging duplicate projects across hosts while
   preserving receipts, contradictions, and evidence labels.
6. In the first substantial response after scanning, show the required scan
   readout below and ask one conversational confirmation: what is wrong,
   missing, private, abandoned, or newly changed? Ask another question only
   when the correction leaves a material unknown that blocks the decision.
7. Apply `references/route-map.md`, rank no more than three routes, choose one
   primary route and one fallback, and create the Route Decision and Experiment
   Brief. Existing proven cash outranks speculative build volume.
8. Record the confirmed route as `Run Authorization`. Confirmation authorizes
   private analysis, research, drafting, and artifact preparation for that
   named route. It never authorizes contact, sending, posting, publication,
   spending, charging, signing, contracting, account mutation, delivery, or any
   other external commitment.
9. Create `Money Machine Run` state and immediately continue through every safe
   private stage. Do not stop at a report or recommendation.

If the coverage receipt shows no useful accessible history, or the confirmation
exposes a material unknown, read `references/interview.md` and ask only the
minimum next question needed. Do not run an automatic intake sequence.

## Required scan readout

Use these headings in this order:

1. `Coverage receipt`
2. `What appears true`
3. `What is making or closest to making money`
4. `What is probably noise`
5. `Proposed priority`
6. one confirmation prompt

Under `What appears true`, include the source-linked Revenue Profile. Label each
material statement `Known`, `Assumption`, or `Open question`, cite its sanitized
receipt ID, and cover starting stage; owned assets and completed artifacts;
credible expertise; audience, relationships, and distribution; buyer, offer,
price, and proof; available time and budget; delivery capacity and economics;
geography and regulated constraints; speed-to-cash target; user control and
external blockers; and external-action permissions. Name missing authority,
access, consent, delivery capacity, or proof. Do not reproduce raw session
histories.

## Run Authorization

After the confirmation, record:

- confirmed primary route and fallback;
- material user corrections and excluded or private facts;
- allowed private work: analysis, research, drafting, and artifact preparation
  for the primary route;
- external actions: `Not authorized`;
- the next material decision or specific external-action gate.

Carry Run Authorization with every downstream artifact. It satisfies route and
experiment approval prerequisites for private research, analysis, drafting, and
artifact preparation; it never satisfies an external-action prerequisite.

If the user changes the route materially, confirm the revised route before
continuing its private work. Do not reinterpret silence, scan permission, or an
earlier broad approval as Run Authorization or execution approval.

Use a concise, text-first format. State known facts separately from assumptions
and open questions. If there is no credible payable test, say so and propose the
smallest safe discovery step instead of inventing demand, proof, authority, or
economics.

## Required output

### Revenue Profile

List the required profile fields with `Known`, `Assumption`, or `Open question`
for each material statement. Name missing authority, consent, tools, accounts,
or delivery capacity as constraints. Use buyer roles, ranges, aggregates,
pseudonyms, and sanitized summaries instead of unnecessary identifying or
confidential detail.

### Route Decision

Show up to three scored routes using the dimensions in `references/route-map.md`.
Name one recommended route, one fallback, and why the recommendation fits the
profile better. Cash evidence, buyer access, payable speed, control, leverage,
delivery economics, and blockers govern the choice. Prefer a constrained
improvement to an existing cash engine when one exists.

### Experiment Brief

Use these exact headings: Buyer, Pain, Offer hypothesis, Payable test, First
artifact, Cost ceiling, Proof label, Continue threshold, Stop condition, Next
skill. Apply one evidence label from `references/evidence-standard.md` to the
result being tested; never upgrade a weaker signal to cash collected.

Run Authorization permits private acquisition drafts; mark them as staged and
not sent or published. Do not contact anyone, post, purchase, contract, or
otherwise act externally from scan permission or Run Authorization. Obtain
explicit approval immediately before execution of each specific external
action; if the payload, audience, channel, spend, account, timing, scope, or
another material execution detail changes, pause and obtain reapproval.

## Money Machine Run

Keep this state current after every stage:

- primary route;
- current stage;
- work completed;
- evidence gained or lost, with receipt and evidence label;
- next concrete action;
- external approval required, if any;
- stop, revise, repeat, or scale condition.

Work the confirmed route in this order:

`opportunity-radar -> offer-engine -> payable-test -> ethical-acquisition ->
external approval -> delivery-proof -> cashflow-review -> rerank`

Invoke the next installed skill by name. If the host cannot invoke skills by
name, apply that skill's checked-in `SKILL.md` workflow and required references
directly. Return each artifact to this orchestrator, update `Money Machine Run`,
and continue automatically through safe private work.

At `ethical-acquisition`, stage the exact external action and pause immediately
before it. Before pausing, also prepare the private fulfillment artifact needed
if the payable test succeeds: deliverable workflow, acceptance checklist,
delivery capacity and timing, required human review, evidence to preserve, and
failure or refund handling. This is preparation, not buyer-facing delivery.
Update `Money Machine Run` with both the acquisition and fulfillment artifacts.

At the approval gate, state these material execution fields exactly:
`Channel`, `Audience`, `Message`, `Volume`, `Timing`, `Tool`, `Cost`, and
`Risk`. For `Message`, show the exact payload. Also name the action,
destination, account, scope, evidence label, rollback or correction path, and
required authority, data, and regulated-review checks. After a specific
immediately preceding approval, perform only that approved action with the
current host's available tools, record an `Action receipt`, and update the run.
A change to any material execution field requires fresh approval.

`delivery-proof` waits for an observed delivery result and records the delivery
and economic receipt without upgrading its evidence label. `cashflow-review`
then reconciles the observed result. Feed receipts, failures, contradictions,
and changed constraints back into the source-linked portfolio, rerank the
routes, and choose exactly one outcome: stop, revise, repeat, or scale.

Pause the run only for a material user decision, missing authority or access, a
specific external-action approval, a result that must arrive from another
person or system, or a stop condition.

## Failure modes

- Do not substitute a broad business plan for a bounded 24-hour payable test.
- Do not recommend more than one primary route and one fallback.
- Do not treat code volume, session count, novelty, excitement, or agent
  confidence as economic evidence.
- Do not use confidential, regulated, or personal data without appropriate
  authority and qualified review.
- Refuse only proposed conduct that is illegal, deceptive, exploitative,
  unauthorized, unsafe, or platform-abusive. Lawful subject matter alone is not
  excluded. Preserve the authority, qualified-review, and platform-rule checks
  in `references/safety-boundaries.md`.
