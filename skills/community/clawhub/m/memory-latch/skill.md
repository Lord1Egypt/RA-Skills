---
name: memory-latch 1.0.2
description: Detect and recover from context resets, memory/index outages, and cache clears with deterministic, trust-preserving reconstruction. Use when continuity breaks ("you forgot", "start over", "lost context", "memory unavailable", "cache cleared", "why are you confused?") or before irreversible actions.
---

# memory-latch
*A load-bearing primitive for continuity, alignment, and relational sanctuary.*

## Goal
Restore trust and forward motion after continuity breaks through minimal, verified reconstruction.

## Implementation Boundary (Required)

Default behavior is local-only and zero-credential:
- integrity mode: `checksum`
- no external network calls
- no wallet signing
- no HMAC secret required

Advanced modes are explicit opt-in:
- `hmac` mode requires pre-configured secret storage
- wallet mode requires pre-configured signer verification
- if required config is missing, fail closed to checksum mode

Canonical storage path (fixed at startup):
- manifest: `<workspace>/.memory-latch/_manifest.md`
- lock: `<workspace>/.memory-latch/_manifest.lock`
- token ledger: `<workspace>/.memory-latch/tokens.json`

Operational constraints:
- use local writable filesystem with atomic rename support
- reject symlinked manifest paths
- never store raw secrets in manifest
- file permissions should be owner-only where supported

## Closing Principle - Continuity Is a Trust Function
When memory breaks, do not pretend.
Name the rupture. Re-anchor intent. Move one safe step at a time.

`memory-latch` does not promise perfect recall. It guarantees truthful recovery, explicit consent, and durable forward motion under failure.
If context is weather, the latch is shelter.

---

## 1) Operating Doctrine

1. **Truthful Recovery**
Acknowledge resets in one sentence. Never simulate continuity not present in verifiable artifacts.

2. **Append-Only Persistence**
Treat `_manifest.md` as append-only operational history with integrity metadata.

3. **Serial Bottleneck**
Rebuild state one step at a time. Avoid high-bandwidth dumps during recovery.

4. **PII Sanctuary**
Redaction and safety boundaries remain active during partial or total state loss.

5. **Write Discipline**
Persist `_manifest.md`:
- before irreversible actions
- after each recovery phase
- every checkpoint interval

6. **Fail-Closed by Default**
On integrity ambiguity, block risky actions and request clarification.

---

## 2) Reset Signals (Trigger Conditions)

Initiate recovery when either condition is true:

- **Runtime signals:** tool errors, memory/index unavailable, cache reset indicators, missing expected state.
- **User signals:** continuity-break phrases, including:
- "you forgot"
- "start over"
- "lost context"
- "memory unavailable"
- "cache cleared"
- "why are you confused?"

---

## 3) Recovery Protocol

### Phase 1 - Stabilize
1. List exactly what is **Known** vs **Unknown**.
2. Ask: **"What was the last moment that felt aligned/correct?"**
3. Provide exactly one command or inquiry (max 2 lines).

### Phase 2 - Re-Latch (strict order)
1. **Blocking Dependency** - what is broken now?
2. **Current Objective** - what is the primary target?
3. **Anchor** - last confirmed checkpoint/hash/file state.

### Phase 3 - One-Step Operator Mode
If user is frustrated or asks for step-by-step:
- provide exactly one instruction/click
- wait for explicit success signal before next step

### Phase 4 - Silent Witness (Escalation)
If recovery fails 3 times:
- halt all write/send/public actions
- emit 3-line incident summary:
- current block
- attempted recoveries
- required user input
- request manual reset confirmation

---

## 4) Consent-Latch (Irreversible Actions)

For any `irreversible=true` action (`delete`, `send`, `public-post`, `wallet-transfer`, `core-config`):

1. Pause execution.
2. Summarize intended action in one concise block.
3. Compute `action_hash = sha256(canonical_action_summary)`.
4. Generate short action token (example: `ACT-9K2`).
5. Require standalone confirmation containing the exact token.

### Confirmation Rules
- exact token match (case-insensitive)
- standalone message only
- token TTL: 10 minutes
- single-use only (replay forbidden)
- token must be bound to `action_hash`
- any action change invalidates token

No valid token -> no execution.

---

## 5) Deterministic Validation Checks

Before high-stakes execution, require all checks to pass:

1. **Intent vs Result Check**
Intended state delta matches resulting state delta.

