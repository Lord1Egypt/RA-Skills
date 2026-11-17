# Security Policy — miab-broker

## Reporting a vulnerability

Open an issue on the repository, or contact the maintainer directly if the issue is sensitive.
Please include the version (`grep VERSION scripts/bin/claw-callback.py`), the command that
reproduces it, and what you observed versus expected.

---

## What this skill does

`miab-broker` is a file-based callback broker for a local multi-agent ensemble. It persists
delegation state to disk and determines where agent wake events are routed. It makes **no network
calls** and has **no runtime dependencies** beyond the Python 3 standard library.

All state lives under `$CLAW_HOME/state/callbacks/` (`CLAW_HOME` defaults to `~/.openclaw`). See
§3 of `SKILL.md` for the exact file inventory.

---

## Trust boundary

The broker assumes **every process that can read `$CLAW_HOME` is trusted**, and that all
participating agents are cooperative. It is designed for a single-user host running one agent
ensemble.

It is **not** hardened for:

- shared or multi-tenant machines,
- untrusted agents participating in a delegation chain,
- environments where local processes outside the ensemble are in the threat model.

If your deployment violates those assumptions, the gaps in "Known limitations" below are load-bearing.

---

## What is enforced

| control | detail |
|---|---|
| **Callback id validation** | Ids must match `^cb-\d{14}-[0-9a-f]{6}$`. Every resolved path is asserted to remain inside the callback root. Ids arrive from agent-generated `callback://` text, making this the primary boundary against a hostile id reaching the filesystem. |
| **`CLAW_HOME` validation** | The root must exist, be owned by the current uid, and have no group or other permission bits. A redirected `CLAW_HOME` would otherwise relocate `agent-registry.json` and hijack wake routing. |
| **Filesystem permissions** | `umask 0077` at entry; state directories `0700`, state files `0600`. |
| **Resume input constraints** | `--resume-file` must resolve under `$CLAW_HOME` unless `--allow-outside` is passed explicitly, is capped at 64 KB, and is schema-validated. `--resume-json` is schema-validated. Only `summary`, `steps`, `expects`, `integrate` are accepted. |
| **Fail-closed behaviour** | All errors emit `{"ok": false, "error": …}` on stderr with a non-zero exit. No raw tracebacks reach agent context. Unreadable envelopes are quarantined to `archive/corrupt/` and logged, never silently skipped. |
| **Path containment on archive writes** | `cancel` and quarantine operations use the same validation as the hot directory. |

---

## Known limitations

These are real, understood, and tracked. Do not assume the broker protects against them.

**No actor authentication.** The `--from` flag is an unverified claim. Any caller may assert any
agent identity. Holder and root ownership are not enforced, so a misbehaving or confused agent can
pop a frame it does not own, or resolve a chain it did not originate.

**No integrity or replay protection.** Envelopes are unsigned plain JSON. A local process can edit
a bottle to redirect its `wake` target or rewrite `resume.steps` — and those steps become
instructions read by the woken agent. There is no tamper detection.

**No concurrency safety.** Envelope writes are not locked and use a shared temporary path.
Concurrent mutation of one bottle can interleave and corrupt it. Corruption is detected and
quarantined on the next `list`/`sweep`, but the data is lost.

**No delivery guarantee.** If a wake event is dropped, the bottle ages out with no redelivery and
the originating agent is not notified. Work can be silently lost.

**Plaintext, unbounded retention.** `ledger.jsonl` is append-only and is not pruned in normal
operation. Task text, results, and artifact paths persist indefinitely.

---

## Guidance for operators

- **Do not put secret values in `--task`, `--summary`, `--result`, or resume fields.** They are
  written to disk in plaintext and are copied into the `dispatch_message` text sent to other
  agents. Reference a secret's *location*, never its value — and prefer not to reference it at all.
- **Keep `$CLAW_HOME` private** (`chmod 700`). The broker enforces this on its root, but the
  surrounding directory tree is your responsibility.
- **Only run the broker among agents you trust.** Given no actor authentication, any participant
  can disrupt any chain.
- **Review `archive/` periodically.** Cancelled and quarantined envelopes accumulate there and are
  not garbage-collected.
- **Measure before enabling the reaper.** A global TTL that suits fast turnarounds will destroy
  legitimate long-running delegations. Use `--dry-run` first.

---

## Scanner findings

This skill has been reviewed by ClawHub's ClawScan and SkillSpector. Both flagged persistent
cross-turn state and unverified actor identity — the "What is enforced" and "Known limitations"
sections above are the direct response. Neither scanner found malicious behaviour; ClawScan's
`purpose_capability` dimension records "no unrelated exfiltration or destructive purpose."

Remediation of the remaining limitations is tracked in
`docs/miab-broker/miab-broker-execution-backlog.md`.

> The `docs/miab-broker/` planning documents referenced here and in `CHANGELOG.md` are internal to
> the reference deployment and are not published with this skill. They are cited for provenance —
> so that a claim in this repository can be traced to the review that produced it — not as files
> you are expected to find alongside it.
