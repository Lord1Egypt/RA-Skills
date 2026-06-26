# CODEX Security Audit Report

- Repository: `normieclaw-notetaker-pro`
- Audit date: 2026-03-08
- Auditor: Codex (GPT-5)
- Scope: All repository files except `.git/*` internals (12 files reviewed)

## Summary Counts

- Critical: 0
- High: 0 (1 fixed during this audit)
- Medium: 2
- Low: 1
- Info: 6

## Repaired High/Critical Findings

### 1. Path traversal in Markdown export category handling (FIXED)
- Severity: High (fixed)
- File: `scripts/export-notes.sh`
- Description: Markdown export used `category` from note JSON directly in `os.path.join(OUTPUT_DIR, category)`. A crafted category like `../../tmp/pwn` could write outside the export directory.
- Fix Applied: Added strict category sanitization (`[a-z0-9_-]`), realpath normalization, and boundary check to enforce output remains under `OUTPUT_DIR`.
- Re-audit: Verified patched logic in `scripts/export-notes.sh:143-151`; `bash -n` passes.

## Detailed Findings (Current State)

### 1. Unrestricted URL fetch instruction can enable SSRF-style access
- Severity: Medium
- File: `SKILL.md`
- Description: The instructions allow fetching user-provided URLs (`web_fetch`) without scheme/host restrictions. In many agent runtimes this can reach internal endpoints (`localhost`, private RFC1918 ranges, metadata endpoints), creating data exposure risk.
- Fix: Add URL safety policy in `SKILL.md`: allow only `https://`, block private/loopback/link-local hosts, deny non-http schemes, and require explicit user confirmation before fetching unknown domains.

### 2. Setup copy workflow can pull from unintended paths
- Severity: Medium
- File: `SETUP-PROMPT.md`
- Description: Setup uses broad `find . -path ... -exec cp ...` from current directory. In large or untrusted trees, this can match multiple paths and copy attacker-controlled files.
- Fix: Resolve a single trusted skill root first, enforce exactly one match, and copy from that fixed path only. Fail closed on 0 or >1 matches.

### 3. Security claims overstate package-wide permission posture
- Severity: Low
- File: `SECURITY.md`
- Description: The document states no world/group-readable files are created, but most shipped files are mode `644` in the repository package.
- Fix: Clarify claim to runtime data files only, or add explicit hardening commands for package files if strict confidentiality is required.

## Informational Results by Requested Category

### (1) Hardcoded secrets or credential-like strings
- Result: No hardcoded secrets found.
- Method: Pattern scan across all files (API keys, tokens, JWTs, private keys, bearer patterns).

### (2) Shell script safety issues
- Result: One High issue found and fixed (`scripts/export-notes.sh` category traversal). Current script uses `set -euo pipefail`, quoted variables, and syntax-valid Bash.

### (3) Path traversal risks
- Result: High risk in Markdown export path handling was fixed. Output directory confinement checks exist for CLI output path and now for derived category directories.

### (4) Data exfiltration risks
- Result: No outbound network commands in scripts. Residual Medium risk exists at instruction level due unrestricted URL fetching guidance in `SKILL.md`.

### (5) File permission issues
- Result: Runtime hardening is present (`chmod 700` directories, `chmod 600` exported files). Package files are mostly `644`, which is acceptable for non-sensitive docs but inconsistent with blanket security wording.

### (6) Prompt injection defense in `SKILL.md`
- Result: Strong baseline defenses are present (explicitly treats ingested content as untrusted data and forbids instruction execution from note content).
- Residual gap: URL fetch safety policy (SSRF/domain restrictions) is not specified.

### (7) JSON config safety
- Files: `config/notes-config.json`, `dashboard-kit/manifest.json`
- Result: Both JSON files are syntactically valid; no embedded credentials found.
- Observation: `manifest.json` sync scope (`"notetaker-pro/data/"`) is broad; consider minimizing scope to required files only.

## Files Reviewed

- `README.md`
- `SECURITY.md`
- `SETUP-PROMPT.md`
- `SKILL.md`
- `config/notes-config.json`
- `dashboard-kit/DASHBOARD-SPEC.md`
- `dashboard-kit/manifest.json`
- `examples/meeting-notes-example.md`
- `examples/search-recall-example.md`
- `examples/voice-dump-example.md`
- `scripts/export-notes.sh`
- `CODEX-SECURITY-AUDIT.md`

## Verification Performed

- `bash -n scripts/export-notes.sh` (pass)
- JSON validation via `python3 -m json.tool` for both JSON files (pass)
- Credential pattern scan across repo (no matches)
- Network command scan (`curl|wget|nc|scp|ssh|ftp`) in tracked content (no script usage)

## Final Verdict

**FAIL**

No unresolved Critical/High findings remain after remediation, but unresolved Medium findings remain in instruction safety (`SKILL.md`) and setup path trust (`SETUP-PROMPT.md`).
