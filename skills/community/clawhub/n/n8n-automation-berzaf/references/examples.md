# Usage Examples — n8n Automation Skill

Real conversation examples showing exactly how to talk
to your OpenClaw agent when this skill is active.

---

## Lead Nurture Examples

**Basic:**
> "Add john@startup.com to lead nurture"

**With context:**
> "John Smith just signed up, email is john@smith.com,
> he found us from the YouTube video on n8n automations"

**Agent response:**
> "Triggering lead nurture for John Smith at john@smith.com
> (source: YouTube). This will send 4 emails over 14 days.
> Confirm? (yes/no)"

**After confirmation:**
> "Done ✅ Lead nurture queued for John Smith.
> Sequence ID: seq_1748291034. First email sends now."

---

## Social Post Examples

**Simple post:**
> "Post to LinkedIn: Just published a new n8n tutorial.
> Link in bio!"

**Multi-platform:**
> "Post this to LinkedIn, X, and Threads:
> Automation tip: You can replace 5 SaaS tools with
> one n8n workflow. Here's how 🧵"

**With hashtags:**
> "Post to LinkedIn with hashtags automation and n8n:
> Our new OpenClaw skill is live on ClawHub!"

**Agent response:**
> "Posting to LinkedIn, X, and Threads:
> 'Automation tip: You can replace 5 SaaS tools with
> one n8n workflow. Here's how 🧵'
> Hashtags: none specified. Confirm? (yes/no)"

---

## Meeting Follow-Up Examples

**After a discovery call:**
> "Send follow-up to Mike Chen at mike@acme.com,
> we talked about their lead gen automation,
> action items are: send proposal by Friday,
> book follow-up call for next week"

**Quick follow-up:**
> "Follow up with sarah@company.com from today's call
> about AI automation"

**Agent response:**
> "Sending follow-up to Mike Chen (mike@acme.com)
> Topic: Lead gen automation
> Action items:
> - Send proposal by Friday
> - Book follow-up call for next week
> Confirm? (yes/no)"

---

## CRM Update Examples

**After a call:**
> "Update CRM for Jessica from TechCorp,
> she said she wants to move forward,
> mark as hot lead, follow up Monday"

**Log a note:**
> "Log in CRM: Called David at 2pm, left voicemail,
> he's interested but needs approval from his boss"

**Status change:**
> "Mark Acme Corp as closed-won in the CRM"

---

## Competitor Report Examples

**Full report:**
> "Check competitors"

**Quick check:**
> "Run competitor report"

**Add a competitor:**
> "Check competitors and also include newcompetitor.com"

**Agent response:**
> "Running competitor monitor report... (fetching data)
>
> # Competitor Report — March 21, 2026
>
> ## Competitor A
> - New pricing page detected — Basic plan now $49/mo (was $39)
> - 3 new blog posts this week about AI automation
>
> ## Competitor B
> - No changes detected
> - 2 new job postings (Senior Engineer x2)
> ..."

---

## Invoice Reminder Examples

**First reminder:**
> "Send invoice reminder to Mike at mike@client.com,
> invoice 1042, $1,500 due last Friday"

**Second nudge:**
> "Second reminder to acme@corp.com for invoice 203, $3,200"

**Final notice:**
> "Final notice to sarah@company.com, invoice overdue 45 days,
> amount $5,000, invoice number 089"

**Agent response:**
> "Sending FIRST invoice reminder to Mike (mike@client.com)
> Invoice #1042 — $1,500
> Tone: Friendly reminder
> Confirm? (yes/no)"

---

## Content Repurpose Examples

**YouTube video:**
> "Repurpose this video:
> https://youtube.com/watch?v=abc123xyz"

**Blog post:**
> "Turn this into social content:
> https://myblog.com/n8n-automation-guide"

**Agent response:**
> "Repurposing content from: [URL]
> Creating: Twitter thread, LinkedIn post, email snippet, hook
> Brand voice: punchy and direct
> Processing... (30 seconds)
>
> ✅ Done! Here are your 4 versions:
>
> **Twitter/X Thread:**
> 1/ You can replace 5 SaaS subscriptions with one n8n workflow...
> [8 tweets]
>
> **LinkedIn Post:**
> Most founders waste $400/month on tools that n8n can replace...
>
> **Email Snippet:**
> Quick tip: if you're paying for [tool], n8n can do that for free...
>
> **Hook:**
> You're paying for tools you don't need. Here's the fix."

---

## Daily Briefing Examples

**Morning trigger:**
> "Morning briefing"
> "What happened overnight?"
> "Daily digest"
> "Give me my briefing"

**Agent response:**
> "# Daily Briefing — March 21, 2026
>
> ## New Leads (Last 24 Hours)
> - 3 new leads
> - Hottest: John from Acme Corp (opened 3 emails)
>
> ## Email Inbox
> - 12 unread emails
> - 2 marked urgent (Mike re: proposal, Client re: invoice)
>
> ## Social Performance (Yesterday)
> - LinkedIn: 1,240 impressions, 47 engagements
> - X: 890 impressions, +12 followers
>
> ## Your Top 3 Priorities Today
> 1. Reply to Mike's proposal email
> 2. Follow up with Sarah (CRM shows 3 days since last contact)
> 3. Post your scheduled content at 9am"

---

## Status Check

**Check if n8n is connected:**
> "n8n status"

**Agent response:**
> "✅ n8n instance connected
> URL: https://your-n8n.com
> Response time: 234ms
>
> Active workflows:
> ✅ lead-nurture
> ✅ social-post
> ✅ meeting-followup
> ✅ crm-update
> ✅ competitor-monitor
> ✅ invoice-reminder
> ✅ content-repurpose
> ✅ daily-briefing
> ✅ health"

---

## Slash Commands Quick Reference

| Command | What It Does |
|---------|-------------|
| `/n8n-status` | Check instance health |
| `/n8n-nurture` | Start lead nurture flow |
| `/n8n-post` | Trigger social post |
| `/n8n-followup` | Send meeting follow-up |
| `/n8n-crm` | Update CRM contact |
| `/n8n-competitors` | Run competitor report |
| `/n8n-invoice` | Send invoice reminder |
| `/n8n-repurpose` | Repurpose content |
| `/n8n-briefing` | Get daily briefing |
