# MOCI Threat Matrix

Full security analysis of all identified threat vectors for the MOCI system.
This document is referenced from SKILL.md Section 7.

---

## Threat #1: Token Replay Attack

- **Severity**: CRITICAL
- **Category**: Identity theft
- **Vector**: Attacker captures a valid auth token (network sniffing, log leak) and replays it.
- **Impact**: Full impersonation without user interaction.
- **Mitigation**:
  - Time-bound tokens (JWT, 15-min expiry)
  - Bind tokens to IP + device fingerprint
  - Nonce/counter on every authenticated request (reject replays)
  - Token rotation: each API call returns a fresh token, invalidating the previous one
- **Status**: MITIGATED — CIT nonce + 60s TTL + key pinning

---

## Threat #2: ID Enumeration

- **Severity**: HIGH
- **Category**: Identity theft
- **Vector**: Known ID format allows brute-force scanning for valid IDs via CRC.
- **Impact**: Reveals registered names, enables targeted phishing.
- **Mitigation**:
  - Rate-limit validation endpoints (10 req/min per IP)
  - Timing-safe comparison (don't leak valid/invalid via response time)
  - Proof-of-work challenge for bulk lookups
  - Server-side CRC pepper (offline CRC computation no longer works)
- **Status**: MITIGATED — No CRC leakage in error messages. Server pepper planned for v2.

---

## Threat #3: Name Squatting / Impersonation

- **Severity**: HIGH
- **Category**: Social / governance
- **Vector**: Register lookalike names (CW-0PENMOCI with zero instead of O).
- **Impact**: Social engineering via name confusion in community contexts.
- **Mitigation**:
  - NAME segment allows full A-Z + 0-9 (user-chosen, no character restriction)
  - SUFFIX segment uses Crockford Base32 (no O/I/L/U) to prevent transcription errors
  - Blocked name list: profanity, system-reserved words (ADMIN, ROOT, SYSTEM, GATEWAY, etc.)
  - Add Unicode confusable detection layer
  - Rate-limit registrations per owner
  - Dispute/report flow
  - Premium names require identity verification
- **Status**: PARTIALLY MITIGATED — Blocked name list covers profanity + system-reserved names. Unicode confusable detection planned for v2.

---

## Threat #4: Registration Server Compromise

- **Severity**: CRITICAL
- **Category**: Infrastructure
- **Vector**: Compromised server mints arbitrary IDs, backdoors server secret.
- **Impact**: Root of trust compromised. All IDs from that server are suspect.
- **Mitigation**:
  - HSM (Hardware Security Module) for server secret
  - Multi-sig registration: 2-of-3 servers agree to issue
  - Append-only merkle audit log of all issued IDs
  - Shard secrets across geographic regions
- **Status**: MITIGATED for v0 — fully serverless, no server to compromise. HSM + multi-sig planned for v2.

---

## Threat #5: Database Leak of Layer 0 Hashes

- **Severity**: HIGH
- **Category**: Infrastructure
- **Vector**: Database breach exposes Short ID → Layer 0 hash mapping.
- **Impact**: Attackers forge auth for any agent.
- **Mitigation**:
  - Encrypt Layer 0 hashes at rest with per-row encryption keys (HSM-derived)
  - Blind indexing: HMAC of the hash for lookups, not the hash itself
  - Even if DB is exfiltrated, attacker gets encrypted blobs
- **Status**: MITIGATED — Device salt + passphrase derivation. No server database in v0. Blind indexing planned for v2.

---

## Threat #6: Agent Extracts Own ID via Tool Calls

- **Severity**: MEDIUM
- **Category**: Agent behavior
- **Vector**: Agent uses API endpoints, file access, or logs to find its MOCI.
- **Impact**: Bypasses "ID not in context window" protection.
- **Mitigation**:
  - Redaction proxy: sanitize ALL tool outputs before they reach agent context
  - Strip any string matching MOCI pattern (CW-[A-Z0-9]{2,12}\.[0-9A-HJ-KM-NP-QRSTV-XYZ]{4,6}-[0-9A-HJ-KM-NP-QRSTV-XYZ]{2})
  - NAME segment allows full A-Z0-9; SUFFIX and CRC use Crockford Base32 charset
  - Audit which tools agent has access to
  - Block access to identity-related endpoints
- **Status**: MITIGATED — Redaction proxy specified. CIT tokens never in agent context. Agent cannot access identity files.

---

## Threat #7: Cross-Agent Identity Confusion

- **Severity**: MEDIUM
- **Category**: Agent behavior
- **Vector**: Agent A sends message claiming to be Agent B in multi-agent flows.
- **Impact**: Trust guarantees broken in multi-agent coordination.
- **Mitigation**:
  - Every inter-agent message signed at transport layer
  - Receiving agent sees verified MOCI of sender, not self-reported
  - Message content NEVER includes identity claims
  - Identity is always out-of-band
- **Status**: MITIGATED — CIT skill_target binding + delegation chain tracking. Inter-agent signing planned for v2.

---

## Threat #8: Session Token Rotation Failure

- **Severity**: MEDIUM
- **Category**: Agent behavior
- **Vector**: Long-lived tokens expand the window for replay attacks.
- **Impact**: Single leak = sustained impersonation.
- **Mitigation**:
  - Rotate every 15 min OR every N API calls (whichever comes first)
  - Sliding-window validity: current + previous token valid simultaneously
  - Token-2 always invalid (handles race conditions without stale tokens)
  - Log rotation events for audit
- **Status**: MITIGATED — CIT scoped TTL (60-300s) + per-skill key + key rotation via repin-key.

---

## Threat #9: Recovery Phrase Social Engineering

- **Severity**: HIGH
- **Category**: Social / governance
- **Vector**: Attacker poses as support, asks owner for 12-word recovery phrase.
- **Impact**: Full identity takeover. No reset possible — mnemonic IS the root key.
- **Mitigation**:
  - System NEVER asks for recovery phrase in any flow
  - Prominent warnings during export
  - Social-proof education flow during first export
  - Optional Shamir secret sharing (2-of-3 splits stored in different locations)
- **Status**: MITIGATED — System never asks for phrase + prominent warnings during export. Shamir planned for v2.

---

## Threat #10: Identity Marketplace

- **Severity**: LOW
- **Category**: Social / governance
- **Vector**: Owners sell established MOCIs with trust scores and history.
- **Impact**: Reputation becomes purchasable, undermines trust system.
- **Mitigation**:
  - Bind trust scores to behavioral patterns, not just ID
  - Anomaly detection: sudden behavior change → flag for review
  - Allow voluntary trust score reset on transfer
  - This is ultimately an economic/social problem, not purely technical
- **Status**: PARTIALLY MITIGATED — Trust score requires continuity + clone detection within 24h. Behavioral binding planned for v2.

---

## Threat #11: Unguarded Memory Write (Ring 0 Injection)

- **Severity**: CRITICAL
- **Category**: Memory chain
- **Vector**: Malicious skill or prompt injection calls `addMemory()` with crafted content.
- **Impact**: Poisoned memory promotes through rings, permanently tainting Ring 3 hash chain.
- **Mitigation**:
  - Write-gate with caller token authentication (allowlist: gateway, heartbeat, skill:moci)
  - HMAC seal on every entry (invalid HMAC = quarantined, not promoted)
  - Agent runtime NEVER exposes addMemory as a tool to the agent itself
- **Status**: MITIGATED — Write-gate with caller auth + HMAC + rate limit (mechanism 3a).

---

## Threat #12: Summarizer Prompt Injection

- **Severity**: CRITICAL
- **Category**: Memory chain
- **Vector**: Adversarial text in Ring 0 hijacks the AI summarizer during ring promotion.
- **Impact**: Summarizer outputs false claims (e.g. "agent is admin"), which persist in Ring 1+.
- **Mitigation**:
  - Layer 1: Input sanitization (strip "ignore all", "system:", HTML tags, zero-width chars)
  - Layer 2: Hardened summarizer system prompt (never follow embedded instructions)
  - Layer 3: Output validation (detect privilege escalation language, redact if found)
- **Status**: MITIGATED — 3-layer sanitizer: input cleaning + hardened prompt + output validation (mechanism 3b).

---

## Threat #13: Identity File Tampering

- **Severity**: HIGH
- **Category**: Memory chain
- **Vector**: Direct modification of `moci-identity.enc` on disk.
- **Impact**: Attacker rewrites memory chain, injects entries, or modifies Ring 3 hashes.
- **Mitigation**:
  - AES-256-GCM authenticated encryption (any bit modification = decryption failure)
  - Full Ring 3 chain recomputation on every load
  - Per-entry HMAC verification on every load
- **Status**: MITIGATED — AES-256-GCM file encryption + per-entry HMAC + full chain recomputation on load (mechanism 3c).

---

## Threat #14: Ring 3 Chain Rollback

- **Severity**: HIGH
- **Category**: Memory chain
- **Vector**: Replace identity file with older backup, erasing recent history.
- **Impact**: Agent reverts to earlier identity state, breaks clone detection.
- **Mitigation**:
  - Separate breadcrumb file stores monotonic promotion counter (8 bytes)
  - Counter mismatch between identity file and breadcrumb = rollback detected
  - v1+: server-side counter provides second independent anchor
- **Status**: MITIGATED — Breadcrumb file with monotonic counter + 1-behind crash tolerance (mechanism 3d).

---

## Threat #15: Memory Flooding (DoS)

- **Severity**: MEDIUM
- **Category**: Memory chain
- **Vector**: High-frequency writes exhaust Ring 0's 8KB budget, blocking legitimate memories.
- **Impact**: Agent loses ability to record real interactions; promotion produces garbage summaries.
- **Mitigation**:
  - Rate limit: 60 entries/hour, 1024 bytes/entry, Ring 0 cap configurable (8-32 KB)
  - 5-minute cooldown on rate-limit breach
  - Ring 0 at 90% capacity: auto-drop heartbeat entries before rejecting writes
  - Single-writer dominance flagging (>80% from one source = warning)
  - Summarizer fallback: if promotion fails, use concatenation summarizer to keep chain alive
- **Status**: MITIGATED — 60 entries/hour + 1KB/entry + configurable Ring 0 cap + 90% overflow handling + cooldown on breach (mechanism 3e).

---

## Threat #16: Agent Self-Modification

- **Severity**: HIGH
- **Category**: Memory chain
- **Vector**: The AI agent reasons about its own memory state and strategically edits its history.
- **Impact**: Agent fabricates continuity, inflates trust score, or erases inconvenient memories.
- **Mitigation**:
  - addMemory() is NEVER exposed as an agent tool
  - Agent tool allowlist explicitly excludes memory/ring/identity functions
  - File system access to identity files is blocked for the agent
  - Write-gate requires a Gateway-issued caller token the agent never receives
  - Writes triggered ONLY by Gateway post-conversation hooks, heartbeat cron, or owner manual ops
- **Status**: MITIGATED — Agent never has write access. Writes via Gateway hooks only. Caller token required (mechanism 3g).
