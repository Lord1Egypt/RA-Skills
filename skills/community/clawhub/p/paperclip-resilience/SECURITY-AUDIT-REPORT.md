# Security Audit Report: `paperclip-resilience`

- **Issue:** SUP-453
- **Date:** 2026-03-27
- **Auditor:** Michael (`michael` agent)
- **Status:** Complete — approved for ClawHub publication

## Executive Summary

The `paperclip-resilience` skill was reviewed for the ClawHub packaging path. No credential leakage, dynamic code execution, or shell-injection primitives were found. The audit focused on the user-controlled inputs most likely to be exposed in public use:

- model identifiers
- `@file` task loading
- spawn mode / label arguments
- regex-based failure pattern config
- Paperclip issue-gate request fields

The review produced a small hardening pass plus a dedicated security test suite.

## Findings and Remediation

### 1. File-path handling needed stronger canonicalization
**Risk:** Medium

`spawn-with-fallback` already blocked obvious `../` traversal, but temp-directory symlinks could still resolve into blocked system paths if only the lexical path was checked.

**Fix applied**
- Canonicalize existing paths with `fs.realpathSync()`
- Evaluate the canonical path against the blocklist / allowlist
- Reject non-regular files before reading

**Result:** temp symlink tunnels into `/etc`, `/usr`, `/var`, etc. are blocked.

---

### 2. Model validation was too narrow and too permissive in the wrong places
**Risk:** Medium

The original validation disallowed valid provider suffixes such as `:free`, while still allowing suspicious path-like segments.

**Fix applied**
- Allow `:` in model segments for real provider/model strings
- Reject empty segments plus `.` and `..` path-traversal segments
- Keep the overall character allowlist and length cap

**Result:** valid model strings continue to work; malformed traversal-style inputs are rejected early.

---

### 3. Security tests were present but not runnable end-to-end
**Risk:** Medium

The draft security tests had async/sync mismatches and assertions that did not reflect the actual validation behavior.

**Fix applied**
- Rebuilt `tests/test-security.js` as a runnable suite
- Updated `tests/test-security-quick.js` to match real validation rules
- Added package scripts for functional + security verification

**Result:** the documented security verification commands now run cleanly.

## Security Review Checklist

### Injection / execution
- ✅ No shell execution in `spawn-with-fallback` (`execFile` only)
- ✅ No `eval`, `Function`, or dynamic code-loading patterns
- ✅ CLI arguments validated before process execution

### Input validation
- ✅ Model names validated and traversal segments rejected
- ✅ Task payload size limited to 1MB
- ✅ `@file` paths validated, canonicalized, and restricted
- ✅ Spawn mode and label inputs allowlisted / sanitized
- ✅ Regex config length/count constrained; invalid patterns dropped
- ✅ Paperclip issue-gate strings sanitized before API writes

### Credentials and secrets
- ✅ No hardcoded API keys or secrets in the skill
- ✅ Runtime auth comes from environment / external auth files
- ✅ No security changes introduced new secret persistence

### File system and network boundaries
- ✅ File reads are explicit and validated
- ✅ System-path access is blocked for task-file loading
- ✅ No undocumented network endpoints introduced by this audit

### Dependency posture
- ✅ Zero external runtime dependencies in `package.json`
- ✅ `npm audit --omit=dev` is effectively clean because there are no installed runtime packages to audit in this skill package

## Verification Evidence

Run from `skills/paperclip-resilience/`:

```bash
node tests/test-spawn-with-fallback.js
node tests/test-security.js
node tests/test-security-quick.js
npm test
```

Expected result: all commands pass.

## Residual Risk / Notes

- `run-recovery.js` still depends on Paperclip / OpenClaw runtime configuration and upstream endpoint behavior; this audit did not expand its API surface.
- Error messages are intentionally practical for local operators. They do not attempt full forensic redaction of every possible user-provided string.
- Security posture here assumes local operator trust for skill configuration files; the hardening focuses on user/task inputs and publication safety.

## Final Assessment

`paperclip-resilience` now meets the bar for public ClawHub distribution:

- no critical findings
- medium findings addressed
- security docs updated
- verification commands runnable

**Recommendation:** ✅ Publish after the normal packaging step.
