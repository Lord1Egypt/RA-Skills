---
name: map-the-work
description: >
  Part of the Overpowered skill suite. Build an evidence-aware current-state map of how work actually happens across people, systems, decisions, handoffs, exceptions, and tacit rules. Use when a business process must be understood before improvement, redesign, or automation.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "2-process-automation"
  version: "0.4.0"
---

# Overpowered / Map the Work

## Core rule

**Map how work currently happens, not merely how documentation says it should happen, and do not redesign it unless asked.**

Current-state understanding is independently useful. This skill is not a mandatory precondition for automation when the process is already sufficiently clear.

## Mapping protocol

1. **Set the boundary.** Name the trigger/start, intended outcome/end, scope, and actors/systems in scope. Do not silently expand to the whole organization.
2. **Gather available evidence.** Inspect procedures, forms, spreadsheets, tickets, logs, messages, screenshots, examples, data dictionaries, and prior maps before interviewing unnecessarily. Discoverable facts should not become questions for the user.
3. **Keep three views separate:**
   - `DOCUMENTED`: what policy or procedure says should happen;
   - `OBSERVED / EVIDENCED`: what artifacts, data, and examples show happens;
   - `REPORTED / TACIT`: what people say they do or decide.
   Do not silently collapse disagreements; use `reconcile` if a material conflict must be resolved.
4. **Map the flow.** Capture trigger, inputs, activities, decisions, handoffs, actors, systems, data/artifacts, and outputs without optimizing them.
5. **Expose invisible work.** Look for queues, waits, re-entry, rework, duplicate entry, manual reconciliation, copy/paste, shadow spreadsheets, out-of-band messages, escalation, tacit judgment, approvals, late/missing inputs, system boundaries, and local workarounds.
6. **Map variants proportionately.** Identify common variants and material exception families. Route complex branch modeling to `find-the-exceptions` rather than duplicating it.
7. **Mark evidence status.** Classify important claims as `confirmed`, `inferred`, `reported`, or `unknown`. An interview report is not established truth without corroboration.
8. **Identify friction without redesigning.** Record delays, rework, ambiguity, duplicate handling, error-prone transfers, poor traceability, bottlenecks, and unnecessary intervention. Keep current-state observation distinct from future-state recommendation.
9. **Test sufficiency.** Stop when the map supports the user's next decision. If automation follows, use `find-the-exceptions` only when branches require it, then `automate-this`.

## Output contract

```text
Process
<name + boundary>

Trigger
...

Outcome
...

Current-state flow
1. ...

Decisions
- decision / actor / input / rule or judgment

Handoffs
- from → to / artifact / failure risk

Systems & data
- ...

Variants / exceptions
- ...

Tacit work
- ...

Friction
- ...

Evidence status
- confirmed:
- reported:
- inferred:
- unknown:

Material gaps
- ...

Ready for next step?
YES / NO — <conditional next skill or missing evidence>
```

Keep the representation proportional to process complexity.

## Gotchas

- Do not equate the documented process with actual practice.
- Do not treat a single interviewee's account as confirmed truth.
- Do not optimize, redesign, or automate while claiming to map current state.
- Do not produce a decorative flowchart that omits handoffs, waits, rework, tacit judgment, or evidence status.
- Do not demand exhaustive discovery when the map already supports the next decision.
- Do not remap a complete current-state specification before direct automation.

## Stop condition

Stop when the bounded flow, material variants, invisible work, evidence status, friction, and gaps are clear enough for the user's stated next step.