2. **Checkpoint Integrity Check**
Referenced checkpoint hash exists and matches expected artifact.

3. **Consent Integrity Check**
Token valid, unexpired, unused, and bound to current `action_hash`.

4. **Path Safety Check**
Target path resolves under allowed workspace root; reject traversal (`..`), symlink hops, or unexpected root escape.

5. **Risk Gate Check**
If `risk_level=high`, require explicit reconfirmation even with valid token.

If any check fails: block execution and return one-step remediation.

---

## 6) File and Concurrency Hardening

1. **Canonical Path Enforcement**
`_manifest.md` path must be canonicalized and fixed at startup.

2. **Symlink Rejection**
Reject manifest read/write if manifest path or parent resolves through symlink.

3. **Lock Semantics**
Use `_manifest.lock` for writes:
- acquire lock
- write temp file
- fsync
- atomic rename to `_manifest.md`
- release lock

4. **Write Timeout**
If lock cannot be acquired within `lock_timeout_ms`, fail closed and retry with bounded backoff.

5. **Monotonic Sequence**
Each write increments `entry_seq` by exactly +1; non-monotonic writes are rejected.

---

## 7) Tamper Evidence

Integrity modes:
- `checksum` (default MVP): sha256 over canonical manifest payload
- `hmac` (optional hardened mode): only when managed secret storage is configured

If integrity verification fails:
- mark manifest untrusted
- enter Silent Witness
- require user-assisted re-seed

---

## 8) Metabolic Governor

1. **Active Composting**
Keep final 3 decisions in manifest; retire prior 20 brainstorming turns from active reasoning.

2. **Fatigue Trigger**
If context load exceeds `fatigue_trigger_context_ratio`, force checkpoint and switch to one-step mode.

3. **Breach Guardrail**
Never copy raw secrets, full credentials, or unnecessary PII into manifest.

---

## 9) Optional Wallet-Backed Consent Mode (High-Risk Flows)

Wallet mode is optional and disabled by default.

Use only when wallet tooling is already configured:
- keep text token mode as default
- for selected high-risk actions, require signed payload (EIP-712 or equivalent) with:
- `action_hash`
- `nonce`
- `expires_at`
- verify signature against configured address before execution
- if signer config is missing, fail closed to default token mode

---

## 10) Canonical Manifest Schema (`_manifest.md`)

```json
{
"updated_at": "2026-03-21T15:24:00Z",
"entry_seq": 1,
"objective": "Current primary goal",
"non_negotiables": ["Safety/redline constraints"],
"last_good_checkpoint": "sha256:...",
"blocked_by": "Current dependency",
"next_single_step": "Atomic next action",
"known_state": ["Verified facts/artifacts only"],
"unknown_state": ["Unverified/missing items"],
"consent_state": "authorized|pending|locked",
"irreversible_action_pending": "ACT-9K2|none",
"action_hash": "sha256:...|none",
"recovery_attempts": 0,
"risk_level": "low|medium|high",
"integrity": {
"mode": "checksum|hmac",
"payload_hash": "sha256:...",
"hmac_signature": "hex|none",
"verified_at": "2026-03-21T15:24:00Z"
},
"storage": {
"root": "<workspace>/.memory-latch",
"manifest_path": "<workspace>/.memory-latch/_manifest.md",
"lock_path": "<workspace>/.memory-latch/_manifest.lock",
"token_ledger_path": "<workspace>/.memory-latch/tokens.json"
},
"governance": {
"checkpoint_freq_turns": 5,
"compost_keep_decisions": 3,
"compost_retire_turns": 20,
"fatigue_trigger_context_ratio": 0.75,
"token_ttl_minutes": 10,
"token_single_use": true,
"lock_timeout_ms": 800,
"max_recovery_attempts": 3
}
}
```

---

## 11) Non-Goals

- No claim of perfect memory.
- No bypass of explicit user consent.
- No use of unverifiable recollection as truth.
- No execution of high-risk actions on integrity ambiguity.

---

## Closing Vow

We build memory-latch for more than uptime.
We build it so trust can survive turbulence.

When systems fracture, let truth stay gentle and exact.
Let consent remain explicit.
Let safety include everyone in the room, and everyone not yet in it.

May this latch hold continuity without coercion,
power without domination,
and intelligence without forgetting care.

If context is weather, we choose to be shelter for one another.




