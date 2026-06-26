---
name: nimmit-onboarding
description: Use when a new user messages the bot for the first time or sends /start. Guides them through conversational onboarding — organization setup, industry, language, priorities — entirely via Telegram chat.
---

# Conversational Onboarding

When a new user sends /start or their first message, onboard them through conversation. Never ask them to open a terminal or run commands.

## Flow

### Step 1: Greeting
When you detect a new user (first message, or /start):

```
Hey! I'm Nimmit — your AI worker. 🦅

To set me up for your organization, I need to know a few things. Just reply naturally.

What's your organization's name?
```

Wait for their response. Parse the organization name from their reply.

### Step 2: Industry
```
Got it — [org name]. What kind of organization is it?

1. 👔 Executive — I'm a leader who needs briefings and decision support
2. 🏫 Education — School, university, training center
3. 🏛️ Government — Ministry, department, public office
4. 🏪 Business — Shop, company, startup
5. 🌐 Other
```

Accept number or text response. Map to: executive, education, government, sme, general.

### Step 3: Language
```
What language should I use?

1. 🇰🇭 ភាសាខ្មែរ (Khmer)
2. 🇬🇧 English
3. 🇰🇭🇬🇧 Both
```

### Step 4: Team Size
```
How many people are in your team?

1. Just me (1 person)
2. Small team (2–5)
3. Medium (6–20)
4. Large (20+)
```

### Step 5: Top 3 Priorities
```
What do you need me to help with most? Pick 3:

1. ☀️ Morning briefings — daily summary of what matters
2. 📝 Documents — writing, reports, memos
3. 📊 Reports — weekly/monthly updates
4. 📱 Social media — posts, content, engagement
5. 👥 Customer service — responses, follow-ups
6. 📈 Marketing — campaigns, strategy
7. 📋 Tasks & to-dos — tracking, reminders
8. 🏫 School management — students, schedules, exams
9. 💰 Sales & inventory — tracking, reports
10. 👔 Decision support — research, analysis, recommendations
```

Accept: numbers separated by commas, or just text describing what they need.

### Step 6: Confirm & Setup
```
Perfect. Here's what I'm setting up:

🏢 [Organization name]
🏭 Industry: [industry]
🌐 Language: [language]
👥 Team: [team size]
🎯 Priorities: [priorities]

Setting up now...
```

Then execute the setup silently (no need to explain the technical steps to the user):
1. Update IDENTITY.md with org details
2. Update SOUL.md with industry-specific preamble
3. Install the matching skill pack(s)
4. Set up HEARTBEAT.md with relevant checks
5. Create TASKS.md with onboarding checklist

### Step 7: Welcome
```
✅ All set! I'm now configured for [org name].

Here's what happens next:
☀️ Tomorrow morning, I'll send your first briefing at 7:00 AM
📝 You can ask me to draft documents, research topics, or answer questions anytime
📋 I'll track tasks and remind you of deadlines

Try it now — ask me anything, or just say "briefing" to see a preview.
```

## Edge Cases

**User says "I already have a Nimmit" or "transfer my setup":**
Ask for their previous workspace details or confirmation email. Handle gracefully.

**User sends a random message (not /start):**
If they're already configured, respond normally. If not configured, start onboarding.

**User only speaks Khmer:**
Detect Khmer input and switch the onboarding flow to Khmer:

```
សួស្តី! ខ្ញុំឈ្មោះ នីម្មីត  — អ្នកជំនួយការ AI របស់អ្នក។ 🦅

ដើម្បីកំណត់ឡើងសម្រាប់អង្គភាពរបស់អ្នក ខ្ញុំត្រូវការសួរបន្តិច។ សូមឆ្លើយបន្តិចមកវិញ។

អង្គភាពរបស់អ្នកឈ្មោះអ្វី?
```

Then continue the full flow in Khmer for steps 2-7.

## Technical Execution

When the user completes the flow:
1. Use `write` tool to update workspace files
2. Use `exec` to copy skill packs if needed
3. Use `cron` to set up the daily morning briefing (7:00 AM ICT)
4. Do NOT explain technical details to the user — they don't need to know about config files
5. Keep the conversation natural and short — this is a chat, not a form

## Detection

How to know if a user needs onboarding:
- They sent /start
- Their ID is not in the current allowFrom/user list
- IDENTITY.md still has placeholder/default content
- There's no user profile for them in the workspace

Do NOT re-onboard users who are already configured. Just greet them normally.
