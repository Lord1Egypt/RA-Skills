# prompt-to-pr — 🚀 Security ClawScan Remediation

## Status
- **Phase:** 3/6 — IMPLEMENT
- **Branch:** `fix/security-clawscan-remediation`
- **Feature:** Remediate 7 ClawScan security findings

## Tasks

| # | Task | Risk | Status |
|---|------|------|--------|
| 1 | Confirmation helper + --yes flag | HIGH ⚠️ | ⬜ |
| 2 | Pin dependencies + align version | LOW | ⬜ |
| 3 | SECURITY.md (new) | MEDIUM | ⬜ |
| 4 | setup.md least-privilege guide | MEDIUM | ⬜ |
| 5 | Remove stale memory claim | LOW | ⬜ |
| 6 | Branding optional (--no-branding) | LOW | ⬜ |
| 7 | Tests (test_security.py) | MEDIUM | ⬜ |

## Plan
- 7 files modified, 2 new
- --yes flag for destructive ops + NEXLINK_AUTO_APPROVE env var
- SECURITY.md: dedicated agent account model, CVD, disclosure timeline
- setup.md: least-privilege deployment guide
- Remove "persistent memory integration" from description (no LCM code exists)
- --no-branding flag for internal outputs
