# Derived Price Level Governance — full rules D1–D10

> Companion to `SKILL.md` §13. That section carries the operating spine (the five-step loop, and what a clean
> validator run does *not* tell you); this file carries the numbered rules in full, with the incidents that
> produced them and the corollaries that make them usable.
>
> **Load this before computing, storing, validating or publishing a derived price level**, and before choosing
> an anchor window for anything. The anchor-window convention table in **D1** is the decision-critical artifact:
> a wrong window produces a level that is arithmetically correct and semantically wrong, which is worse than an
> arithmetic error because it looks plausible.

## 13. Derived Price Level Governance

Every price in this framework that is *computed* rather than *quoted* is a derived level: mode-D add lines, mode-B pullback triggers, range-position bands, B-class trailing stops, and derived thresholds such as a yield-versus-bond gate. They share one failure mode — none of them is self-contained. Each is `f(anchor)`, so a level is only as trustworthy as the anchor behind it, and an anchor that is never declared cannot be checked.

This section exists because a live portfolio once carried the same add-line at two different values in three different files. The trigger line sat within 1% of the price, so the disagreement was not academic. Root cause: a wide-window range high had been reused as the anchor for a narrow-window rule.

### D1 — Anchor windows are per-rule, not per-instrument

A single instrument legitimately has several "highs." They are not interchangeable:

| Rule type | Anchor window | Typical semantics |
|---|---|---|
| Short-horizon add line (e.g. candidate staged entry) | **Recent N-day high** | Short-term drawdown reference; frozen at position open |
| Pullback add on an existing holding | Recent N-day high | Rolling |
| Range-position monetisation | **52-week / 12-month high** | Upper edge of a long box; rolling, reviewed monthly |
| Trailing stop | Rolling high | Rolling, paired with a buffer |
| Derived threshold (yield, spread) | A reference rate or curve point | Refreshed on a fixed calendar |

A 52-week high answers "how far below the one-year top are we." A 20-day high answers "how far below the recent local peak are we." Substituting one for the other produces a level that is arithmetically correct and semantically wrong — which is worse than an arithmetic error, because it looks plausible.

### D2 — Never reverse-engineer an anchor from a target level

Solving `anchor = level ÷ factor` to explain an existing level manufactures an anchor out of nothing. It always "works" — any level divides by any factor — and it launders a bad number into a registered one. Two independent tells that this has happened:

- **Anchor self-inconsistency.** If a rule generates several levels from one anchor, back-solving each level must return the same anchor. Two different implied anchors means neither is real.
- **Anchor coincidence.** If the implied anchor lands within a fraction of a percent of another rule's anchor for the same instrument, the level was almost certainly computed off the wrong window.

Anchor first, from market data. Levels second. Never the reverse.

### D3 — One source of truth, everything else is a mirror

Levels get copied into whatever file needs to read them — position state, risk state, dashboards. The moment there are three writable copies, they drift. Fix the topology, not the values:

- A **registry** holds each level once, with `anchor.type`, `anchor.value`, `anchor.date`, freeze semantics, the per-level `formula`, and a `status`.
- **Every other occurrence is a mirror.** Edit the registry, then propagate. A mirror mismatch is never a judgement call — it is an error.
- Write the **anchor-window convention table** into a machine-readable file next to the registry, not into prose. A convention that exists only in a report has no enforcement power; the next scan will re-derive the level from whatever high it happens to have loaded.

### D4 — Validate mechanically, and be explicit about what the validator judges

Reading the numbers does not find these defects — they are all internally plausible. Only recomputation does. A level validator should check, in this order:

| # | Check | Detection |
|---|---|---|
| D-a | **Anchor rebuild** | Rebuild the anchor independently from daily data over the declared window and freeze date; compare |
| D-b | **Formula recompute** | Recompute each level from the registered anchor and compare |
| D-c | **Mirror consistency** | Every copy outside the registry must equal the registry value |
| D-d | **Cross-window suspicion** | Anchor within ~0.5% of another rule's anchor or range high for the same instrument |
| D-e | **Branch ordering** | When a level has two trigger branches, the higher price must trigger first |
| D-f | **Level already breached** | A live add line above the current price means it fired, or the level is wrong — either way it needs an owner |

Two design rules matter more than the checks themselves:

**The validator audits whether the truth is faithfully registered, not whether the truth is correct.** A mismatch on an entry marked `verified` is a hard failure. The same mismatch on an entry already registered as `unverified`, `suspected` or `conflicting` is a warning — the defect is on record and under repair. Without this split, a known open item turns the gate permanently red and the gate stops meaning anything; red must mean "new problem," or nobody reads it.

