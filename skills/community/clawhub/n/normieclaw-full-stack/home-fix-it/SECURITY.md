# Security & Safety Guarantees

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-brightgreen)

## What Was Audited
This skill package underwent a comprehensive Codex Security Audit covering:
- Prompt injection and safety rule override vulnerabilities
- File system isolation and permissions
- Data exfiltration checks
- Database schema security (Dashboard Kit)

## Security Guarantees
- **100% Local Processing:** Your photos, home profile, and maintenance logs are stored entirely locally in your workspace. The skill does not transmit data to external servers or APIs (other than the LLM provider you configure in NormieClaw).
- **Workspace Isolation:** All file operations are scoped strictly to the `home/` directory within your workspace.

## User Setup Guidance
- **File Permissions:** Ensure your `home/` directory and its contents are restricted to your user account (e.g., `chmod -R 700 home/`).
- **Data Privacy:** Avoid entering highly sensitive personal information into your home profile if it is not necessary for maintenance tracking.

## Skill-Specific Notes
**⚠️ SAFETY DISCLAIMER:** Home Fix-It provides maintenance guidance based on AI analysis. Safety advice provided by this tool should *always* be verified. This is guidance, not a licensed contractor's assessment. If a task is flagged as a **RED ZONE** (e.g., gas lines, main electrical panels, structural issues), stop immediately and consult a certified professional.
