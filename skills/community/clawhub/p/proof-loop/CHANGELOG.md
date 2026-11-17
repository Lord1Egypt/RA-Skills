# 0.3.3

- Align optional OpenCode guidance with explicit workflow opt-in.
- Make checker and template wording explicit: artifact consistency is not authenticated verifier attestation.

# 0.3.2

- Keep public proof fixtures outside hidden directories filtered by ClawHub.
- Do not require GitHub CI metadata for runtime doctor checks; tests use explicit interpreters when registry installs omit executable bits.

# 0.3.1

- Reject empty/incomplete verdicts, missing ACs, duplicate or extra ACs, wrong task/phase, and missing evidence/problems artifacts.
- Validate nested artifact types, enums, timestamps and required fields; document the mechanical gate’s trust boundary.

# Changelog

## v0.3.0

- Add a focused adoption kit for repo owners who want to run Proof Loop today.
- Add a compact completed checkout empty-state proof folder under `examples/adoption-kit/`.
- Refresh README quick path around copy-paste setup, fresh verifier handoff, and mechanical done gates.
- Bump skill metadata to `0.3.0`.
