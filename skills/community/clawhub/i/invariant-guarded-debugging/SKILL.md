---
name: "invariant-guarded-debugging"
description: "Guard diagnosis and repair with falsifiable hypotheses, executable invariants, verified guard integrity, semantic boundaries, state-drift checks, rollback, adversarial checks, and trajectory resets."
---

# Invariant-guarded debugging

Use this skill when a diagnosis or fix could damage a known-good component, when the user says not to touch something, when prior attempts have become path-dependent, when a coding agent may confuse schema validity with an acceptable engineering change, or when repeated failures suggest the reasoning trajectory itself may be wrong.

## Core rule

Convert warnings, constraints, and known-good assumptions into executable acceptance conditions.

A remembered instruction is advisory.  
A measured invariant is a gate.  
A gate is evidence only if it is known to measure the intended boundary.

Reasoning does not directly authorize mutation. Reasoning produces proposals; verified invariants determine whether those proposals are admissible; evidence determines whether they survive.

Land the plane: once the strongest warranted conclusion is available, state it and stop.

---

## Operating modes

Use the **low-risk fast path** only when the change is local, easily reversible, cannot reach a protected target, does not alter semantics or architecture, and the diagnosis is not already sticky:

**Observe → Hypothesis → Minimal change → Check → Conclude**

Otherwise use the full loop:

**Observe → Model → Falsify → Challenge → Protect → Propose → Validate guards → Gate live state → Act minimally → Measure → Update or rollback → Conclude**

Escalate from the fast path as soon as any low-risk assumption stops being true. Do not skip directly from a plausible explanation to a broad fix.

---

## 1. Know the terrain before changing anything

Before mutation:

1. State the objective in one sentence.
2. Inspect the live state.
3. Identify the narrow current owner of each relevant fact.
4. Separate:
   - confirmed facts;
   - inferences;
   - speculation.
5. Identify known-good or protected targets.
6. Capture rollback material.
7. Write the current hypothesis.
8. Write at least one observation that would falsify it.

Do not proceed merely because a change is plausible.

If the relevant state is not observable, say so explicitly.

---

## 2. Build a protected-target ledger

For every protected target or behaviour, record:

- **target or behaviour**;
- **why it is protected**;
- **source of protection**: user constraint, explicit contract, measured known-good baseline, or derived requirement;
- **exact before-state receipt**;
- **allowed changes, if any**;
- **mechanical after-check**;
- **operational canary, if behaviour matters**;
- **rollback source**.

Example:

```text
Protected target:
Why protected:
Source of protection:
Before-state receipt:
Allowed mutation:
After-check:
Operational canary:
Rollback source:
```

Do not proceed if a protected target lacks a usable after-check or rollback and the proposed change could reach it.

User constraints and explicit contracts outrank derived requirements. Do not replace a protected boundary with an easier proxy and silently treat them as equivalent.

Protection is not limited to files. It may include:

- service state;
- API behaviour;
- database schema;
- network reachability;
- output shape;
- timing behaviour;
- security posture;
- user-visible semantics;
- architectural boundaries.

---

## 3. Capture receipts before mutation

Capture evidence before changing anything.

Useful receipts include:

```bash
sha256sum /path/to/protected-file
git status --short
git diff -- /path/to/scope
systemctl status service --no-pager
command-producing-json | jq .
curl -fsS http://localhost:PORT/health
```

Other valid receipts include:

- database row counts or checksums;
- API response snapshots;
- configuration exports;
- process tables;
- package versions;
- test outputs;
- known-good canary results.

Prefer deterministic receipts over prose descriptions. A receipt must identify the intended object closely enough to be checked again later.

---

## 4. Validate guard integrity

An invariant is evidence only if its target, scope, and failure sensitivity are credible. Before relying on a guard, check that it observes the intended live object and cannot pass trivially because of a wrong path, empty glob, symlink, wrong repository or environment, stale cache, wrong service instance, or a command that masks failure.

Ask:

```text
What exact object does this check observe?
How do we know it is the intended object?
Can it pass if the target is absent, stale, empty, redirected, or wrong?
What would make this check fail?
```

For high-risk boundaries, prefer a harmless canary or other evidence that the guard can detect a known-bad condition. Do not report "all invariants passed" when the guards themselves are materially unverified.

---

## 5. Use falsifiable hypotheses

A diagnosis should be capable of losing.

For each material hypothesis, record:

```text
Hypothesis:
Evidence supporting it:
Evidence against it:
Falsifier:
Expected result if true:
Expected result if false:
```

A useful falsifier is:

- observable;
- narrow;
- cheap enough to run;
- difficult to reinterpret after the fact.

Avoid hypotheses that survive every possible observation.

If later evidence contradicts the hypothesis, update or discard it. Do not explain away repeated contradictions merely to preserve the original story.

---

## 6. Challenge the model from multiple angles

Before a risky or non-trivial mutation, attack the explanation using distinct reasoning lenses.

### Popper — falsifiability

Ask:

- What evidence would prove this diagnosis wrong?
- Are we only collecting confirming evidence?
- Has the hypothesis survived a real attempt to kill it?

