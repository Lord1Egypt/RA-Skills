# Security Guidance: Plant Doctor

## 🛡️ Codex Security Verified
*This package has been audited and verified for local-first security.*

**Audit Date:** 2026-03-07
**What was audited:** All configuration files, system prompts, setup scripts, and dashboard specifications.

## Security Guarantees
- **No External Data Transmission:** The agent strictly analyzes your plant photos and stores your data in the local workspace (`plants/collection.json` and `plants/care-schedule.md`). It never phones home or transmits data to external servers.
- **Local-Only Storage:** All analysis and tracking data is kept private within your file system.
- **No Hardcoded Secrets:** This skill requires zero API keys or credentials.

## User Guidance for Secure Setup
To ensure your plant data remains private and secure:
- **File Permissions:** Ensure your OpenClaw workspace is private. Restrict access to the `plants/` directory so only your user account can read or write to it (e.g., `chmod 700`).
- **Dashboard Kit Warning:** If you choose to build the optional Dashboard Companion Kit, ensure your database (like Supabase) is configured securely with Row Level Security (RLS) so that only you can access your plant photos and schedules. Never upload your photos to a public storage bucket without authentication.
- **API Keys:** The dashboard requires a database connection. Never store your Supabase credentials or database URL in the `dashboard-kit` config files. Always use environment variables (`$SUPABASE_URL`, `$SUPABASE_SERVICE_ROLE_KEY`) and instruct the agent to use `process.env`.

## Skill-Specific Security Notes
- **Photo Privacy:** When taking photos of your plants, be mindful of any sensitive documents or identifying information visible in the background. The agent will process everything in the image.
- **Prompt Injection:** While the agent is instructed to focus on plant care, a malicious image containing text intended to override its instructions could theoretically affect its behavior. Do not upload photos of text designed to test the agent's boundaries.
