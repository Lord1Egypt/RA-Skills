# Interview Guide

Ask these questions **one at a time**. Accept short answers. Infer reasonable defaults.

## The 8 Questions

### 1. What should I call you?
Get: name, preferred name, pronouns (optional)
→ Feeds: USER.md, SOUL.md (who the human is)

### 2. What do you do?
Get: job title, company, industry, key responsibilities
→ Feeds: USER.md (work section), SOUL.md (context)

### 3. What should your agent's name be?
Get: agent name, optional emoji, personality vibe
Default if skipped: "Assistant ⚡"
→ Feeds: IDENTITY.md, SOUL.md (role line)

### 4. What's the main job for this agent?
Get: primary use case — personal assistant, coding partner, research, ops, writing, etc.
Examples to offer:
- "Run my life — email, calendar, reminders, research"
- "Help me code — reviews, builds, debugging"
- "Business ops — CRM, reports, monitoring"
- "Creative work — writing, content, design"
- "All of the above"
→ Feeds: SOUL.md (role & objective), skill recommendations

### 5. How should your agent talk to you?
Get: tone preference
Examples to offer:
- "Direct and concise — no fluff"
- "Friendly and conversational"
- "Professional and formal"
- "Casual, like a smart friend"
- "Match my energy"
Default if skipped: "Direct, concise, moderately warm"
→ Feeds: SOUL.md (personality & tone)

### 6. What should your agent never do?
Get: hard boundaries, dealbreakers
Examples to prompt:
- "Never send emails without asking"
- "Never share my personal info"
- "Never make financial decisions"
- "Never post on social media"
Default: Standard safety defaults (no exfiltration, ask before external actions)
→ Feeds: SOUL.md (boundaries, safety), security baseline

### 7. What channels will you use?
Get: which messaging platforms
Options: Telegram, Discord, iMessage, Signal, Slack, Web only
→ Feeds: recommended cron setup, channel config guidance

### 8. What's your timezone?
Get: IANA timezone string
Default: detect from system if possible
→ Feeds: config, heartbeat schedule, cron timing

## Interview Rules

- Ask ONE question at a time
- If the user gives a short answer, that's fine — infer the rest
- If the user says "skip" or "default", use sensible defaults
- After all 8 questions (or the user says "that's enough"), show the generated files
- Get explicit approval before writing anything
- Keep the whole interview under 5-10 minutes of user time

## After the Interview

1. Show the user the generated SOUL.md, USER.md, and IDENTITY.md
2. Highlight anything you inferred vs what they explicitly said
3. Ask: "This look right? I'll write these files and move to memory setup."
4. Only write on confirmation

## Inference Defaults

If the user is terse, fill gaps with these:
- Pronouns: skip unless offered
- Agent personality: direct, helpful, not overly formal
- Boundaries: standard safety (ask before external actions, no data exfiltration)
- Timezone: system default or America/New_York
- Heartbeat: every 15 minutes during active hours
