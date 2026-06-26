# Security & Privacy Guarantees

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-brightgreen)

## What Was Audited
This skill package underwent a comprehensive Codex Security Audit covering:
- Prompt and HTML injection vulnerabilities
- PDF generation script safety (Playwright)
- File system isolation and path traversal
- Sensitive data handling and storage

## Security Guarantees
- **100% Local Processing:** Your business profile, client list, and invoices are stored entirely locally. The skill does not exfiltrate financial data to external servers.
- **No Hardcoded Secrets:** This skill package contains no hardcoded API keys or external webhook endpoints.

## User Setup Guidance
- **Sensitive Data Handling:** Do NOT store highly sensitive information (such as full bank account numbers, unredacted tax IDs, or passwords) in plain text in `business-profile.json` or the SQLite database. Use reference identifiers or payment links (like Stripe/PayPal) instead of raw banking details.
- **File Permissions:** Ensure your `invoices/` directory and SQLite database are restricted to your user account (e.g., `chmod -R 700 invoices/`) to prevent unauthorized access by other local processes.
- **Environment Variables:** If extending this skill with external APIs, always use environment variables. Never hardcode secrets.

## Skill-Specific Notes
The PDF generation script uses a headless browser to render HTML templates. For enhanced security, ensure that any user-provided descriptions or client names do not contain malicious HTML tags, as they will be rendered in the final PDF document.
