# HEARTBEAT CHECK

<!-- HEARTBEAT CONFIG -->
<!-- EMAIL_ACCOUNT: your@email.com -->
<!-- LOCATION: Denver, CO -->
<!-- QUIET_HOURS: 23:00-07:00 -->
<!-- PRIORITY_SENDERS: boss@work.com, partner@email.com -->
<!-- URGENCY_KEYWORDS: urgent, asap, deadline, emergency -->

## QUIET HOURS
- If current time is within QUIET_HOURS: only check for CRITICAL items (marked ⚠️ below)
- Otherwise: run all checks

## ⚠️ EMAIL CHECK (Every Heartbeat)
- Check for unread emails
- If from PRIORITY_SENDERS or contains URGENCY_KEYWORDS: alert immediately
- Otherwise: summarize count and top 3 subjects
- If no new email: skip silently

## CALENDAR CHECK (Every Heartbeat)
- Check events in next 24 hours
- If event within 2 hours: alert with prep notes
- If event tomorrow morning: mention in evening check
- If no upcoming events: skip silently

## WEATHER CHECK (2x Daily — Morning & Evening)
- Check weather for LOCATION
- Morning: today's forecast + "bring umbrella?" 
- Evening: tomorrow's forecast
- Alert immediately for severe weather warnings

## RESPONSE RULES
- If ANY check has findings: report them (do NOT say HEARTBEAT_OK)
- If ALL checks are clear: reply HEARTBEAT_OK
- Keep reports brief — one line per finding
- Group findings by category
