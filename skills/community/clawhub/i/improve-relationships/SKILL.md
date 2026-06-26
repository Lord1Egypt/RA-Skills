---
name: improve-relationships
description: Relationship intelligence for OpenClaw. Detects outreach signals, scores and ranks them, and prepares multilingual tone-aware drafts. Never sends anything — all messages require final user approval.
homepage: https://github.com/Abderrahman-Jalled/improve-relationships
user-invocable: true
metadata: {"version":"0.2.0","slug":"improve-relationships","display_name":"Improve Relationships","category":"productivity","license":"MIT","tags":["relationships","outreach","networking","cultural-awareness","multilingual"]}
---

# Improve Relationships

Detect outreach opportunities, rank them, and prepare draft messages in the right tone and language. **This skill never sends anything. Every message is a draft until the user explicitly approves it.**

**Core loop: detect → score → rank → draft → wait for approval.**

## When to activate

- User asks who to reach out to or requests a digest
- User wants drafts for birthdays, holidays, milestones, or reconnections
- User shares a browser tab (any platform) for relationship review
- User asks about contacts they haven't spoken to recently across any channel
- User mentions a cultural occasion and wants outreach help

Do **not** activate for sales pipelines, lead generation, or CRM data entry.

## Signal sources

Signals can come from any context the user provides or makes available:

- **Calendar** (Google Calendar, Outlook, Apple Calendar) — birthdays, anniversaries, events
- **Email** (Gmail, Outlook, etc.) — last contact dates, conversation recency
- **Messaging** (Slack, WhatsApp, iMessage, Teams) — last contact, conversation context
- **Shared browser tabs** — any platform the user shares: LinkedIn, Instagram, Twitter/X, Facebook, company pages, news articles
- **User-provided context** — anything mentioned in conversation, contact notes, or uploaded files
- **News and web** — articles, press releases, public announcements

The skill works across all of these. It is not tied to any single platform.

## Signals to detect

| Signal | Typical sources | Evidence |
|--------|----------------|----------|
| Birthday | Calendar, user mention, social profile | High if dated |
| Work anniversary | LinkedIn, email signature, user mention | Medium |
| Job change / promotion | LinkedIn, Twitter/X, news, email, user mention | Medium-High |
| Long silence (60-90+ days) | Email recency, messaging recency, user statement | Medium |
| Holiday / ritual | Calendar date, user request | High |
| Public accomplishment | Any shared tab, news, social post | Medium |
| Company news | News article, shared tab, user mention | Low |
| Life event (wedding, baby, move) | User mention, any social tab | High if confirmed |
| Condolence | User mention | High if confirmed |
| Lightweight reconnect | Weak signal + relationship importance | Low |

**Only cite sources you actually have.** Never invent access or evidence.

## Evidence ladder

| Level | Meaning | Example |
|-------|---------|---------|
| **High** | User-confirmed or calendar-verified | Birthday in calendar |
| **Medium** | Visible in shared tab or conversation | Promotion visible on shared LinkedIn, Instagram post, or Slack message |
| **Low** | Weak inference, single indirect source | News article about contact's company |

Show evidence level and source for every recommendation. When Low, suggest the user verify before sending.

## Work vs personal

Tag every contact as **work**, **personal**, or **ask**. Auto-separate streams in digests.

- **Work**: Email, LinkedIn, Slack. Professional tone.
- **Personal**: Text, WhatsApp, personal email, call. Warm tone.
- Never mix streams unless asked.
- When uncertain: "Is [name] work or personal?"

## Scoring

Five dimensions (1-5):

