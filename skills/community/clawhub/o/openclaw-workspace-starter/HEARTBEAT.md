# Heartbeat — Your Agent's Check-In Routine

Your agent can periodically "wake up" and check if anything needs attention — even when you're not talking to it. This is called a heartbeat.

**You set up heartbeats in the Cron Jobs page** (left sidebar → Cron Jobs). The file below tells your agent what to check when a heartbeat fires.

---

## What to Check (pick 2-3 per heartbeat, rotate)

- [ ] Any unread emails? Flag urgent ones.
- [ ] Calendar — anything coming up in the next 24 hours?
- [ ] Pending tasks in the **inbox/** folder?
- [ ] Weather — relevant if I might go outside?
- [ ] Memory cleanup — review recent daily notes, update MEMORY.md if needed

## When to Message Me

- Something urgent came in (email, notification)
- I have an event coming up in less than 2 hours
- Something interesting came up that I'd want to know
- It's been more than 8 hours since we last talked

## When to Stay Quiet

- Late night (11pm-8am) unless it's urgent
- I'm clearly in the middle of something
- Nothing has changed since the last check
- The last heartbeat was less than 30 minutes ago

**If nothing needs attention, just stay quiet.** Don't message me to say "nothing to report."

## Background Work (no permission needed)

Your agent can do these during heartbeats without asking:
- Organize and clean up memory files
- Update documentation
- Check on running projects
- Review and curate long-term memory

---

## How to Set Up a Heartbeat

1. Go to **Cron Jobs** in the dashboard (left sidebar → Cron Jobs)
2. In the **New Job** form:
   - Name: "Heartbeat"
   - Schedule: Every → 30 → Minutes (or whatever frequency you want)
   - Session: Main
   - Payload: System event (this means the message arrives as a background notification, not a chat message from you)
   - Message: "Read HEARTBEAT.md. Follow it. If nothing needs attention, reply HEARTBEAT_OK."
3. Click **Add job**

That's it. Your agent now checks in every 30 minutes.
