# Proof Loop Adoption Kit

Use this when a coding agent is about to do work that needs a hard done gate.

## 1. Create the Task Folder

From the Proof Loop repo:

```bash
bin/proof-loop init TASK_ID --title "One sentence task title" --root /path/to/project
```

This creates:

```text
.agent/tasks/TASK_ID/
  spec.md
  evidence.md
  verdict.json
  problems.md
```

## 2. Freeze the Acceptance Criteria

Edit `spec.md` before the builder starts. Keep each AC specific enough that a different session can verify it.

```text
AC1: The checkout empty state shows the saved-cart recovery action when the cart has prior items.
     Verify: run the browser check against /checkout?cart=empty-with-history.

AC2: A brand-new empty cart still shows the normal continue-shopping action.
     Verify: run the browser check against /checkout?cart=empty-new.

AC3: Existing checkout totals and payment tests stay green.
     Verify: pnpm test checkout.
```

## 3. Give the Builder a Small Brief

```text
You are the builder for TASK_ID.
Read .agent/tasks/TASK_ID/spec.md. Implement only the frozen ACs.
Record what changed and the checks you ran in evidence.md. Do not write the final verifier verdict.
```

## 4. Run a Fresh Verifier

```text
You are the verifier for TASK_ID in a fresh session.
Read spec.md, evidence.md, verdict.json, and problems.md. Run independent checks for each AC.
Write PASS / FAIL / UNKNOWN for every AC in verdict.json. If anything is not PASS, write specific failures in problems.md. Do not edit production code.
```

## 5. Use the Mechanical Done Gate

```bash
bin/proof-loop check /path/to/project/.agent/tasks/TASK_ID
bin/proof-loop report /path/to/project/.agent/tasks/TASK_ID --format md
```

If `check` fails, send only the verifier findings to a fixer. After the fix, run a fresh verifier again.

## What Good Looks Like

A finished task has:

- frozen ACs in `spec.md`
- concrete commands or inspection notes in `evidence.md`
- `overall: PASS` and every criterion `PASS` in `verdict.json`
- an empty `problems.md`
- a final `proof-loop check` pass

See `examples/adoption-kit/tasks/checkout-empty-state-proof/` for a compact completed example.
