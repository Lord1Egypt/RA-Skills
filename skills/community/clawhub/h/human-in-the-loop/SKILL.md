---
name: human-in-the-loop
description: Gate agent writes on human approval — one exact plan per OK, single-use expiring nonce, crash reconciliation, drafts-only filter. Use before any agent write. Local state file.
metadata: {"clawdbot":{"emoji":"✋","requires":{"bins":["python3"]},"homepage":"https://openclaw.ai"}}
---

# Human in the Loop

An approval is a narrow, perishable object: it covers one exact action, once, for a limited time. Everything around it is bookkeeping that must survive a crash: the intent is written before the call, success is an id returned by the API, and a doubt is resolved by looking before creating, never by retrying.

## Data, state, and retention — read first

| Item | What this skill does |
|---|---|
| What `scripts/hitl.py` touches | One JSON state file + its `.lock` sidecar, and one run-lock file per external application, all paths you choose, created `0600`, symlinks refused. No network call, no subprocess. |
| What the state file holds | Item id, status, plan fingerprint (sha256), gate names, sha256 of the open nonce, remote id, attempt count, timestamps. Never the plan, the draft, or the nonce itself. |
| Personal data | Business keys and drafts stay in your process memory. They may hold personal data: process them only under the lawful basis of the pipeline that produced them, and prefer opaque references (file number, thread id) over names in item ids and keys. |
| Retention | Keep `applied` items as long as your reconciliation lookups reach back (a pruned item can be re-created as a duplicate). Prune older items on your own schedule. |
| Credentials | One approval secret (≥32 bytes) from an env var or a `0600` file, distinct from every provider credential. Never logged. |

## When to Use

| Situation | Action |
|---|---|
| "ask me before it creates / sends / pays" | §1-§3 with `regime="approval"` |
| "the user said OK, can the agent also fix the other thing?" | No. §1: one plan = one action |
| "the job timed out, did it create the record?" | §4: reconcile, never re-run the creation |
| "two runs of the cron hit the same app" | §5: run lock |
| "the agent only prepares drafts, a human sends them" | §6: `regime="draft_only"`, filter in code |
| Auditing an existing approval flow | Fill the Output Format, one row per rule |

## States and named gates

| State | Meaning | Leaves by |
|---|---|---|
| `proposed` | Plan fingerprinted, nothing asked yet | `open_request`, or apply (draft_only only) |
| `waiting_human` | Blocked on a person; carries named gates | signed decision, expiry, or a new request |
| `approved` | Signed OK redeemed, valid until `approval_exp` | apply, or `approval_stale` |
| `applying` | Intent persisted, API call in flight | recorded id, or `uncertain` |
| `uncertain` | No proof either way | reconciliation only |
| `applied` / `rejected` / `expired` | Final / explicit no / request timed out | new request (not from `applied`) |

Gates are snake_case names the report can count, never prose: `new_record_review`, `possible_duplicate`, `retry_exhausted`, `approval_stale`, `draft_filter`, `workflow_classification_uncertain`, `ambiguous_match`, `missing_document`, `send_required`, `unknown_screen`. When the screen, the data, or the classification does not match the playbook, the answer is `waiting_human` with a gate, not a best guess.

## 1. An OK covers the exact action, never the adjacent

One item = one plan = **one** mutating action. A multi-step job is several items, each approved on its own.

```python
plan = {"action": {"verb": "create_record", "target": "folder/REF-1", "fields": {"amount": 120}},
        "business_key": {"client_ref": "REF-1", "party": "Party A"},
        "unknowns": []}
propose(store, "REF-1:open", plan, regime="approval")
```

`begin_apply` compares the action about to run with `plan["action"]` as canonical JSON. A different verb, another target, or one extra field ("while I'm here, I also closed the old one") is refused. Approval drift is the common failure: the human reads a one-line summary, says OK, and the agent treats it as a mandate to tidy up around it.

## 2. Approval lifecycle

Token format and threat model (why a reply matching `GO 42` is not an approval, channel identity vs signed nonce) are covered by the `prompt-injection` skill, §5. This section covers what happens to a request over time.

```python
nonce = open_request(store, "REF-1:open", plan, ["new_record_review"], ttl_s=3600)
# show the human: plan summary + fingerprint prefix + buttons carrying the nonce
tok = sign_decision(secret, "REF-1:open", nonce, fingerprint(plan), "owner", "approve")  # approval bot side
decide(store, "REF-1:open", tok, secret, plan, {"owner"})
# Output: 'approved'
```

