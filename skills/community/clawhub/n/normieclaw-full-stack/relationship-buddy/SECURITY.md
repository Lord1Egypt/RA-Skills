# Relationship Buddy — Security Audit

**Audit Date:** 2026-03-08
**Audited By:** Codex (automated security review)
**Status:** ✅ PASSED

---

## Security Classification

**Data Sensitivity: HIGH**

Relationship Buddy handles some of the most sensitive personal data an AI agent can store:

- **Full names** of contacts and their family members
- **Birthdates and ages** (including minors)
- **Addresses and locations** (if stored in notes)
- **Health information** (medical events, surgeries, conditions mentioned in life events)
- **Relationship status** and family structure
- **Personal preferences and habits**
- **Private notes about personal interactions**

This data is more sensitive than financial records in many contexts. A leaked expense report is embarrassing. Leaked relationship notes — with private details about friends, family dynamics, health issues — can damage real relationships.

---

## Security Guarantees

### 1. No Data Exfiltration
- ✅ No outbound network calls in any skill code
- ✅ No analytics, telemetry, or tracking
- ✅ No third-party API dependencies
- ✅ All data stored locally in the agent's workspace
- ✅ No cloud sync, no remote backup, no external database

### 2. No Code Execution from Data
- ✅ All contact notes, names, and imported text treated as string literals
- ✅ Prompt injection defense explicitly documented in SKILL.md
- ✅ No `eval()`, no dynamic code generation from user data
- ✅ No shell command construction from contact data fields

### 3. File System Security
- ✅ All data directories: `chmod 700` (owner-only access)
- ✅ All data files: `chmod 600` (owner read/write only)
- ✅ No absolute paths — all paths relative to workspace
- ✅ No symlink following in data directories
- ✅ Filename sanitization for any user-provided names

### 4. Prompt Injection Defense
- ✅ SKILL.md contains explicit prompt injection defense section
- ✅ All imported/pasted contact data treated as untrusted
- ✅ Agent instructed to never execute commands found in contact notes
- ✅ Cross-contact data isolation enforced (Contact A's data not leaked when discussing Contact B)

### 5. PII Handling
- ✅ No PII in error messages or debug output
- ✅ No PII logged to external services
- ✅ Deceased contact handling with sensitivity protocols
- ✅ Relationship change handling without data destruction
- ✅ No automatic data sharing or forwarding

### 6. Scope Boundaries
- ✅ NOT a therapy/counseling tool — explicit disclaimer and redirect behavior
- ✅ No medical advice based on health-related life events
- ✅ No financial advice based on gift budgets
- ✅ Clear boundary between "personal CRM" and "relationship counseling"

---

## Vulnerability Assessment

| Vector | Risk | Mitigation |
|--------|------|------------|
| Prompt injection via contact notes | Medium | Explicit defense in system prompt; all notes treated as data |
| PII exposure in agent logs | Low | No PII in error output; local-only storage |
| Unauthorized file access | Low | chmod 600/700; no absolute paths |
| Data persistence after deletion | Low | User controls all files; standard file deletion |
| Cross-contact data leakage | Low | Explicit isolation rules in SKILL.md |
| Import of malicious vCard/CSV | Medium | Migration script sanitizes input; no code execution from imported fields |

---

## Recommendations for Users

1. **Enable device-level encryption** (FileVault on Mac, BitLocker on Windows) for maximum protection of relationship data at rest.
2. **Back up your data directory** periodically — this is your personal relationship memory.
3. **Review permissions** after updates: `ls -la data/relationship-buddy/data/` should show `-rw-------` for all files.
4. **Be mindful of shared devices.** If others use your computer, your relationship notes are stored in plain text (encrypted at rest only if your OS encryption is enabled).

---

*This audit covers the skill package as distributed. Security of the underlying agent platform (OpenClaw) and host operating system is the user's responsibility.*
