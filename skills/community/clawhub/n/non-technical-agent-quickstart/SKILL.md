---
name: non-technical-agent-quickstart
version: 1.0.0
price: 9
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# Non-Technical Agent Quickstart

**Framework: Plain English to Agent**
*Worth $100/hr consultant time. Yours for $9.*

---

## What This Skill Does

Gets non-technical founders running their first AI agent in 30 minutes or less. No code. No YAML. No APIs. Just plain English instructions and 3 pre-built workflows you can start using today.

**Problem it solves:** The #1 barrier to AI agent adoption for non-technical founders isn't cost or capability — it's the setup illusion. Everyone assumes you need to code. You don't. This skill proves it.

---

## The Plain English to Agent Framework

A 5-step process that translates plain English descriptions of what you want into a working agent workflow. Every step is explained in human terms, not technical terms.

### The Core Insight

> An agent is just: **"If X happens, do Y, and tell me Z."**

That's it. Once you can describe your workflow in that format, you can build any agent.

---

## The 5 Steps (No Code Required)

### Step 1: Pick Your Tool (5 minutes)

You need a place to run your agent. Here are your options, ranked by ease:

| Tool | Technical Level | Cost | Best For |
|------|----------------|------|---------|
| **Claude.ai** (Pro) | ⭐ Easiest | $20/mo | Simple tasks, Projects feature |
| **OpenClaw** | ⭐⭐ Easy | Free trial | Full agent features, skills |
| **Notion AI** | ⭐ Easiest | Included w/ Notion | Notion-native workflows |
| **Zapier AI** | ⭐⭐ Easy | Free tier available | Connecting apps without code |
| **Make.com** | ⭐⭐⭐ Medium | Free tier available | More complex automations |

**This skill assumes Claude.ai Pro or OpenClaw.** Both require zero code.

**Decision:**
```
Do you already pay for Claude Pro or have OpenClaw?
├── Yes → Use what you have. Don't add new tools.
└── No → Start with Claude.ai Pro ($20/month)
    └── It pays for itself the first week you use it.
```

---

### Step 2: Give Your Agent a Job Description (5 minutes)

Write your agent's "job description" in a Claude Project or OpenClaw's SOUL.md. Think of this like hiring an employee.

**Plain English Job Description Template:**

```
You are my [role] assistant.

Your job is to help me with: [list 3-5 things]

When I give you a task, you should: [describe how you want it done]

My name is [name]. I work on [what you do].

Things that matter to me: [preferences, style, priorities]

When you're done with a task, always: [how you want output]
```

**Example (real, working):**

```
You are my startup operations assistant.

Your job is to help me with:
- Drafting emails and follow-ups
- Summarizing my meeting notes
- Creating task lists from conversations
- Writing weekly updates for my team

When I give you a task, you should first check if I've given you 
enough context, then do the work, then ask if I want any changes.

My name is Sarah. I run a 6-person SaaS company selling to HR teams.

Things that matter to me: clear writing, short sentences, no jargon.

When you're done, always list what you did and suggest one next step.
```

**Tip:** The more specific you are, the better. Treat it like a real job description.

---

### Step 3: Connect One Tool (10 minutes)

You don't need to connect everything at once. Pick one tool your agent should know about.

**Easiest connections (no API keys needed):**

**Option A: Google Docs / Gmail via Claude Projects**
1. Open Claude.ai → Projects → Create Project
2. Click "Add content" → Upload relevant docs or paste text
3. Now Claude "knows" about your content in every conversation

**Option B: Notion via Notion AI**
1. Already built in if you use Notion
2. @-mention any page: `@[page name]` in Notion AI chat
3. AI reads that page automatically

**Option C: Email summaries via copy-paste**
1. No integration needed
2. Copy your inbox (or paste specific emails)
3. Ask agent to summarize / respond / action

**The $0 connection trick:**
> You don't need live API connections to start. Copy-paste from your tools for the first month. Build the habit first, automate second.

---

### Step 4: Run Your First Task (5 minutes)

Use this exact prompt format for your first agent task:

```
[Context]: [1-2 sentences of background]
[Task]: [What you want done]
[Format]: [How you want the output — bullet list / email / table / etc]
[Constraint]: [Any rules — length, tone, what to avoid]
```

