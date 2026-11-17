# proofkit 🔬 — Proof-of-Work Verification for AI Agents

**Category:** Verification / Quality · **Tier:** Freemium · **Deps:** python3 (zero paid)

## One-liner
Catch fake-success, dry-run theater, and stub code before it ships — the adversarial layer that assumes your agent is lying until a real artifact proves otherwise.

## The hook
~60% of failed agent deployments fail the same silent way: the agent reports success it never achieved. `ok=True`, no side effect. proofkit turns "it looks done" into "here's the live artifact that proves it ran." Built running a 39-agent autonomous fleet at $0/month.

## Free
- verify_real_scan.py — static fake-success scanner (return-True, message_id:0, random simulators, stubs, demo data, error-swallow, dry-run defaults). Word-boundary precise.
- The /verify-real 3-step method: scan → demand a live artifact (real stdout/msgid/file/HTTP-200/DB-row + tripwire) → honest verdict.

## Premium ($ — freemium upsell)
- /redteam adversarial multi-pass (N refuting skeptics, follow-the-data)
- gatecheck guard-invariant proofs (PASS/DRIFT table)
- Tripwire harness generator (false pass = impossible)
- CI hook (proof-of-work required to merge)
- Fleet mode (rank N agents by fake-success rate)

## Screenshots / proof
Real scan output catching a planted fake (success:True + message_id:0 + random.choice) — both flags caught; and a clean precise pass on real code.
