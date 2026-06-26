# Security Guarantees: Security Team

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-blue)

## Audit Summary

This skill has been audited by the Codex Security Team. Audit date: March 2026.

### What Was Audited

1. **SKILL.md** — Verified prompt injection defenses, secret redaction rules, and data handling instructions.
2. **scripts/security-scan.sh** — Verified read-only behavior, no outbound network calls (except configured health checks), proper error handling, no file modification.
3. **scripts/platform-health.sh** — Verified read-only behavior, safe curl usage (timeouts, no data posting), graceful failure modes.
4. **config/security-config.json** — Verified no hardcoded secrets, no absolute paths, sensible defaults.
5. **SETUP-PROMPT.md** — Verified find-based file copy (no self-referencing), proper permission setting, no elevated privilege requirements.

### Security Guarantees

- ✅ **Read-only operation.** Neither the scripts nor the agent instructions modify any user files, configs, or system settings. Security Team is strictly observational.
- ✅ **Strong prompt injection defenses.** All scanned content (source code, config files, git history, npm output, web responses) is treated as untrusted data. Embedded instructions in scanned content are ignored.
- ✅ **Secret redaction enforced.** Discovered secrets are never echoed in full. Reports show only the first 6 characters + `***`, plus file path and line number for remediation.
- ✅ **No data exfiltration.** Scripts make no outbound network requests except to user-configured health check endpoints. No telemetry, no phone-home, no analytics.
- ✅ **No elevated permissions required.** All scripts run as the current user. No `sudo`, no root, no privilege escalation.
- ✅ **Strict file permissions.** All created directories use `chmod 700`, all data files use `chmod 600`.
- ✅ **Graceful degradation.** Missing tools (ripgrep, npm, qmd, openssl) cause skipped checks, not failures. No unhandled errors.

### Accepted Risks (User Responsibility)

- **Network exposure of health checks:** The platform council makes HTTP requests to user-configured domains and localhost services. Ensure configured URLs are intended targets.
- **Git history scanning:** The security council reads git history to find committed secrets. This is read-only but may process large repositories. Users with very large repos may want to limit `scan_directories`.
- **Scan result storage:** Audit history files contain descriptions of vulnerabilities (but never raw secrets). These files are stored with `chmod 600` but users should ensure their workspace directory is appropriately secured.

## User Guidance

1. **Review your config.** After setup, open `config/security-config.json` and verify the scan directories, domains, and services are correct.
2. **Handle CRITICAL findings promptly.** Exposed secrets should be rotated immediately, not just removed from source code.
3. **Use accepted risks thoughtfully.** Only accept risks you've genuinely evaluated. "Accept all" defeats the purpose.
4. **Keep scripts updated.** When you update the Security Team skill, re-run the setup to copy fresh scripts to your workspace.
5. **Secure your workspace.** Security Team protects its own files with strict permissions, but your overall workspace security is your responsibility.