| Rule | Why |
|---|---|
| The request has its own expiry, separate from the token's | A request left open for days turns into a blank cheque; a late tap on an expired request is refused and the item is marked `expired`. |
| A new request supersedes the old one | Only the latest nonce digest is stored; a token for the previous request dies with it. |
| Redeeming clears the nonce in the same locked step | Replay finds no open request. The state file is the ledger. |
| `approval_exp = min(token exp, request exp)` | An OK given on Monday does not authorise a run on Friday: past it, `begin_apply` returns `waiting_human` + `approval_stale` and calls nothing. |
| Clock tolerance 60 s on `iat`, none on `exp` | Two hosts drift; a token dated further ahead than that was not minted by your approver. |
| "No" is signed too | An unsigned "no" is as forgeable as an unsigned "yes"; `rejected` is a state, not an absence of reply. |
| Fingerprint re-checked at decision **and** at apply | A plan edited after the request, or after the OK, is refused at both points. |
| A new OK cannot restart an `applying`/`uncertain` item | Otherwise approval becomes a way around reconciliation. |

## 3. Apply: intent first, success = an id

```python
r = guarded_apply(store, item_id, plan, plan["action"], create=call_api)
# Output: {'status': 'applied'}   or {'status': 'uncertain'}   or {'status': 'waiting_human', 'gates': [...]}
```

Order inside `guarded_apply`: checks and filters → `applying` persisted with fsync → the call → the result. If the process dies after the remote object exists but before the write-back, the state file still says `applying`, which is what forces §4 on the next run.

| API outcome | Recorded as |
|---|---|
| Response carries a non-empty id | `applied`, id stored |
| Exit 0, `{"ok": true}`, `{}`, `None`, `id: ""`, `id: true`, `id: 0` | `uncertain` |
| Timeout, 5xx, client crash, any exception | `uncertain` (never `failed`: you do not know) |

Keep two counters in the run summary, `skipped` and `technical_failures`: a technical failure is not a skip, and it goes to the top of the report.

## 4. After a crash or timeout: reconcile, never re-create

```python
matches = search_remote(**plan["business_key"])   # YOUR lookup; it must raise on error
reconcile(store, item_id, plan, matches)
# Output: 'applied' | 'waiting_human' (possible_duplicate / retry_exhausted) | 'approved' (one retry)
```

| Lookup result | Outcome |
|---|---|
| `None`, a string, anything not a list of dicts | Refused; stays `uncertain`. A failed search is not "absent". |
| Exactly one candidate whose business-key fields all match (trimmed, case-folded) | `applied`, its id attached |
| Two or more matches, or any candidate missing a key field or an id | `waiting_human` + `possible_duplicate` |
| Zero matches, attempts < 2 | `approved` again (or `proposed` in draft_only): one bounded retry |
| Zero matches after the retry | `waiting_human` + `retry_exhausted`. No third attempt, no auto-reconnect loop. |

Business keys are the fields a human would use to spot a duplicate (reference, parties, date, amount), not the remote id you never received. Re-check candidates in code: remote search is often fuzzy or prefix-based.

## 5. One runner per application

```python
acquire_lock("/var/lib/agent/app.lock", job_id="open-records-am", ttl_s=2700, app_running=probe())
```

| Lock state | Outcome |
|---|---|
| None | Acquired |
| Live (not expired) | `SkipLocked("SKIP_LOCKED")`: do nothing this tick |
| Expired, `app_running is False` (proven stopped) | Taken over |
| Expired, `app_running` True, `None`, `"false"`, `0` | Refused: technical alert, lock left intact |
| Corrupt or symlinked lock file | Refused |

An expired lock means the holder is late, not dead. A UI-driving agent that is still clicking when a second run starts produces the duplicate that §4 then has to untangle.

## 6. Drafts-only regime

When the agent only prepares drafts that a human sends or deletes, the draft **is** the proposal. No one sees it before it exists, so the filters stop being precautions and become the only barrier. They run in code before creation; an instruction in the prompt is not a filter.

```python
dp = {"action": {"verb": "create_draft", "target": "thread-7"},
      "business_key": {"thread": "thread-7"}, "unknowns": ["hearing date"]}
propose(store, "thread-7:reply", dp, regime="draft_only")        # a send verb is refused here
guarded_apply(store, "thread-7:reply", dp, dp["action"], create=create_draft,
              draft={"target": "thread-7", "body": body}, forbidden=[r"(?m)^--\s*$"])
```