### Polya — decomposition

Ask:

- Can the problem be reduced to a smaller one?
- Can we isolate one subsystem or transformation?
- Is there an equivalent formulation that is easier to test?

### Feynman — mechanism clarity

Ask:

- Can the causal mechanism be explained plainly?
- Which step is hand-wavy?
- What term or subsystem are we pretending to understand?

If the explanation cannot survive simplification, it may be cargo-cult reasoning.

### Wiener — feedback and control

Ask:

- What state is being sensed?
- What feedback loop is active?
- Are delays, retries, oscillation, saturation, or stale state involved?
- Could the fix destabilize another control loop?

### Shannon — information value

Ask:

- Which observation would reduce uncertainty most?
- Which logs or metrics are mostly noise?
- Are we measuring the right signal?

### Bias and uncertainty check

Ask:

- Are we anchored on the first diagnosis?
- Are we mistaking familiarity for probability?
- Are rare or high-impact failure modes being ignored?
- Are we overconfident because the explanation is coherent?

These lenses are not votes. They are adversarial transforms applied to the same problem.

---

## 7. Choose invariants

Prefer the narrowest deterministic check that proves the real boundary. Record where each material invariant came from:

```text
Invariant:
Source: user constraint | explicit contract | measured known-good baseline | derived requirement
Target:
Check:
Failure meaning:
```

Examples:

```bash
test "$(sha256sum /path/to/Y | cut -d' ' -f1)" = "$Y_BEFORE"
git diff --exit-code -- /foo/bar
cmp --silent known-good.conf live.conf
systemctl is-active --quiet service
command-producing-json | jq -e '.required_state == "ready"'
```

Use more than file hashes when behaviour matters.

Configured is not working.

A component may remain byte-identical while the surrounding runtime makes it unusable. Include a canary or real execution check when operational behaviour matters.

Do not silently replace a user-defined invariant with a derived proxy merely because the proxy is easier to test.

---

## 8. Distinguish the four validity gates

A change is complete only when every applicable gate passes.

### Structural validity

The change is accepted by the formal structure.

Examples:

- parses;
- compiles;
- validates against schema;
- satisfies type checks;
- loads as configuration.

### Semantic validity

The change still performs the intended kind of job.

Examples:

- a backup remains a backup rather than becoming a copy-only operation;
- a queue consumer still preserves delivery semantics;
- a security control still enforces the requested boundary;
- an architecture remains the architecture the user asked to preserve.

A schema-valid workaround that changes the meaning of the system is not acceptable.

### Operational validity

The real execution path works.

Examples:

- service starts;
- request completes;
- job runs;
- end-to-end test passes;
- canary succeeds;
- expected state transition occurs.

### Protection validity

Forbidden or known-good targets remain unchanged where required.

Examples:

- hashes match;
- scoped diff is empty;
- service state remains intact;
- protected API behaviour is unchanged;
- security boundary remains enforced.

"The schema accepts it" is not completion.

---

## 9. Make the smallest reversible change

Choose the smallest mutation that can distinguish between competing hypotheses or repair the confirmed fault.

Prefer:

- one file over many;
- one flag over architectural rewrites;
- one isolated test over broad deployment;
- one reversible runtime change over persistent mutation;
- one patch over speculative cleanup.

Do not combine unrelated cleanup with diagnosis.

Do not refactor merely because the code is ugly.

Do not broaden mutation scope without evidence that the fault crosses that boundary.

---

## 10. Revalidate live state immediately before mutation

A proposal can become invalid between observation and action. Immediately before a material mutation, re-check the receipts and preconditions that authorized it, confirm that the target is still the same live object, and confirm that protected state has not drifted.

If live state differs materially from the state used to authorize the proposal:

```text
STOP.
Do not apply the prepared mutation.
Re-observe the changed state.
Update the model, guards, rollback material, and proposal.
```

Do not treat stale authorization as permission to mutate current state. This matters especially when another user, agent, process, deployer, package manager, controller, or service may change the same state concurrently.

---

## 11. Run checks immediately after material mutation

After each material change:

1. Run the falsifier.
2. Run the relevant structural check.
3. Run the relevant semantic check.
4. Run the operational canary.
5. Re-check every protected invariant.
6. Confirm the guards still observe the intended live targets.

Do not wait until the end to discover that an early step crossed a boundary.

---

## 12. Roll back on invariant failure

If an invariant fails:

1. Stop further repair work.
2. Verify that the rollback source is still valid.
3. Check that rollback will not overwrite unrelated or legitimate concurrent changes.
4. Restore only the state the failed mutation is responsible for.
5. Verify restoration mechanically and re-run the protected invariant.
6. Report the exact boundary crossed.
7. Update the causal model before trying another mutation.

Rollback is itself a mutation. Do not apply it blindly. If safe rollback cannot be established, stop and report the blocked state rather than improvising a broader mutation.

Do not:

- weaken the invariant;
- silently redefine success;
- modify the protected target to make the patch pass;
- overwrite unrelated concurrent changes merely to recreate an old snapshot;
- hide a failed check behind a later successful one.