**An unverifiable anchor is not a passing anchor.** When the data window does not reach back far enough to rebuild the anchor, the correct output is "unverified," not "no problems found." Silence is not evidence.

**A green validator is not an action permit.** A validator can only audit whether the values are *faithfully registered*; it has no way to know whether the *rule behind a value has been adjudicated*. An open question about how a level is defined — a basis still under discussion, a window nobody has fixed — leaves the arithmetic perfectly consistent and the conclusion unsafe. Keep the two outputs separate: consistency is a property of the registry, authority to act is a property of the rule's status. Where a rule is still open, the correct output is **pending adjudication** plus the item's identifier — never a trigger, a direction, or a size.

### D5 — Declare, register, validate, resolve, trace

The five-step loop, applied before acting on any level:

1. **Declare** — name the rule, then take the anchor window and freeze semantics from that rule's definition.
2. **Register** — the level must be in the registry with a complete anchor record. An unregistered level is not usable for a decision.
3. **Validate** — run the validator. Its output is the only accepted evidence.
4. **Resolve** — a hard failure blocks the action. Warnings and open entries are surfaced in the output, never silently absorbed.
5. **Trace** — an anchor or formula change keeps the previous value, the reason and the date. Anchors get edited by scans, merges and hand fixes; without a trace, nobody can tell a correction from a corruption.

### D6 — Resolve every percentage cap against the owning account, not the portfolio

A percentage-of-capital limit is only meaningful once its base is named. Portfolio documents tend to say "≤N% of total assets" in dozens of places while defining "total assets" nowhere, and the same phrase quietly drifts into meaning four different numbers: portfolio net asset value, securities market value, and each account's own total.

The rule: **an add-size cap resolves against the total value of the account the instrument sits in**, because cross-account cash is not fungible. Portfolio-level limits — concentration, drawdown, allocation drift — resolve against portfolio net asset value. Account-scoped ceilings resolve against that account. State which base was used whenever a cap comes into play.

Two corollaries:

- **Ratify before you rewrite.** Check how the historical trade log actually computed the percentage before declaring a base. If the log has been using the owning-account basis all along, the formal definition ratifies existing practice rather than changing it — and it must not alter any past decision.
- **Beware same-named account fields.** An accounts block may store one book's value cash-inclusive and another's securities-only. Summing the block then silently drops cash. Resolve totals from the aggregate block, never by adding up account entries.

A cap whose base is unstated is not a cap — it is a number that will be computed two ways by two people.

### D7 — Date every balance, and reconcile it with a rollforward

Prices get validated; balances usually do not. A price series is visibly wrong when it is stale — the change column gives it away. A cash figure is invisible: it sits in a state file looking exactly like a fresh number until someone reads the broker.

The rule: **every balance-like field carries its own as-of date and source.** A balance with no as-of marker is treated as unverified, never as current. And any account-level correction ships with a **cash rollforward** — an anchor balance, every cash-moving entry in the interval, and the residual. A non-zero residual must be attributed explicitly (rounded anchor, unlogged entry, or genuinely unresolved). Never absorb it silently.

Three corollaries:

- **Match the check strength to the field's liquidity.** A field that becomes spendable cash tomorrow deserves a stronger gate than an analytical estimate. If your derived levels have a multi-check validator and your balances have none, the asymmetry is the bug.
- **Arbitrate by tier, not by recency.** A first-party broker statement wins on account-level truth — net liquidation value, cash, share counts. The exchange close wins on price. Reconcile both, state the delta and its cause, and never let one silently overwrite the other.
- **A displayed number is not a stored number.** Broker apps round. When a panel shows a rounded figure, recover the precise value from the account identity (net liquidation value minus market value) and record the rounding delta rather than quoting the display.

A stale balance is the most expensive kind of stale data, because nothing about it looks stale.

### D8 — Example configs carry no author positions

Sample data is built by copying the shape of whatever book the author happens to run. That is convenient, and it is also an export: a shipped example watchlist, a `--detail` example in a docstring, or a sample trade log quietly publishes the author's positions to everyone who installs the package. Nothing marks it as a disclosure, so nobody reviews it as one.

The rule: **sample tickers are generic and must not coincide with anything actually held.** A demo exists to show the shape of the config — strategy types, exit ladders, adapter wiring — and every one of those survives substitution. Cost bases, share counts and account balances are left at zero or plainly synthetic values for the same reason.

