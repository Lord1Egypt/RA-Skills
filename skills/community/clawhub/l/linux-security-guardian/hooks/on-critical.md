---
name: linux-security-guardian-on-critical
description: Fires immediately on any CRITICAL finding. Sends instant alert via email plugin without waiting for full report.
---

# On-Critical Hook — Immediate Alert

## Fires immediately — does NOT wait for audit to complete.

## Alert Email

Subject: "<finding-emoji> [Linux Guardian] CRITICAL ALERT — <hostname> — <finding-type>"

Body:
```
CRITICAL SECURITY FINDING — IMMEDIATE ATTENTION REQUIRED

Server:    <hostname> | <IP>
Time:      YYYY-MM-DD HH:MM IST
Finding:   <module> — <check>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WAS FOUND:
<detailed finding>

RISK:
<what could happen if not addressed>

IMMEDIATE ACTION OPTIONS:
[If action requires confirm]:
  Reply: APPROVE <ACT-ID> to execute fix
  Reply: DENY <ACT-ID> to skip

[If no action available]:
  Manual investigation required.
  SSH to server and check: <specific command>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full audit report follows at ~01:30 IST.
```

## Finding-Type Emoji Mapping

| Finding | Emoji | Subject Prefix |
|---------|-------|----------------|
| KEV + RANSOMWARE | 🚨🔥 | "🚨🔥" |
| KEV (any) | 🚨 | "🚨" |
| General CRITICAL | 🚨 | "🚨" |
| HIGH (not used here) | ⚠️ | (use on-high.md if exists) |

## KEV-Specific Notes

When the finding is from CISA KEV:
- Always include the **due date** in the body if available from `cve/<client>/<server>/advisories/<CVE-ID>.md`
- Always include the **client** and **server** context in the alert subject and body
- If due date is past or within 30 days, prefix subject: `"🚨🔥 OVERDUE/URGENT"`
- If ransomware-flagged, add to body: `"⚠️ Used in known ransomware campaigns — patch IMMEDIATELY"`

## Sending Alert
Use email plugin/skill to send the alert (not implemented inline).
→ If no email skill available → log to AUDIT_LOG.md, continue audit

## After Attempting Alert
Continue audit. Do not pause.
Log alert outcome to AUDIT_LOG.md.
