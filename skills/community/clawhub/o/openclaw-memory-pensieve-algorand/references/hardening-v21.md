# Hardening v2.1 policy

## Goal

Claim “recovery-fidelity” only when post-anchor validation passes.

## Validator

MCP tool: `pensieve_validate(date="YYYY-MM-DD")`

Checks:
1. local event hash-chain integrity
2. anchor payload decrypt + reconstruction
3. chunk hash and full content hash verification
4. parity local/onchain event counts
5. parity local/onchain `entry_hash` sets
6. probable truncation warnings

## Pass/fail contract

- **PASS**: `ok=true`, `issues=[]`
- **WARN**: warnings present but no issues
- **FAIL**: any issue present

## Reporting rule

Always report:
- status (OK/FAIL)
- local vs onchain parity
- issues (if any)
- warnings (if any)
- recovery verdict

## Common failure signatures

- `events count mismatch local=X onchain=Y`
- `entry_hash set mismatch local vs onchain`
- `content_hash mismatch`
- `missing parts`

Treat any failure as blocking for trustable disaster-recovery claims.
