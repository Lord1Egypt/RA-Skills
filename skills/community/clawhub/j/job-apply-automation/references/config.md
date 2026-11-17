# Config — YOUR DETAILS
# Copy this file to CONFIG.md and fill in your real information.
# The agent reads CONFIG.md, not config.md — this file stays as a template.
# NEVER share your CONFIG.md with anyone.

## Personal Info

```yaml
name: "[YOUR FULL NAME]"
email_application: "[your-gmail@gmail.com]"
email_personal: "[your-personal@email.com]"
phone: "[YOUR PHONE NUMBER]"
linkedin: "[YOUR LINKEDIN URL]"
cv_filename: "CV.pdf"          # must match the actual filename in references/
timezone: "[YOUR TIMEZONE]"   # e.g., Europe/Berlin, America/New_York, Asia/Tokyo
notification_channel: whatsapp
notification_number: "[YOUR WHATSAPP NUMBER]"
```

## Target Profile

```yaml
target_roles:
  - Full Stack Developer
  - Software Engineer
  - Backend Developer
  - TypeScript Developer
  - Node.js Developer

target_locations:
  - Remote
  - Berlin
  - Germany

salary_minimum: 50000
salary_currency: EUR

notice_period: "2 weeks"
right_to_work: "EU"
visa_sponsorship_required: false
willing_to_relocate: false
```

## Email Settings

```yaml
smtp_host: smtp.gmail.com
smtp_port: 587
smtp_tls: true
# ⚠️ app_password is stored separately in references/SMTP-SECRET.txt
# Do NOT paste your password here. See Setup Checklist below.
smtp_user: "[your-gmail@gmail.com]"
```

---

## Secret Files (Never Commit)

This skill requires one additional secret file that must **never** be shared, exposed, or uploaded anywhere:

```bash
# Collect the password securely — never pass secrets as command-line arguments.
# The read -p prompt hides input and does not save it to shell history as a visible argument.
umask 077
read -rsp "Gmail app password: " SECRET
printf '\n'
printf '%s\n' "$SECRET" > references/SMTP-SECRET.txt
unset SECRET
```

If you previously used an `echo` command, remove it from history with `history -d $(history | grep "SMTP-SECRET" | head -1 | awk '{print $1}')`.

`references/SMTP-SECRET.txt` contains **only** the raw app password (one line, no label). The agent resolves it at send-time only.

## Credential Security

- **SMTP secret isolation:** `references/SMTP-SECRET.txt` must never be loaded during initial context loading. It should only be read immediately before SMTP authentication, after explicit user approval of the email content.
- **CONFIG.md must NOT contain any passwords or secrets.** It contains only non-sensitive settings (host, port, username). The SMTP app password belongs ONLY in `references/SMTP-SECRET.txt`.
- Use a **dedicated Gmail account** for job applications (not your primary/personal email).
- Enable 2FA on the dedicated account. The app password is only as strong as the parent account's security.
- If you suspect credential exposure: revoke the app password immediately from Google Account settings, then generate a new one.
- `CONFIG.md` and `SMTP-SECRET.txt` should never be shared, uploaded to cloud storage, or included in any external communication.
- **Credential lifecycle:** Read the secret immediately before SMTP authentication, keep it only in process memory for the minimum required duration, and discard it immediately after the send attempt.

---

## Setup Checklist

- [ ] Dedicated Gmail account created
- [ ] Gmail App Password generated from Google Account → Security → 2-Step Verification → App Passwords
- [ ] All fields above filled in (except app_password — stored separately)
- [ ] Created `references/SMTP-SECRET.txt` with your app password and set permissions to 600
- [ ] CV PDF dropped into `references/` (filename must match `cv_filename`)
- [ ] `CONFIG.md` created (copy of this file with real values)
- [ ] Target companies added to `references/platform-notes.md`
- [ ] **Security verification:** Confirm `references/SMTP-SECRET.txt` is NOT listed in Step 1 of SKILL.md (credential isolation verified)
