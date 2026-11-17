---
name: proofkit
description: Prove your AI agents actually did the work — catch fake-success, dry-run theater, and stub code before it ships. Static fake-success scanner + live-artifact verification methodology.
homepage: https://github.com/therealmacsteel
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "category": "verification",
        "requires": { "bins": ["python3"] },
        "tier": "freemium",
        "install":
          [
            {
              "id": "copy",
              "kind": "script",
              "label": "Install proofkit scanner",
              "bins": ["python3"],
            },
          ],
      },
  }
---

# proofkit — proof-of-work verification for AI agents

**The #1 way autonomous agents fail is quietly: they report success they never
achieved.** `ok=True` with no side effect. A `message_id: 0` "delivery". A
`random` simulator dressed as a metric. A dry-run marked "done". proofkit is the
adversarial layer that assumes your agent is lying until a real artifact proves
otherwise.

Built and battle-tested running a 39-agent autonomous fleet at $0/month.

## Why this exists (the pain)

~60% of failed agent deployments share one root cause: **unverified success**.
The agent's log says it worked. The code says `return True`. Nobody checked the
actual side effect. proofkit turns "it looks done" into "here is the live
artifact that proves it ran."

## Free tier — the scanner + the method

### 1. Static fake-success scan
```bash
python3 proofkit/verify_real_scan.py <file> [<file> ...]
```
Flags the tells that let code report success without doing the work:
- `return True` / hardcoded `success=True` / `message_id: 0`
- `random.*` simulators returning fabricated "metrics"
- `TODO` / `NotImplementedError` / empty `pass` bodies
- demo/sample/fixture data on a production path
- `except: pass` that swallows an error then reports success
- dry-run defaults masquerading as live runs

Precise by design (word-boundary matched — `exist_ok=True` won't trip it), and
it prints the honest caveat: **a clean static scan is necessary, not sufficient.**

### 2. The /verify-real method (3 steps)
1. Static pre-scan (above).
2. **Demand a LIVE artifact** — real stdout numbers, a non-zero `message_id`, a
   file that now exists + its bytes, an HTTP 200 from a served page, a real DB
   row that changed. Use a *tripwire*: assert the downstream never runs if a
   false pass would ship.
3. **Verdict:** `VERIFIED LIVE` / `BUILT-BUT-UNVERIFIED` / `FAKE-BROKEN` — with
   the artifact as evidence. Never call it done because it *looks* done.

## Premium tier — the enforcement suite

Everything free, plus the parts that make it a standing guarantee, not a manual pass:

- **/redteam** — adversarial multi-pass verifier: N independent skeptics per
  claim, each prompted to *refute*, kill on majority. Follows the data one layer
  down (the "real API" wrapper is where the fake usually hides).
- **gatecheck** — 6+ guard-invariant proofs (kill-switch reachable, trading
  blocked, injection defense intact, quality gate fail-closed) as a PASS/DRIFT
  table you run before every ship.
- **Tripwire harness generator** — auto-wraps a build step so a false "pass" is
  impossible: the downstream throws unless the real artifact exists.
- **CI hook** — fail the pipeline on any fake-success flag or missing live
  artifact; proof-of-work required to merge.
- **Fleet mode** — run the whole suite across N agents, ranked report of who's
  shipping fake success.

## Use cases
- Autonomous posting/trading/outreach agents (prove the post/order/email really happened)
- Multi-agent fleets where one agent's fake success corrupts the next's input
- CI for AI-generated code (block stubs + fabricated results from merging)
- Any "the agent said it worked" moment you can't afford to trust blind

## Install
Copy `verify_real_scan.py` into your project (free) or install the full skill
from ClawHub for the premium enforcement suite. Zero paid dependencies — pure
Python stdlib + your existing local model for the adversarial pass.