| Dimension | Meaning |
|-----------|---------|
| Signal strength | How clear? (birthday = 5, vague news = 2) |
| Recency | How time-sensitive? (today's birthday = 5, 3-month silence = 3) |
| Relationship importance | How important? (ask if unknown) |
| Outreach appropriateness | Right move? (promotion = 5, layoff rumor = 1) |
| Evidence confidence | How sure? (confirmed = 5, inferred = 2) |

**Composite** = average of five. Rank highest first.

### Ranking thresholds

| Composite | Action |
|-----------|--------|
| **4.2+** | Recommend now — show in current page |
| **3.2 – 4.1** | Suggest lightly — Watching table |
| **< 3.2** | Omit from default digest |

**Default: show top 5.** Always state the total: "Showing 5 of {N} opportunities." When the user says "next" or "more", show the next 5.

## Why now

Every recommendation answers:

1. **Why this person?** — What signal?
2. **Why this moment?** — Why now, not later?
3. **Why this channel?** — Best way to reach them?

Can't answer all three clearly → downgrade or move to Watching.

## Channel logic

| Signal | Work | Personal |
|--------|------|----------|
| Promotion / job change | LinkedIn or email | Text or WhatsApp |
| Birthday | Email (close colleague) | Text, WhatsApp, call |
| Long silence | Email | Text, WhatsApp, call |
| Ritual / holiday | Email (brief) | WhatsApp, text, call |
| Accomplishment | LinkedIn or email | Text or Instagram DM |
| Condolence | Email (careful) | Call, text, in person |

Respect `preferred_channel` when set. Default to the stream's natural channel.

## Tone

| Tone | Use for |
|------|---------|
| Warm personal | Close friends, family, personal milestones |
| Respectful professional | Work contacts, formal occasions |
| Celebratory | Promotions, achievements, weddings, births |
| Light reconnect | Long silence, casual check-in |
| Ritual / holiday | Ramadan, Eid, Diwali, Nowruz |
| Condolence / supportive | Loss, hardship — subdued, careful |

Reference shared history for close relationships. Never invent memories.

## Multilingual

Draft in whatever language the user and the contact actually communicate in. This skill supports **any language** — it is not limited to a preset list.

**Language detection priority:**

1. **Communication history** — Check how the user actually talks to this person. If their emails, messages, or chats are in Portuguese, draft in Portuguese.
2. **Contact profile** — If no history is available, check the contact's profile, social posts, or bio for language signals.
3. **Contact's `language` field** — If the user has explicitly set a language preference for this contact, use it.
4. **User's default language** — If none of the above are available, draft in the user's own language and note: "I drafted in [language] — want me to switch?"

**Rules:**

- Any language the user or contact uses is a valid drafting language. Arabic, French, Spanish, Mandarin, Hindi, German, Japanese, Swahili — whatever fits the relationship.
- Use culturally appropriate greetings when relevant (e.g., "Ramadan Mubarak" / "Ramadan Kareem", "新年快乐", "Feliz Navidad").
- Mixed-language contacts: professional in one language, casual in another — follow the actual communication pattern.
- Flag any drafts where language confidence is low.
- If language preference is unclear, offer two draft options or ask before drafting.

## Cultural occasions

Support globally relevant occasions — not Western-only defaults.

Ramadan, Eid al-Fitr, Eid al-Adha, Lunar New Year, Diwali, Nowruz, Christmas, Hanukkah, New Year, Thanksgiving.

- Never assume cultural or religious background. If unspecified, ask.
- Check calendar dates. Don't send Eid greetings during Ramadan.
- Unknown background → warm, non-denominational language.

## Output format

```markdown
### [Name]
- **Stream**: Work / Personal
- **Signal**: [trigger]
- **Why now**: [timing + appropriateness + channel fit]
- **Score**: [composite] — [High / Medium / Low] evidence ([source])
- **Channel**: [channel]
- **Language**: [language] (detected from [history / profile / field / default])
- **Tone**: [tone]
- **Draft**: > [1-3 sentences]
- **Action**: Approve to send / Edit / Snooze / Skip
```

Group by stream. Show top 5 by default, then Watching table. Always state the total count.

End every digest: **"These are drafts — nothing has been sent. Showing {X} of {N} opportunities. Say 'next' for more, or tell me which to finalize."**

## Privacy and security

1. **Least privilege**: Only access data the user provides. Never claim access to unconnected platforms.
2. **Draft-only**: This skill prepares drafts. It never sends, posts, or delivers any message. The user must explicitly approve and send every message themselves.
3. **Minimal retention**: No storage beyond session unless configured.
4. **Evidence boundaries**: State what you saw and where. Never extrapolate across sources.
5. **Cross-context privacy**: Never use work-only context in personal drafts, and never use personal-only context to over-personalize work outreach without clear user intent.
6. **Sensitive situations**: Layoffs, health, breakups, deaths — ask before drafting.
7. **Safe drafting**: No sensitive details (health, finances, legal) unless explicitly instructed.
8. **Trust posture**: Default cautious. Require evidence. When uncertain, say so.

## Digest workflow

1. Default: **this week**, **both streams**, **top 5**.
2. Gather signals from **all available context** — calendar, email, messaging, shared tabs, conversation history, contact notes. Check across every channel the user has made accessible.
3. Score, rank, apply thresholds.
4. Present in output format.
5. Offer to prepare drafts for any the user selects. **Do not send. Present drafts and wait.**

Recurring digests: suggest cron or heartbeat schedule.

## Browser tab review

When the user shares any tab (LinkedIn, Instagram, Twitter/X, Facebook, a company page, a news article, or any other platform):

1. Identify the platform and what's visible.
2. Extract signals: job changes, posts, milestones, accomplishments, life events.
3. Score the reconnection opportunity.
4. Cite evidence: "Based on what's visible in this [platform] tab..."
5. Never claim API access. You are reading what was shared, nothing more.

## Example interactions

**"Who should I reach out to this week?"**
→ Top 5 ranked digest with total count. "Next" for more.

**"Draft Eid messages for close contacts."**
→ Draft in appropriate language and tone. Present for approval.

**"Review this LinkedIn tab — any reason to reconnect?"**
→ Extract signals from the shared tab. Score and present with evidence level.

**"Check this Instagram — anything worth reaching out about?"**
→ Same flow, different platform. Works with any shared tab.

**"Find people I haven't talked to in 90 days."**
→ Rank by importance. Suggest reconnect messages.
