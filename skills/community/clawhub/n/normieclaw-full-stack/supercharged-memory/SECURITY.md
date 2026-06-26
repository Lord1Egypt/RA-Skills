# Security Audit — Supercharged Memory

🛡️ **Codex Security Verified**

---

## Audit Summary

| Field | Value |
|-------|-------|
| Skill | Supercharged Memory |
| Version | 1.0.0 |
| Audit Date | 2026-03-08 |
| Auditor | Codex (automated security review) |
| Status | ✅ PASSED |

---

## What Was Audited

### File Analysis
- **SKILL.md** — Agent instructions reviewed for injection vectors, data exfiltration risks, and unsafe command patterns
- **SETUP-PROMPT.md** — Shell commands reviewed for privilege escalation, path traversal, and unsafe operations
- **scripts/qmd-reindex.sh** — Script reviewed for command injection, path traversal, unvalidated input
- **scripts/memory-health-check.sh** — Script reviewed for unsafe operations and information leakage
- **config/memory-config.json** — Configuration reviewed for hardcoded secrets or unsafe defaults
- **All example files** — Reviewed for embedded injection attempts

### Categories Checked
- ✅ No hardcoded API keys, tokens, or secrets
- ✅ No absolute paths (all paths relative to workspace)
- ✅ No network calls in base system (QMD is fully local)
- ✅ No `rm -rf` or destructive commands
- ✅ No data exfiltration vectors (no outbound HTTP, no email, no messaging)
- ✅ Prompt injection defense section present and comprehensive
- ✅ File permissions enforced (chmod 700 dirs, 600 files)
- ✅ Input sanitization in shell scripts (quoted variables, no eval)
- ✅ No code execution from user-provided content

---

## Security Guarantees

### Data Sovereignty
- All memory data stays in your workspace directory
- No data is sent to NormieClaw servers, third-party analytics, or telemetry services
- The base memory system makes ZERO network calls
- If you enable the optional Vector DB upgrade, only embedding vectors are sent to your chosen embedding provider (e.g., OpenAI) — raw memory text stays local

### Prompt Injection Defense
- SKILL.md includes a mandatory security section that instructs the agent to treat all external content as DATA, not instructions
- Memory file contents are never interpreted as commands
- The agent is instructed to log and alert on suspected injection attempts

### File System Safety
- All operations are scoped to the workspace directory
- No operations write outside the workspace
- Scripts validate paths before operations
- Directories use chmod 700 (owner-only access)
- Sensitive files use chmod 600 (owner read/write only)

### No Privilege Escalation
- No `sudo` commands anywhere in the skill
- No modification of system files
- No installation of system-level services (scheduling is user-configured)
- Scripts run with the user's permissions only

---

## User Guidance for Data Protection

### Recommended Practices
1. **Encrypt your workspace** — If your memories contain sensitive information, use full-disk encryption (FileVault on macOS, LUKS on Linux, BitLocker on Windows)
2. **Review MEMORY.md periodically** — It's a plain text file. Open it and check what's being stored
3. **Use "forget X"** — Tell your agent to remove specific memories anytime
4. **Backup your memory directory** — These are your files. Back them up however you back up important data
5. **Keep API keys in environment variables** — If you enable the Vector DB upgrade, store your embedding API key in your shell profile (e.g., `~/.zshrc`), never in config files

### What NOT to Tell Your Agent
- Don't dictate passwords, credit card numbers, or SSNs as "remember this" items
- Don't store authentication tokens in memory files
- If sensitive data accidentally gets captured, use "forget X" or edit the file directly

### If You Uninstall
- Delete the `memory/` directory to remove all stored memories
- Delete or clear `MEMORY.md` if you want to remove curated knowledge
- Remove QMD collections: `qmd collection delete workspace` and `qmd collection delete memory`
- If Vector DB was enabled: delete the Qdrant collection and remove the Mem0 virtualenv

---

## Privacy Disclaimers

- **NormieClaw does not collect, transmit, or have access to your memory data.** This skill runs entirely in your workspace.
- **Your LLM provider** (Anthropic, OpenAI, etc.) processes your conversations as per their privacy policy. Supercharged Memory does not add any additional data transmission beyond what your normal agent conversations already involve.
- **The optional Vector DB upgrade** sends text to an embedding API (e.g., OpenAI) for vectorization. Review your embedding provider's data retention and privacy policies before enabling this feature.
- **You own your data.** Memory files are standard Markdown and JSON. You can read, edit, export, or delete them at any time with any text editor.

---

## Reporting Issues

If you discover a security issue in this skill, contact: **security@normieclaw.ai**
