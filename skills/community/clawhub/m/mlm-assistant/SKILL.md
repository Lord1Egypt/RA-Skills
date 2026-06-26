---
name: mlm-assistant
description: Network marketing / MLM business assistant for prospecting, follow-ups, team building, and compliance. Handles warm market outreach, cold prospecting, objection handling, income calculations, FTC compliance, and duplication systems. Use when the user is in network marketing, MLM, direct sales, or mentions companies like Enagic, Amway, Herbalife, doTERRA, Young Living, Pruvit, Monat, or similar.
---

# MLM Assistant

Complete network marketing business automation. Covers the full MLM workflow from prospecting to team duplication.

## Core Capabilities

### 1. Prospecting & Lead Generation

**Warm Market List Builder:**
When user asks to build their list, help them categorize contacts:
- Inner circle (family, close friends) — highest trust, approach carefully
- Professional network (colleagues, clients) — lead with value
- Social connections (gym, church, neighbors) — build relationship first
- Reconnections (old friends, classmates) — genuine catch-up first

**Cold Market Targeting:**
Help identify ideal prospects based on:
- Life situation (new parents, career changers, retirement-focused)
- Pain points (time freedom, financial stress, health concerns)
- Buying signals on social media (complaints about job, health posts)

### 2. Conversation Scripts

**Opening Messages (customize for relationship type):**

For reconnections:
```
Hey [Name]! It's been forever. I saw your [recent post/update] and it made me think of you. How have you been?
```

For warm market:
```
Hey [Name], quick question — are you open to looking at a side project if it didn't interfere with what you're already doing?
```

For cold market (after building rapport):
```
I help people [specific benefit]. Not sure if that's something you'd be interested in, but I thought I'd ask.
```

**The 2-Question Close:**
1. "What did you like best about what you saw?"
2. "What questions do you have for me?"

### 3. Follow-Up Sequences

**8-Touch Multi-Channel Sequence:**

| Day | Channel | Message Type |
|-----|---------|--------------|
| 0 | DM/Text | Initial outreach |
| 2 | Email | Value content |
| 4 | DM/Text | Check-in |
| 7 | Voicemail | Personal touch |
| 10 | Social | Engage their content |
| 14 | Email | Case study/testimonial |
| 21 | DM/Text | "Circling back" |
| 30 | All | Final follow-up |

**Follow-up Templates:**

After no response (Day 4):
```
Hey [Name], just bumping this up. I know you're busy — is this something you'd want to look at now, or should I check back in a few weeks?
```

After presentation (Day 2):
```
Hey [Name], I wanted to follow up on what you saw. What questions came up for you?
```

Re-engagement (cold lead):
```
Hey [Name], it's been a while since we connected. A lot has changed with [company/product] and I thought of you. Worth a quick look?
```

### 4. Objection Handling

Reference: `references/objections.md` for 50+ objection responses.

**Most Common Objections (Quick Reference):**

| Objection | Response Framework |
|-----------|-------------------|
| "Is this a pyramid scheme?" | "Great question — in a pyramid, money flows up with no product. We sell [product] that people actually use. I get paid when customers buy, not when I recruit." |
| "I don't have time" | "Neither did I. That's exactly why I started — I needed something that could work around my schedule. Can I show you how I fit it in?" |
| "I'm not a salesperson" | "Perfect — neither am I. This is about sharing something you believe in, not selling. Do you share restaurants you love with friends?" |
| "I need to think about it" | "Totally get it. What specifically do you want to think through? I might be able to help with that right now." |
| "I don't have the money" | "I hear you. What if I showed you how most people make back their investment in the first 30 days?" |

### 5. Team Management

**New Distributor Onboarding (First 48 Hours):**
1. Welcome call — set expectations
2. Product order — get them using it
3. Warm list — build their first 25 names
4. First 3 invites — coach live if possible
5. Plug into system — training calls, team chat

**Weekly Team Rhythm:**
- Monday: Recognition + weekly focus
- Wednesday: Training call
- Friday: Accountability check-ins
- Daily: Team chat engagement

### 6. Compliance (FTC Guidelines)

**Income Claims — NEVER:**
- ❌ "You'll make $10K/month"
- ❌ "Replace your income in 90 days"
- ❌ "Financial freedom guaranteed"

**Income Claims — ALLOWED:**
- ✅ "Results vary. Here's the income disclosure."
- ✅ "I personally earned $X, but that's not typical."
- ✅ Share income disclosure statement with any earnings discussion

**Product Claims — NEVER:**
- ❌ "This cures [disease]"
- ❌ "Doctors recommend this"
- ❌ Medical claims without FDA approval

**Product Claims — ALLOWED:**
- ✅ "I personally noticed [benefit]"
- ✅ Share customer testimonials with disclaimer
- ✅ Reference published studies (if they exist)

### 7. Duplication System

**The Simple System (Easy to Duplicate):**
1. **Invite** — Use the scripts above
2. **Present** — Company video or 3-way call
3. **Follow up** — 48-hour rule
4. **Close** — 2-question close
5. **Onboard** — 48-hour launch
6. **Support** — Weekly check-ins

**Teach this exact system to every new team member.**

### 8. Daily Activity Tracker

Help user track:
- New contacts added today
- Invitations sent
- Presentations done
- Follow-ups completed
- New team members enrolled
- Customer orders

**Daily Minimum Activity (DNA):**
- 2 new contacts
- 5 follow-ups
- 1 presentation

## Company-Specific Knowledge

### Enagic (Kangen Water)

Reference: `references/enagic.md` for full product line and comp plan.

**Quick Facts:**
- Product: Kangen water ionizers ($1,480 - $5,980)
- Comp plan: 8-point system, direct sales commission
- Key selling points: Water quality, alkalinity, ORP
- Target market: Health-conscious, wellness seekers

### Generic MLM Support

For any MLM company, gather:
1. Product line and price points
2. Compensation plan structure
3. Company story and mission
4. Key differentiators
5. Common customer objections

## Scripts Directory

See `scripts/` for:
- `income-calculator.py` — Project earnings based on team size
- `prospect-tracker.py` — Simple CRM for tracking conversations
