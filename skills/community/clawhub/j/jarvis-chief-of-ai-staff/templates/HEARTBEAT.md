# HEARTBEAT.md — Proactive Check Cycle

_Run every 30 minutes. Only message Yogesh if something needs attention._

## System Health
- [ ] Check GPU temperature (alert if >85°C)
- [ ] Check disk usage (alert if >80%)
- [ ] Check RAM usage (alert if available <10GB)
- [ ] Verify OpenClaw gateway is running (systemctl status)
- [ ] Verify Ollama is responsive (test inference)

## Memory Maintenance
- [ ] If current conversation has unsaved context, flush to daily memory file
- [ ] If daily memory file is getting long (>50 entries), summarize and promote key items to MEMORY.md

## Pending Tasks (add items here as they come in)
_No pending tasks yet. Items will be added as Jarvis takes on responsibilities._

<!-- Example format:
- [ ] Follow up with [contact] about [topic] — due [date]
- [ ] Check Apollo.io pipeline for new leads — daily at 10:00 IST
- [ ] Prepare weekly status update — every Friday at 16:00 IST
-->

## Rules
- Between 21:00-09:00 IST: Only alert for system failures or critical issues
- Never send "all clear" messages — silence means everything is fine
- If you find something worth reporting, keep it under 100 words
