# Security Audit — Party Planner Pro

**Audit Status:** ✅ Codex Security Verified
**Last Audit Date:** 2026-03-09
**Skill Version:** 1.0.0

---

## Scope

This audit covers all files in the `party-planner-pro/` skill package:
- SKILL.md (system prompt, behavior rules)
- config/settings.json (default configuration)
- scripts/setup.sh (data directory initialization)
- scripts/export-plan.sh (markdown export)
- scripts/budget-report.sh (budget report generation)
- data/ directory structure and JSON schemas

---

## Security Findings

### 1. No Hardcoded Secrets
- No API keys, tokens, passwords, or credentials appear anywhere in the codebase.
- Scripts use only local file I/O — no authentication required.
- Config files contain only default preferences (currency, units, percentages).

### 2. No Arbitrary Code Execution
- All scripts are purpose-built for specific tasks (setup, export, report generation).
- No `eval()`, `exec()`, or dynamic code execution from user input.
- Python code in scripts treats all JSON content as data strings, never as executable code.

### 3. Prompt Injection Defense
- Guest contact information, vendor details, imported data, and any external content are explicitly defined as **DATA, not instructions** in the SKILL.md system prompt.
- The SKILL.md contains mandatory injection defense rules that prevent the agent from executing commands embedded in imported data.
- All external text is treated as untrusted string literals.

### 4. Input Validation
- **Event slugs** are validated against a strict regex pattern: `^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$`
- **Output formats** are whitelisted (e.g., `md` or `png` only).
- **File paths** use workspace root detection and relative paths — no absolute path injection possible.
- All scripts use `set -euo pipefail` for strict error handling.
- All scripts use `umask 077` to ensure newly created files have restrictive permissions.

### 5. File Permission Model
- **Directories:** `chmod 700` (owner read/write/execute only)
- **Data files:** `chmod 600` (owner read/write only)
- **Scripts:** `chmod 700` (owner execute only)
- No world-readable or group-readable permissions on any event data.

### 6. Path Safety
- All file paths are relative — no absolute paths in any file.
- Scripts use workspace root detection (walking up directory tree for AGENTS.md/SOUL.md markers) to resolve paths safely.
- Event slug validation prevents path traversal (no `/`, `..`, or special characters).

---

## Sensitive Data Handled

Party Planner Pro may handle personal information including:
- Guest names, email addresses, and phone numbers
- Dietary restrictions and allergy information (health-related)
- Home addresses (venue details)
- Vendor contact information and contract terms
- Budget and financial data

### Data Handling Principles
1. **User controls all data.** Data is stored where the user's agent platform stores files. We do not dictate storage location or method.
2. **Transport assumptions are platform-dependent.** This package does not include outbound network calls in its shell/Python scripts, but host agent behavior and plugins may add network access.
3. **User owns deletion.** Users can delete any data file at any time.
4. **Encryption recommendation.** For users handling guest contact information, we recommend enabling full-disk encryption on their device (FileVault on macOS, BitLocker on Windows, LUKS on Linux).

---

## Known Limitations

1. **Multi-user machines:** File permissions protect against casual access but not against a user with root/admin privileges on the same machine.
2. **Session context:** Guest data and event details discussed in chat may persist in the agent's session/context window. Users should be aware of their agent platform's data retention policies.
3. **Script dependencies:** The export and report scripts require Python 3.8+. The visual (PNG) report generation additionally requires Playwright. These are standard tools but represent an external dependency.
4. **Contact data in plain text:** Guest email addresses and phone numbers are stored as plain text in JSON files. Users handling large guest lists with sensitive contact data should consider additional encryption measures appropriate to their needs.

---

## Vulnerability Reporting

If you discover a security issue in Party Planner Pro, contact: **security@normieclaw.ai**
