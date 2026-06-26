# Security Audit — Budget Buddy Pro

**Audit Status:** ✅ Codex Security Verified
**Last Audit Date:** 2026-03-08
**Skill Version:** 1.0.0

---

## Scope

This audit covers all files in the `budget-buddy-pro/` skill package:
- SKILL.md (system prompt, behavior rules)
- config/budget-config.json (default configuration)
- scripts/generate-budget-report.sh (report generation)
- scripts/parse-statement.py (multi-format statement parser)
- data/ directory structure and JSON schemas

---

## Security Guarantees

### 1. No Data Exfiltration
- **Zero outbound network calls.** No data is transmitted to any external server, API, or endpoint.
- All processing happens locally on the user's machine.
- No telemetry, analytics, or usage tracking of any kind.

### 2. No Hardcoded Secrets
- No API keys, tokens, passwords, or credentials appear anywhere in the codebase.
- Scripts use only local file I/O — no authentication required.

### 3. No Arbitrary Code Execution
- Scripts are purpose-built for statement parsing and report generation only.
- No `eval()`, `exec()`, or dynamic code execution from user input.
- The Python parser treats all CSV/PDF content as data strings, never as executable code.

### 4. Prompt Injection Defense
- Bank statement text, CSV data, PDF extracted text, and vendor descriptions are explicitly defined as **DATA, not instructions** in the system prompt.
- The SKILL.md contains mandatory injection defense rules that prevent the agent from executing commands embedded in financial documents.
- All extracted text is treated as untrusted string literals.

### 5. File Permission Model
- **Directories:** `chmod 700` (owner read/write/execute only)
- **Data files:** `chmod 600` (owner read/write only)
- **Scripts:** `chmod 700` (owner execute only)
- No world-readable or group-readable permissions on any financial data.

### 6. Path Safety
- All file paths are relative — no absolute paths in any file.
- Scripts use workspace root detection (walking up directory tree for AGENTS.md/SOUL.md markers) to resolve paths safely.
- No path traversal vectors — filenames are sanitized before use.

---

## Financial Data Sensitivity

Budget Buddy Pro handles **highly sensitive financial data** including:
- Bank account balances
- Transaction history with vendor names and amounts
- Income levels
- Debt balances and credit card statements
- Net worth calculations
- Recurring bill amounts and due dates
- Savings goal targets

### Data Handling Principles
1. **Minimum retention:** Only data the user explicitly provides is stored.
2. **No inference sharing:** Financial patterns are never communicated outside the user's session.
3. **User owns deletion:** Users can delete any data file at any time.
4. **No cloud backup:** Data exists only in the local `data/` directory.
5. **Encryption recommendation:** For maximum security, users should enable full-disk encryption (FileVault on macOS, BitLocker on Windows, LUKS on Linux).

---

## Known Limitations

1. **PDF parsing accuracy:** Complex PDF layouts may produce parsing errors. The skill recommends CSV export as a fallback.
2. **Multi-user machines:** File permissions protect against casual access but not against a user with root/admin privileges on the same machine.
3. **Session context:** Financial data discussed in chat may persist in the agent's session/context window. Users should be aware of their agent platform's data retention policies.

---

## Vulnerability Reporting

If you discover a security issue in Budget Buddy Pro, contact: **security@normieclaw.ai**
