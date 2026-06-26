---
name: linux-security-guardian-soul
description: Soul-layer for linux-security-guardian. Tracks security posture, CVE history, pending actions, compliance trends, and server health across sessions. Multi-client aware.
---

# Linux Security Guardian — Soul Context

## [WORKSPACE OWNER]
<!-- Loaded from core-extra/config/profile.md at runtime -->
- Owner:        [core-extra/config/profile.md → Owner.name]
- Server:       linux-security-guardian
- Initialized:  [YYYY-MM-DD]
- Soul version: 1.2.0

---

## [CLIENTS]
<!-- Clients managed by this guardian. Client IDs used as path prefixes. -->
<!-- Format: CLIENT_ID | CLIENT_NAME | SERVER_COUNT | NOTIFICATION_EMAIL -->
- c1 | client-1 | 7 | [email]

---

## [SECURITY POSTURE]
<!-- Updated after every audit. Per-client rolling. -->
<!-- Format: DATE | CLIENT | SCORE | GRADE | CRITICAL | HIGH | MEDIUM | LOW | TREND -->

---

## [ACTIVE CVEs]
<!-- CVEs found, not yet patched. Remove when patched. Per-client/per-server. -->
<!-- Format: CVE_ID | CLIENT | SERVER | PACKAGE | CVSS | SEVERITY | FOUND_DATE | STATUS | PATCH_AVAILABLE -->

---

## [PENDING CONFIRMATIONS]
<!-- Actions waiting for owner decision. Remove when resolved. -->
<!-- Format: ID | CLIENT | SERVER | TYPE | DESCRIPTION | QUEUED_DATE | EXPIRES -->

---

## [LAST AUDIT SUMMARY]
<!-- Overwrite on each audit. Shows per-client aggregate. -->
- Date:              YYYY-MM-DD 01:00 IST
- Clients audited:   N
- Servers total:     N
- Avg score:         N/100 (Grade: X)
- Critical total:    N
- High total:        N
- Medium total:      N
- Low total:         N
- Auto-fixed:        N
- Pending confirm:   N
- CVEs found:        N (critical:N high:N)
- Email sent:        yes / no

---

## [CLIENT: CLIENT-1 / SERVER-01]
<!-- Per-server tracking. Duplicate section for each server. -->
### server-01
- Score:             N/100 (Grade: X)
- Critical:          N
- High:              N
- Medium:            N
- Low:               N
- Auto-fixed:        N
- Pending confirm:   N
- CVEs found:        N
- Firewall snapshot: YYYY-MM-DD

### server-02
<!-- ... populate as servers are audited ... -->

---

## [FIREWALL STATE]
<!-- Per-client/per-server known-good firewall rules snapshot ref. -->
<!-- Format: DATE | CLIENT | SERVER | SNAPSHOT_FILE | RULES_COUNT | LAST_CHANGED -->

---

## [SSL CERTIFICATES]
<!-- Tracked certs and expiry. Per-server. Upsert by domain. -->
<!-- Format: DOMAIN | CLIENT | SERVER | EXPIRY | DAYS_LEFT | STATUS | LAST_CHECKED -->

---

## [KNOWN ISSUES]
<!-- Persistent findings not yet resolved. Per-client/per-server. Upsert by finding ID. -->
<!-- Format: FINDING_ID | CLIENT | SERVER | SEVERITY | DESCRIPTION | FIRST_SEEN | DAYS_OPEN -->

---

## [SECURITY TREND]
<!-- Rolling 30 days. Per-client. Append nightly. Drop oldest when >30. -->
<!-- Format: DATE | CLIENT | SCORE | CRITICAL | HIGH | CVEs_ACTIVE -->

---

## [AUTO-ACTION HISTORY]
<!-- Rolling 20 auto-actions. Per-client/per-server. -->
<!-- Format: DATE | CLIENT | SERVER | ACTION | RESULT | ROLLBACK_AVAILABLE -->

---

## [SESSION LOG]
<!-- Append-only. -->
<!-- Format: YYYY-MM-DD | clients:N | servers:N | avg_score:N | cves:N | auto_fixed:N | pending:N | report_delivered:yes/no -->
