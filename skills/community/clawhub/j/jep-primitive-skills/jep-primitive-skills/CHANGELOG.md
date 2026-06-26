# Changelog

## [1.0.0] - 2026-04-26

### Added
- Four atomic primitive skills, each <= 200 lines of core logic:
  - **JudgeSkill** (J): Initiate observation assertion with subject/predicate/value structure.
  - **DelegateSkill** (D): Transfer authority with assigner/assignee JAC extension.
  - **TerminateSkill** (T): Close lifecycle with JAC-Fault extension for audit trail.
  - **VerifySkill** (V): Cross-validate with confirmed/rejected/partial results.
- Three-layer architecture:
  - **PrimitiveSkill** (API): Friendly `execute()` methods returning `PrimitiveResult`.
  - **JEPAdapter** (Mapping): `FriendlyEvent` -> strict `JEP04Event` conversion.
  - **JEPCodec** (Protocol): Canonical JSON (RFC 8785), SHA-256 multihash (RFC 9122), UUIDv4 nonce (RFC 9562).
- FastAPI endpoints: `/judge`, `/delegate`, `/terminate`, `/verify`, `/health`.
- Example: `complex_workflow.py` — 7-step warehouse monitoring using only J/D/T/V primitives.
- Tests: 6 unit tests covering all four primitives, parent task hash, rejected verification.

### Design Principles
- **Minimal**: Each primitive does exactly one thing.
- **Composable**: Any complex workflow is an ordered sequence of these four atoms.
- **Interoperable**: Events are strict JEP-04 and feed into Determinability-Checker, COE-Consensus, and JEP-Guard-Audit without conversion.

### References
- Wang, Y. (2026). *JEP: Judgment Event Protocol* (draft-wang-jep-judgment-event-protocol-04).
- Wang, Y. (2026). *JAC: Judgment Accountability Chain* (draft-wang-jac-01).
