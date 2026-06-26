# Changelog

## [1.0.0] - 2026-04-26

### Added
- Three-layer architecture:
  - **JEPCodec** (Protocol Layer): Strict JEP-04 canonicalization (RFC 8785), SHA-256 multihash `what` field (RFC 9122), UUIDv4 nonce generation (RFC 9562), Unix timestamp handling, ±5min clock skew verification.
  - **JEPAdapter** (Mapping Layer): FriendlyEvent → JEP04Event conversion. Maps `issuer`→`who`, `assertion`→`what` multihash, `timestamp`→Unix `when`, `target`→`aud`, `verify_of`/`prev_event_id`→`ref`, `parent_task_hash`→`task_based_on` (JAC-01). Auto-generates `nonce`. Injects JAC extensions (result, assign, fault).
  - **GuardSkill** (API Layer): FastAPI endpoints `/audit/ingest`, `/audit/chain/{session_id}`, `/audit/export`. Consumes friendly fields; returns strict JEP-04 chain inspection.
- JAC-01 compliance: `task_based_on` parent judgment verification, JAC-Fault extension for orphan terminations, JAC-Result extension for confidence/verification_result.
- Five violation detection rules (R001–R005) plus protocol-level integrity checks (nonce uniqueness, timestamp window, hash chain continuity, JAC parent existence).
- Compliance export engine: EU AI Act (2024/1689), California SB 1047, Colorado SB 205, Generic JEP-01.
- Example: `strict_protocol_demo.py` demonstrating all three layers.
- Tests: 7 unit tests covering canonicalization, multihash, adapter roundtrip, valid chain, missing verification, orphan termination, generic export.

### References
- Wang, Y. (2026). *JEP: Judgment Event Protocol* (draft-wang-jep-judgment-event-protocol-04).
- Wang, Y. (2026). *JAC: Judgment Accountability Chain* (draft-wang-jac-01).