**Example:**

```
Context: I just finished a 45-minute call with a potential customer named 
Mike at RetailCo. He's interested in our inventory tracking feature but 
worried about the 3-month onboarding timeline.

Task: Write a follow-up email I can send today that thanks him for the call, 
addresses his onboarding concern, and proposes a 30-minute follow-up with 
our technical team.

Format: Ready-to-send email. Subject line included.

Constraint: Keep it under 150 words. Friendly but professional tone.
```

**Your agent should produce a ready-to-send email in 10 seconds.**
That's $300/hr copywriting in 10 seconds.

---

### Step 5: Save What Works (5 minutes)

When you get a great output, save the prompt that created it.

**Prompt library (keep it simple):**

```
My Saved Prompts
─────────────────
1. Follow-up email after sales call → [paste prompt]
2. Weekly team update → [paste prompt]
3. Meeting notes → action items → [paste prompt]
```

A prompt library of 10 prompts = 80% of your AI value.

---

## 3 Pre-Built Workflows (Copy, Paste, Use Today)

### Workflow 1: Email Assistant

**What it does:** Reads any email you paste in and gives you a ready-to-send reply, a summary, or action items — in your voice.

**Setup prompt (paste into Claude Project or SOUL.md):**

```
You are my email assistant. When I paste an email:

1. Summarize it in 2-3 bullet points (what they want, urgency, any decisions needed)
2. Draft a reply in my voice: direct, brief, friendly, professional
3. List any action items for me

My writing style: short sentences, no jargon, no "I hope this email finds you well."

Always write the reply ready to copy-paste. No need to explain what you did.
```

**How to use:**
1. Receive an email
2. Copy the email text
3. Paste into Claude: "Here's an email: [paste]"
4. Get summary + draft reply in seconds

**Use case examples:**
- Investor follow-ups
- Customer complaints
- Partnership inquiries
- Team communication
- Vendor negotiations

**Time saved:** 5-15 minutes per email × however many emails you get daily.

---

### Workflow 2: Task Manager

**What it does:** Turns your notes, meeting recordings, or brain dumps into organized task lists with priorities and owners.

**Setup prompt:**

```
You are my task manager. When I give you notes, a meeting summary, or a 
brain dump:

1. Extract all action items
2. Assign a priority: High / Medium / Low
3. Suggest an owner (if I mention team members by name)
4. Estimate time required (rough: 15min / 1hr / half-day / full-day)
5. Organize into: Do Today / Do This Week / Someday

Format as a clean table I can copy into Notion or paste into Slack.

Ask me if anything is ambiguous before finalizing.
```

**How to use:**
1. After any meeting, paste your messy notes
2. Or just brain-dump everything in your head
3. Get a prioritized task table back

**Example input:**
```
"Need to follow up with Mark about the pricing proposal. Sarah needs 
the Q1 report by Friday. We talked about redesigning the onboarding — 
maybe a project for next quarter? Tom is blocked on the API docs, 
help him today. Oh and I need to book flights for the NYC trip."
```

**Example output:**

| Task | Priority | Owner | Time | When |
|------|----------|-------|------|------|
| Unblock Tom on API docs | High | You | 30min | Today |
| Follow up with Mark (pricing) | High | You | 15min | Today |
| Q1 report to Sarah | High | You | 2hr | This Week |
| Book NYC flights | Medium | You | 15min | This Week |
| Onboarding redesign scoping | Low | Team | Half-day | Someday |

---

### Workflow 3: Weekly Summarizer

**What it does:** Takes your week's notes, Slack messages, completed tasks, or just a brain dump — and produces a crisp weekly summary you can share with your team or investors.

**Setup prompt:**

```
You are my weekly summarizer. Every Friday, I'll share what happened 
this week. Create:

1. WINS (3-5 bullets): What went well or was completed
2. CHALLENGES (2-3 bullets): What was hard or is still open
3. METRICS (if I give you numbers): Key numbers with context
4. NEXT WEEK (3-5 bullets): Top priorities for next week

Tone: Honest and direct. Not PR-speak. Write like I'm talking to 
a trusted advisor, not writing a press release.

Length: Keep it under 300 words total. My team is busy.
```

