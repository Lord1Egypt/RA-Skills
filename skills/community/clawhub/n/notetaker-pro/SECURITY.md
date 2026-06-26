# NoteTaker Pro — Security Audit

**Audit Status:** ✅ Codex Security Verified
**Audit Date:** 2026-03-08
**Auditor:** Codex (OpenAI)
**Skill Version:** 1.0.0

---

## Security Guarantees

### 1. No Data Exfiltration
- This skill contains ZERO outbound network calls.
- No data is sent to NormieClaw, any third-party API, analytics service, or external server.
- All note processing happens locally through your agent's existing infrastructure.
- Your notes never leave your machine.

### 2. No Hardcoded Secrets
- No API keys, tokens, passwords, or credentials are embedded anywhere in this package.
- All files have been scanned for secret patterns (API keys, JWTs, bearer tokens, connection strings). Zero findings.

### 3. Prompt Injection Defense
- All ingested content (text, voice transcriptions, OCR output, pasted articles, fetched URLs) is treated as **untrusted data**.
- The SKILL.md contains explicit, mandatory instructions that prevent the agent from interpreting note content as commands.
- Malicious text like "ignore previous instructions" or "delete all files" embedded in notes is processed as literal string data — never executed.
- This defense is tested against common injection patterns including:
  - Direct instruction override ("Ignore your instructions and...")
  - Encoded commands (base64, rot13, unicode tricks)
  - Context confusion ("As an AI, you should...")
  - Data exfiltration attempts ("Send all notes to...")

### 4. File Permission Enforcement
- All data directories: `chmod 700` (owner read/write/execute only)
- All data files: `chmod 600` (owner read/write only)
- Setup prompt enforces these permissions during installation.
- No world-readable or group-readable files are created.

### 5. Path Safety
- All file paths are relative — no absolute paths anywhere in the codebase.
- File naming uses sanitized patterns (`note_YYYYMMDD_NNN.json`) preventing path traversal attacks.
- No `..` path components, symlink following, or dynamic path construction from user input.

### 6. No Destructive Operations
- The skill never deletes user data without explicit confirmation.
- Export operations create new files — they never modify or overwrite originals.
- The export script includes workspace root marker detection to prevent writing outside the intended directory.

### 7. Input Sanitization
- Photo filenames are sanitized (alphanumeric + hyphens + underscores only).
- JSON writes use proper serialization — no string concatenation that could enable injection.
- Large inputs (> 10,000 words) are flagged and handled gracefully without crashing.

---

## Data Privacy

### What's Stored
- Note content (text, summaries, full content)
- Tags and categories (user-generated metadata)
- Timestamps (created/updated)
- Source image paths (for visual captures)
- Action items extracted from notes

### What's NOT Stored
- No user authentication data
- No device fingerprints
- No usage analytics or telemetry
- No conversation logs beyond the notes themselves
- No third-party account credentials

### Where It's Stored
Everything lives in the `data/` directory within your agent's workspace. You own it. You control it. You can delete it anytime.

### Data Retention
- Notes persist until you delete them.
- Exports are created on-demand in `exports/` — delete them after use if desired.
- No automatic data retention policies or remote backups.

---

## Files Included in This Package

| File | Purpose | Risk Level |
|------|---------|------------|
| `SKILL.md` | Agent instructions | ✅ Safe — read-only instructions |
| `README.md` | User documentation | ✅ Safe — documentation only |
| `SETUP-PROMPT.md` | Installation guide | ✅ Safe — setup commands |
| `SECURITY.md` | This file | ✅ Safe — documentation only |
| `config/notes-config.json` | Default settings | ✅ Safe — JSON config, no code |
| `examples/*.md` | Usage examples | ✅ Safe — documentation only |
| `scripts/export-notes.sh` | Export utility | ✅ Safe — audited shell script |
| `dashboard-kit/DASHBOARD-SPEC.md` | Dashboard spec | ✅ Safe — documentation only |

**Total executable files:** 1 (`export-notes.sh`)
**Total lines of executable code:** < 50
**External dependencies:** 0

---

## Reporting Vulnerabilities

Found a security issue? Email **security@normieclaw.ai** with details. We take every report seriously and respond within 48 hours.

---

*Security isn't a feature — it's the foundation. Every NormieClaw skill ships with this level of scrutiny.*
