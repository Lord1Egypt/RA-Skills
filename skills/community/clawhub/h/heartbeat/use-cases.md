# Heartbeat Use Cases

## 1. Inbox and Notification Triage

Use heartbeat for adaptive checks when urgency is variable.

Pattern:
- run cheap unread precheck
- escalate only for urgent labels
- send `HEARTBEAT_OK` when no urgent items

## 2. Incident Watch During Working Hours

Use active-hours heartbeat for operational monitoring.

Pattern:
- short burst interval while incident open
- automatic cooldown for repeated alerts
- fallback to default interval after resolution

## 3. Calendar-Proximity Nudges

Use heartbeat to detect upcoming events with contextual lead times.

Pattern:
- precheck event window
- notify only within configurable threshold
- skip overnight windows via timezone + active hours

## 4. Release Pipeline Follow-Up

Use heartbeat for state-change detection, not constant full scans.

Pattern:
- precheck pipeline status summary
- pull detailed logs only on failure or stuck state
- suppress duplicates with cooldown

## 5. Hybrid Daily Ops Model

Combine cron and heartbeat:
- cron for exact 09:00 summary
- heartbeat for adaptive urgent checks between summaries

This avoids both timing drift and over-polling.