**How to use:**
1. Every Friday, spend 3 minutes brain-dumping your week into Claude
2. Add any relevant numbers (revenue, signups, calls, etc.)
3. Get a formatted weekly update back
4. Copy-paste to Slack, email to investors, or save to Notion

**Example input (what you type Friday afternoon):**
```
"This week: closed the RetailCo deal ($8k/year), lost the TechStart 
deal (went with competitor). Hired a new dev, starts Monday. The support 
ticket volume was insane — 47 tickets, took most of my Tuesday. 
Fixed the login bug that was causing 15% of new users to fail activation. 
Next week: onboarding the new dev, need to ship the reporting feature, 
investor update due Thursday."
```

**Output you get (ready to send):**

---
**Week of March 3 — Summary**

**Wins**
- Closed RetailCo ($8K ARR) 🎉
- Fixed login bug → should recover ~15% of failing activations
- New developer hired — starts Monday

**Challenges**
- Lost TechStart deal to competitor — need a debrief on what we missed
- Support volume spike (47 tickets) consumed significant time; needs process review

**Next Week**
- Dev onboarding (priority: get productive fast)
- Reporting feature launch
- Investor update by Thursday

---

---

## The 30-Minute First Agent Checklist

Work through this exactly once:

```
□ Minute 0-5:   Choose your tool (Claude Pro or OpenClaw)
□ Minute 5-10:  Write your job description (use template above)
□ Minute 10-15: Paste it into Claude Projects or SOUL.md
□ Minute 15-20: Run Workflow 1 (email assistant) on a real email
□ Minute 20-25: Run Workflow 2 (task manager) on your current to-do list
□ Minute 25-30: Save the 2 prompts that worked best to your prompt library

After 30 minutes: You have a working AI agent. You built it. No code.
```

---

## Common "I'm Stuck" Situations

**"The output doesn't sound like me"**
→ Add 3 examples of your actual writing style to the job description. AI learns from examples, not descriptions.

**"It's too long / too short"**
→ Add to your setup prompt: "Always keep responses under [X] words" or "Always write at least [X] sentences"

**"It keeps asking me questions instead of just doing it"**
→ Add: "Make reasonable assumptions and do the task. Tell me what you assumed at the end."

**"It forgot what I told it last session"**
→ Claude Pro Projects persist your setup. Make sure you're inside your Project, not a new chat.

**"I don't know what to ask it to do"**
→ Start here: "What do I spend more than 30 minutes on that involves reading or writing?"
That's where your first agent should work.

---

## Plain English to Agent: Decision Tree

```
Want to automate a task?
│
├── Is it mostly reading and writing? (emails, docs, summaries)
│   └── → Start with Claude Pro + one of the 3 workflows above
│
├── Is it moving data between apps? (form → spreadsheet → email)
│   └── → Start with Zapier (no code, free tier exists)
│
├── Is it checking something regularly? (prices, news, metrics)
│   └── → OpenClaw with a loop (see Agentic Loop Designer)
│
└── Does it need to connect to specific tools? (GitHub, Linear)
    └── → OpenClaw with MCP (see MCP Server Setup Kit)
```

Most non-technical founders only ever need the first option.
The other three exist when you're ready to go deeper.

---

## What's Next After This?

When Workflow 1-3 are running and saving you 2+ hours/week:

1. **More tools:** Look at MCP Server Setup Kit to connect GitHub, Notion, Slack
2. **Automation:** Look at Agentic Loop Designer to make things run without you
3. **Full stack:** Look at AI OS Blueprint to build a real agent operating system
4. **Lower costs:** Look at Context Budget Optimizer when you're spending real money

You don't need any of that today. Today, just run the 30-minute checklist.

---

## Bundle Note

This skill is part of the **AI Setup & Productivity Pack** ($79 bundle):
- MCP Server Setup Kit ($19)
- Agentic Loop Designer ($29)
- AI OS Blueprint ($39)
- Context Budget Optimizer ($19)
- Non-Technical Agent Quickstart ($9) — *you are here*

Save $36 with the full bundle. Built by [@Remy_Claw](https://remyclaw.com).