Two corollaries:

- **Comment residue counts.** Reviewers check the config body and skip the docstrings. A ticker sitting inside a usage example or an `Args:` block is exactly as public as one in the watchlist, and it is the one a scan for "does this file contain a symbol I hold" is least likely to cover.
- **Re-check on release, not on authoring.** A ticker that was neutral when the example was written becomes a disclosure the day it is bought. Audit before publishing, not when the sample is first drafted.

An example that mirrors your book is not a demo — it is a position disclosure shipped without review.

### D9 — An unsettled question needs its own ledger

Long-form prose and error codes are both wrong homes for "this is not settled yet." Prose gets skimmed past; an error code gets folded into pass/fail, and a gate that is permanently red is a gate nobody reads. Give disputes their own register:

- **One ledger, absorptive.** Every open question lives in a single machine-readable file — including the ones already sitting as commentary inside rule documents, as correction queues inside a registry, or as reason strings inside a state file. A question recorded in five places is recorded in none, because the next reader consults whichever one they happen to open.
- **Each entry carries a blocking scope.** Not merely "this is open," but *what it blocks*: a rule, a set of instruments, or a named action. Without a scope an open question either blocks everything (and gets ignored) or nothing (and gets forgotten).
- **Disputes stay out of the exit code.** Keep the adjudication block separate from pass/fail. Its signal is a stop for the *specific* action whose rule is blocked — not for the run. Folding it in would turn the gate permanently red, and a permanently red gate is worse than no gate.
- **Mirrors replicate values, not disputes.** A position or state mirror may carry a reminder field, but the absence of that field means nothing — only the ledger is authoritative. This asymmetry is the trap: an audit that reads mirrors sees consistent numbers and concludes there is no issue, because the disagreement was never a number.
- **A resolved item is not a deleted item.** Move it to resolved with the decision and its date. The next reader needs to know a question was *settled*, not that it never existed.

### D10 — Keep the registry executable; move the chronology out

Traceability and usability pull in opposite directions. Every rule that says "record the previous value, the reason, the date" adds narrative to the file that is read fastest and most often — and the registry is read under time pressure, when a price is near a line. Left alone the narrative wins: the registry becomes an archive wrapped around a thin operational core, and the reader skims it *by topic*, which is exactly how a load-bearing caveat goes unread while every check stays green.

- **Separate the two concerns; delete neither.** Operative values and rule definitions stay in the registry. Chronology, resolutions, correction queues and superseded values move to a companion history file, and the registry keeps a pointer per removed block.
- **Whatever carries a currently binding condition stays.** A record that looks historical but states a live precondition — a gate that must be re-checked, a split that governs the next action — belongs with the values. Moving it recreates the failure the split was meant to fix. "Looks historical" is not the test; "still binding" is.
- **Give the companion file a single write path** that also updates the pointer's count, so the two cannot drift apart.
- **Guard the shape, not just the size.** Fail on a history key reappearing in the registry, on a missing operative field, on a count mismatch, and on serialization drift — a reformat that buries a three-line change inside a three-thousand-line diff is a review failure even when every value is identical.
- **Derive the size target from arithmetic.** Measure the floor first: the rule blocks the validator actually reads cannot be removed, and they usually dominate the file. A target taken from a round number rather than from what must remain will be either trivially met or arithmetically impossible — and an impossible target is the most reliable way to end up with no target at all.

Corollary: prove a registry reshape by **replay against a pre-migration copy** — assert that every moved value appears in the companion file and that every retained field is unchanged — rather than by reading the result and judging it complete.

---

### Two rules that make this structural rather than procedural

**Opposing rules on the same instrument need a mutex.** An add line below the price and a reduce band above it are both legitimate, but if both can fire in the same period the framework contradicts itself. Resolve by first-trigger-wins on a logged timestamp, freeze the other side for the period, and re-evaluate next period. Never allow a same-period add and reduce.

**A level near the price is a live commitment, not a monitor.** The closer a line sits to the current price, the more it needs a registered anchor, a named owner and an execution plan. Distance creates the illusion of safety; the level that is 0.5% away is the one that will be hit while nobody is watching.

**A definition backfill is not a rule change — label it as such.** When a term the rules lean on was never actually defined, defining it changes no threshold and no mode; it only removes the room for two people to compute the same situation differently. Publish it under its own version, call it a backfill, and leave every number untouched. Silently "clarifying" a value is how a definition becomes a rule change nobody signed off on.

---
