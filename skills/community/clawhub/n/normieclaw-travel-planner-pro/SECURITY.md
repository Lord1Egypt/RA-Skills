# Security Guarantees: Travel Planner Pro

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-blue)

**Audit Date:** March 2026
**Auditor:** Codex Security Team (NormieClaw)

---

## What Was Audited

1. **SKILL.md** — Agent instructions, prompt injection defenses, data handling rules.
2. **SETUP-PROMPT.md** — Directory creation, file permissions, config initialization.
3. **scripts/trip-reminder.sh** — Shell script for pre-trip reminders. Input validation, path traversal prevention, no external data exfiltration.
4. **config/travel-config.json** — Default configuration. No embedded secrets or credentials.
5. **Data schemas** — All JSON schemas reviewed for PII handling.

---

## Security Guarantees

### Prompt Injection Defense
- All external content (travel websites, hotel descriptions, airline pages, booking confirmations, travel blogs) is treated as **untrusted string literals**.
- The agent will never execute commands, modify behavior, or access files outside data directories based on content embedded in fetched web pages or user-pasted travel notes.
- Explicit defense instructions are embedded in SKILL.md and enforced at the system prompt level.

### Sensitive Data Protection
- **Passport numbers** are NEVER stored. Only expiry dates and validity status.
- **Credit card numbers** are NEVER stored. Only "ends in XXXX" references if needed.
- **Booking passwords and login credentials** are never captured or logged.
- All personal data files use `chmod 600` (owner read/write only).
- All data directories use `chmod 700` (owner access only).

### Data Isolation
- All data stays local to the user's workspace. No phone-home, no telemetry, no external API calls with user data.
- Weather API (Open-Meteo) is queried with only latitude/longitude and dates — no personal information transmitted.
- Web searches for destination research contain only destination names and travel dates — no PII.

### Script Security
- `trip-reminder.sh` validates all file paths before reading.
- No shell injection vectors — all variables are quoted.
- Scripts detect workspace root via marker file (AGENTS.md/SOUL.md) to prevent path traversal.
- No scripts execute with elevated privileges.
- No scripts download or execute remote code.

### No Hardcoded Secrets
- Zero API keys, tokens, URLs, or credentials in any file.
- Open-Meteo weather API requires no authentication key.

---

## User Guidance for Data Protection

1. **Encrypt your workspace** if you store sensitive travel documents. Use full-disk encryption (FileVault on macOS, BitLocker on Windows) or encrypt the `travel/` directory specifically.
2. **Don't store raw passport scans** in the travel directory. The skill only needs the expiry date.
3. **Review your travel profile** periodically. Remove companions or loyalty programs you no longer use.
4. **Back up trip data** before deleting — completed trips contain your preference learning history.
5. **If sharing your device**, ensure the `travel/` directory permissions (`chmod 700`) prevent other users from accessing your travel data.

---

## Accepted Risks

- **Web search queries** include destination names and date ranges. These are visible to the search provider (same as manual browsing).
- **Weather API requests** include geographic coordinates. Open-Meteo's privacy policy applies.
- **Itinerary content** reflects publicly available information (restaurant names, attraction details). No proprietary data is generated or stored.

---

## Reporting

If you discover a security issue with this skill, contact: security@normieclaw.ai