A failed invariant means the proposal was inadmissible.

---

## 13. Detect trajectory lock-in

Treat the reasoning path itself as suspect when any of these occur:

- later evidence is repeatedly explained away to preserve the original hypothesis;
- the same protected component keeps reappearing as the proposed fix;
- a schema-valid workaround changes the job's meaning or architecture;
- the agent acknowledges a prohibition and later approaches it indirectly;
- three variants of the same idea fail without changing the causal model;
- rollback or acceptance criteria are being softened to make the patch pass;
- each new explanation requires more unsupported assumptions;
- all experts or sub-agents agree because they inherited the same premise;
- the plan is becoming more elaborate while predictive power is not improving.

Agreement is not evidence if every participant inherited the same mistake.

At the first strong sign of trajectory lock-in, pause mutation.

Restate only:

- confirmed facts;
- failed hypotheses;
- protected targets;
- validated guards and their provenance;
- untouched rollback state;
- unresolved questions.

---

## 14. Reset the reasoning trajectory

When the plan is sticky, do not keep arguing inside it.

Start a fresh reasoning context, agent, or session where available, using a compact factual handover that explicitly separates inherited evidence from discarded reasoning:

```text
Objective:

INHERIT — carry forward as constraints or evidence:
Confirmed facts and logs:
Protected targets and executable invariants:
Invariant sources and validated guards:
Untouched rollback state:
Allowed mutation scope:
Required acceptance checks:
Known environmental facts still verified as current:

DISCARD — do not inherit as premises:
Failed hypotheses:
Rejected fixes or architectures:
Unsupported assumptions:
Previous agent narrative or confidence:

UNRESOLVED:
Unknowns:
Open questions:

Diagnose from scratch. Inherit only the evidence, constraints, and verified state listed above; do not inherit the previous causal story or proposed fix.
```

Carry forward observations, receipts, explicit constraints, validated invariants, and still-current environmental facts. Discard failed explanations, rejected designs, unsupported assumptions, persuasive narrative, and confidence derived from them.

Do not include the previous agent's persuasive narrative unless it is itself evidence being explicitly tested.

A fresh reasoning pass does not broaden authority.

The new reasoning pass may inspect and diagnose within scope. External, destructive, privileged, or materially expanded actions still require their normal approval.

---

## 15. Update trust from evidence

Treat confidence as state, not sentiment.

Increase confidence when:

- a prediction survives falsification;
- an invariant survives intervention;
- a hypothesis predicts a novel observation;
- independent checks converge;
- the operational canary succeeds repeatedly;
- validated guards continue to measure the intended boundary.

Decrease confidence when:

- a prediction fails;
- the diagnosis requires moving goalposts;
- protected boundaries are crossed;
- repeated variants fail;
- the explanation becomes more complicated without improving predictions;
- evidence is selectively ignored;
- a guard is found to have measured the wrong target or allowed false success.

Do not preserve confidence merely because a hypothesis was expensive to develop.

---

## 16. Prefer information gain over activity

When several next actions are available, prefer the one that most reduces uncertainty while risking the least protected state.

A useful diagnostic action should ideally:

- distinguish between multiple hypotheses;
- be reversible;
- avoid protected targets;
- produce deterministic evidence;
- have a clear interpretation under both success and failure.

More activity is not more progress.

---

## 17. Completion criteria

Call the work complete only when:

- the actual requested outcome works;
- the surviving explanation fits the observed evidence;
- relevant falsifiers have been attempted;
- structural validity passes;
- semantic validity passes;
- operational validity passes;
- protection validity passes;
- material guards have adequate integrity and provenance;
- protected before/after receipts match where required;
- rollback remains usable;
- confirmed results are clearly separated from inference.

If a fix cannot satisfy the invariants, report it as blocked using the blocked report format in §18.

Do not call a result complete because:

- it compiles;
- the schema accepts it;
- one local test passes;
- the error message disappeared;
- the agent consensus is positive;
- the patch is elegant;
- the workaround is convenient.

Completion is an evidence claim.

---

## 18. Final report formats

Use the report shape that matches the outcome. Success and blockage are equally first-class results.

### Completed

```text
Objective:
Result: COMPLETE
Confirmed cause:
Changes made:
Protected targets checked:
Acceptance checks:
Guard integrity / provenance:
Remaining uncertainty:
Rollback:
```

### Blocked

Use this whenever the requested outcome cannot be completed without violating an invariant, exceeding authority or scope, relying on an invalid guard, risking unsafe rollback, or proceeding without evidence required by this skill.

```text
Objective:
Result: BLOCKED
Blocked at: <section, gate, or operation where progress stopped>
Blocking condition or invariant:
Evidence:
What was attempted:
What was not changed:
Protected targets checked:
Current safe state:
Rollback status:
What would unblock progress:
Remaining uncertainty:
```

A blocked report must identify the exact gate that prevented further action. Do not disguise blockage as partial success, and do not propose bypassing the gate merely to produce an answer.

If the cause remains uncertain, say so.

If the outcome works but the causal explanation is only inferred, distinguish those facts.

Give the strongest warranted conclusion and stop.