| Check | Blocks when |
|---|---|
| Verb | Anything but `create_draft` / `update_draft` |
| Target | Draft target ≠ plan target |
| Markers | A field listed in `unknowns` lacks `[TO COMPLETE: <field>]` verbatim in the visible text: removed, reworded to "(to be confirmed)", lower-cased, or hidden in an HTML comment |
| Templates | An unresolved `{{placeholder}}` |
| Caller rules | A `forbidden` regex matches (e.g. a pre-applied signature block) |
| Body | Empty after stripping comments |

A blocked draft goes to `waiting_human` + `draft_filter` with the reasons, and nothing is created. A human approval does not bypass the filter: fix the draft or the plan. Markers are never softened for style; an unknown shown as prose gets sent.

**Half of the draft tests must prove the filter does not over-block.** A filter that refuses legitimate drafts is switched off within a week, and then there is no barrier. The selftest passes drafts containing "send", "sent", "signature", single braces and JSON, markers inside HTML tags or next to an unrelated HTML comment, accents and non-Latin text, `-- see below --`, extra markers, 20k characters, and the `update_draft` verb.

## Reference module

`scripts/hitl.py` (stdlib, Python 3.9+, POSIX): `fingerprint`, `propose`, `open_request`, `sign_decision`, `decide`, `sweep_expired`, `draft_gate`, `begin_apply`, `record_result`, `reconcile`, `guarded_apply`, `acquire_lock`, `release_lock`, `Store`. Every guard raises `Refused` on absent, empty, null, or wrongly typed input; illegal state transitions raise too.

```bash
python3 scripts/hitl.py --selftest            # 118 fixtures (70 must-refuse), exit 1 on any failure
python3 scripts/hitl.py status state.json     # read-only: counts, waiting_human gates, uncertain items
# Output: HITL STATUS applied=12 uncertain=1 waiting_human=2
```

Fifteen guards were mutated once each (request expiry, exact-action check, id-as-proof, failed-lookup-as-absent, stale-lock takeover, marker check, HTML-comment stripping, clock tolerance, approver allowlist, incomplete-candidate rule, stale approval, retry bound, reopen of an in-flight item, and two over-blocking filters); the selftest failed every time.

## Output Format

Approval request (one per item):

```
APPROVAL <item_id> — gates: new_record_review — expires <UTC time>
Action : create_record on folder/REF-1 (fields: amount=120)
Plan   : fp 3f9a1c07…   Duplicate check: 0 match on client_ref+party
[Approve] [Reject]   (buttons carry the nonce; typed replies are ignored)
```

Run summary (every run, even when nothing happened):

```
HITL_RUN_SUMMARY <job_id> <UTC time>
applied=3 uncertain=1 waiting_human=2 skipped=0 technical_failures=1
ALERT uncertain: REF-9:open (timeout) -> reconcile next run
waiting_human: REF-4:open [possible_duplicate]  thread-7:reply [draft_filter: marker_missing:hearing date]
next_action: human decision on 2 items
```

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `previous attempt unresolved: reconcile first` | Item left `applying`/`uncertain` by a crash or timeout | Run your lookup, pass it to `reconcile` |
| Approved item returns `approval_stale` | Apply ran after `approval_exp` | Open a new request; do not extend the old one |
| Valid-looking token refused as "older request" | A later `open_request` superseded it | Use the latest request's buttons |
| Every draft goes to `draft_filter` | Model drops or rewrites markers | Tell the drafting step to copy markers verbatim; never relax the check |
| `SKIP_LOCKED` every tick | Lock TTL longer than the cron interval, or a hung runner | TTL ≈ worst-case run time; alert after N skips |
| `stale lock and the application may still be running` | Expired lock, no proof the app stopped | Check the host by hand, then pass `app_running=False` |
| `state corrupt` | Truncated write or manual edit | Stop and inspect; never auto-reset the state |

## Scope

This skill ONLY: binds a human OK to one exact, fingerprinted action for a limited time; persists intent before any write; treats a missing id as `uncertain`; reconciles by business key before any retry; serialises runners per application; blocks drafts in code before creation.

This skill NEVER: infers approval from free text; widens an OK to adjacent actions; re-runs a creation after a crash or timeout without reconciliation; overwrites a lock whose holder may still run; softens a `[TO COMPLETE]` marker; sends what it drafted; stores plan content, drafts, or nonces in its state.

*Alexandre Bloch · ClawHub @alexbloch-ia*
