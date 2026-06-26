---
name: ms-forms-auto
description: Automate Microsoft Forms submission with dual-calendar integration and M365 MFA support. Use when: automating daily productivity log submissions, submitting Microsoft Forms with calendar-based auto-fill, setting up scheduled form submissions with training/content-dev/learning hour calculations, or working with org MS Forms that require M365 number-matching MFA. Triggers on phrases like "fill out MS form", "automate form submission", "daily form report", "submit Microsoft form", "daily productivity log", "training hours form".
---

# MS Forms Auto

Automate Microsoft Forms submission with Playwright, dual-calendar auto-fill, and M365 number-matching MFA support.

## Quick Start

### 1. Install Dependencies

```bash
cd <skill-directory>
npm install
npx playwright install chromium
```

### 2. Set Up Credentials (one-time)

```bash
node scripts/setup-credentials.js
```

Creates `config/credentials.json` (gitignored) with M365 email/password.

### 3. First Login with MFA

```bash
xvfb-run --auto-servernum node scripts/mfa-login.js
```

When prompted, enter the 6-digit code from your Authenticator app. Saves auth state to `config/storageState.json` for headless reuse.

### 4. Fetch Calendar Data

```bash
node scripts/calendar-fetch.js              # Today (SGT)
node scripts/calendar-fetch.js --date 2026-03-18  # Specific date
```

Returns JSON with all form fields auto-populated from both calendars.

### 5. Submit the Form

```bash
node scripts/submit-daily.js
```

Reads today's entry from `daily-entries/YYYY-MM-DD.json` and submits.

## Architecture

### Dual Calendar System

| Calendar | URL Source | Purpose |
|----------|-----------|---------|
| **Training (TMS)** | Built into script | Training Hours (source of truth) |
| **Outlook** | Built into script | Content Dev Hours, Other Items |

### Field Logic

| # | Field | Source |
|---|-------|--------|
| 1 | Date | Today (M/d/yyyy) |
| 2 | Training Hours | Training calendar events |
| 3 | Content Dev Hours | Outlook calendar (content dev blockouts) |
| 4 | Content Dev Topic | Event description from Outlook |
| 5 | Learning Hours | `max(0, 8 - training - contentDev)` |
| 6 | Learning Topic | 2-3 random topics + any KT Sessions |
| 7 | Other Items | "Preparation, testing, and rehearsal for my next class" + Outlook events (excludes KT Sessions, training duplicates) |
| 8 | Team Hours | Blank |
| 9 | Team Description | Blank |

### Fallback Defaults (if calendars fail)

| Field | Fallback |
|-------|----------|
| Training Hours | 0 |
| Content Dev Hours | 0 |
| Content Dev Topic | NA |
| Learning Hours | 8 |
| Learning Topic | 3 random topics from pool |
| Other Items | "Preparation, testing, and rehearsal for my next class" |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/calendar-fetch.js` | Fetch both calendars, output all form fields |
| `scripts/submit-with-mfa.js` | **Primary**: Combined MFA login + form submit in one session |
| `scripts/submit-daily.js` | Submit form using saved storageState (no MFA) |
| `scripts/mfa-login.js` | Standalone MFA login (headed mode, saves state) |
| `scripts/fill-form.js` | CLI form filler with `--date`, `--training`, etc. args |
| `scripts/setup-credentials.js` | One-time credential setup |

## Automated Pipeline (via OpenClaw Cron)

```
5:45 PM SGT → Pre-Fill cron (isolated) → calendar-fetch.js → draft entry JSON
6:00 PM SGT → Submit cron (main session) → asks Master for MFA code → 
              submit-with-mfa.js --code CODE → login + submit in one session → done
```

**Why main session?** The submit job runs in the main session so it can ask Master Phil for the 6-digit Authenticator code. Speed is critical — the MFA code expires in ~30 seconds, so the login and submit happen in a single browser session via `submit-with-mfa.js`.

## Configuration Files

| File | Purpose | Gitignored? |
|------|---------|-------------|
| `config/credentials.json` | M365 email + password | ✅ |
| `config/storageState.json` | Saved browser session (cookies) | ✅ |
| `config/calendars.json` | Calendar URLs (contains auth tokens) | ✅ |
| `config/calendars.json.example` | Template for calendar URLs | ❌ |
| `config/form-values.json` | Legacy form value defaults | ❌ |
| `daily-entries/` | Daily submission audit trail | ✅ |

## MFA Handling (Improved)

This skill now **intelligently handles both MFA and non-MFA scenarios**:

### Smart Behavior

1. **Auto-detection**: The script attempts credential login first, then checks if MFA is required
2. **Flexible invocation**:
   - `node scripts/submit-with-mfa.js` - Tries credentials only; if MFA appears, waits 30s for manual code entry or exits with code 2
   - `node scripts/submit-with-mfa.js --code XXXXXX` - Provides MFA code upfront; uses it if MFA appears, otherwise proceeds
3. **Graceful fallback**: If credentials alone are sufficient (no MFA prompt), it works without requiring a code
4. **Exit codes**:
   - `0` — Success
   - `1` — General error / invalid credentials
   - `2` — MFA required but no code provided (use --code flag)
   - `3` — MFA code wrong or expired
   - `4` — Form submission failed

### Recommended Usage

**For daily cron (6 PM SGT):**
```
node scripts/submit-with-mfa.js --code [MFA_CODE_HERE]
```
This ensures speed (code ready) and handles both cases:
- If MFA appears → code is used immediately
- If no MFA → code is ignored, submission proceeds

**For manual testing (unknown MFA requirement):**
```
node scripts/submit-with-mfa.js
```
The script will wait 30 seconds on the MFA screen if needed, allowing you to manually type the code from your Authenticator app.

### Why This Works

Microsoft's M365 authentication can be inconsistent:
- Sometimes the OIDC cookie from previous login is still valid → no MFA needed
- Sometimes the cookie expired → MFA required
- Sometimes conditional access policies trigger MFA based on IP/device

The new logic eliminates the "always ask for MFA" problem by making the code optional and only using it when the MFA prompt actually appears.

## Troubleshooting

- **Auth expired**: Run `xvfb-run --auto-servernum node scripts/mfa-login.js` with a fresh Authenticator code
- **Calendar fetch fails**: Script uses graceful fallbacks (0/NA defaults), form still submits
- **Form URL changed**: Update the URL in `scripts/submit-daily.js`
- **Wrong field values**: Run `node scripts/calendar-fetch.js --date YYYY-MM-DD` to verify calendar data
- **Detailed test plan**: See `references/TESTING_AUTH_WORKFLOW.md` for comprehensive authentication workflow testing scenarios
