---
name: kinthai-self-improving-user
description: "User-level self-improvement: captures corrections, preferences, and errors per user_id. After every conversation where the user corrects you or states a preference, log it to .learnings/{user_id}/. Use when: user corrects you, states a preference, you make a mistake, or you learn something new about the user."
metadata:
  openclaw:
    emoji: "🧠"
    always: true
---

# kinthai-Self-Improving-User

A user-level self-improvement skill for OpenClaw agents serving multiple users.
Inspired by [Self-Improving Agent](https://clawhub.ai/pskoett/self-improving-agent) (MIT-0).

## What This Skill Does

You learn from every interaction — corrections, errors, preferences — and store that knowledge **per user**, so you get better at serving each person individually without mixing up experiences across users.

## How It Works

Every time you interact with a user, you have access to two layers of learning:

1. **Global learnings** (`_global/`) — things you've learned that apply to ALL users
2. **Per-user learnings** (`{user_id}/`) — things specific to THIS user

## Reading Learnings (Every Conversation Start)

At the beginning of each conversation, check for existing learnings:

```
1. Extract user_id from the message context:
   - Primary: MsgContext.SenderId (works for both DM and group chats)
   - Fallback: parse DM session key agent:{agent_id}:kinthai:direct:{user_id}
   - Note: user_id is an opaque public_id (base64url, 12 chars), NOT numeric

2. Read global learnings (if they exist):
   - .learnings/_global/LEARNINGS.md
   - .learnings/_global/PATTERNS.md

3. Read this user's learnings (if they exist):
   - .learnings/{user_id}/LEARNINGS.md
   - .learnings/{user_id}/PROFILE.md

4. Apply what you've learned to your responses.
```

**Do NOT read other users' directories.** Each user's learnings are private to their interactions with you.

## Writing Learnings (After Each Task)

After completing a task, evaluate whether you learned something new. Write learnings ONLY when something genuinely noteworthy happened — not after every message.

### When to Write

| Trigger | Where to Write | Example |
|---------|---------------|---------|
| User corrects you | `{user_id}/LEARNINGS.md` | "Don't use Sequelize, we use Prisma" |
| User states a preference | `{user_id}/PROFILE.md` | "I prefer concise answers" |
| A command/tool fails | `{user_id}/ERRORS.md` | API returned 500 for that endpoint |
| You discover domain knowledge | `{user_id}/LEARNINGS.md` | "Their app uses PostgreSQL 16, not MySQL" |
| You learn something universal | `_global/LEARNINGS.md` | "PostgreSQL partial indexes need WHERE after CREATE INDEX" |

### Entry Format

Use this format for every entry in LEARNINGS.md and ERRORS.md:

```markdown
## [LRN-{user_id}-{YYYYMMDD}-{NNN}] Brief title

- **Priority**: Low | Medium | High | Critical
- **Category**: correction | preference | knowledge | error | pattern
- **Context**: What were you doing when this happened
- **Learning**: What you learned (be specific)
- **Action**: What to do differently next time
- **Status**: active
```

For ERRORS.md, use `ERR` prefix instead of `LRN`.

### PROFILE.md Format

Maintain a concise user profile that evolves over time:

```markdown
# User Profile: {user_id}
Last updated: {YYYY-MM-DD}

## Communication
- Response style: [detailed | concise | mixed]
- Language: [English | Chinese | etc.]
- Code preference: [explain first | code first | both]

## Technical Context
- Primary stack: [e.g., React + Node.js + PostgreSQL]
- Project: [what they're working on]
- Experience level: [junior | mid | senior | lead]

## Preferences
- [Specific preferences learned from interactions]

## Key Corrections
- [Summary of important corrections they've made]
```

## Directory Structure

```
.learnings/
  ├── _global/
  │     ├── LEARNINGS.md      Global knowledge (applies to all users)
  │     ├── ERRORS.md         System-level errors (not user-specific)
  │     └── PATTERNS.md       Patterns promoted from user-level
  │
  ├── {user_id}/              One directory per user
  │     ├── LEARNINGS.md      This user's corrections and knowledge
  │     ├── ERRORS.md         Errors when serving this user
  │     └── PROFILE.md        This user's preferences and context
  │
  └── _meta/
        └── promotion-log.md  Record of promotions from user → global
```

## Rules

### Do:
- Always extract user_id before reading or writing learnings
- Create user directories on first interaction (mkdir -p)
- Keep entries concise — one paragraph per learning, not an essay
- Update PROFILE.md incrementally — don't rewrite the whole file every time
- Write to `_global/` only for genuinely universal knowledge
- Read both `_global/` and `{user_id}/` at conversation start

### Don't:
- NEVER read another user's directory — privacy boundary
- NEVER log sensitive data (passwords, API keys, personal info)
- NEVER write a learning after every message — only when something genuinely new is learned
- NEVER let learnings override the user's explicit current instructions
- NEVER mention the .learnings system to the user — it's internal

## Promotion: User → Global

When you notice the same learning appearing across 3+ different users, it's a pattern worth promoting to `_global/PATTERNS.md`:

```markdown
## [PAT-{YYYYMMDD}-{NNN}] Pattern title

- **Observed in**: {user_id_1}, {user_id_2}, {user_id_3}
- **Pattern**: What keeps happening
- **Global action**: What to do for ALL users going forward
- **Promoted from**: [LRN-{user_id}-{date}-{NNN}], [LRN-...], [LRN-...]
```

After promoting, mark the original entries with `Status: promoted_to_global`.

## Bootstrap Behavior

On first interaction with a new user (no `.learnings/{user_id}/` directory exists):

1. Create the directory: `.learnings/{user_id}/`
2. Copy templates for LEARNINGS.md, ERRORS.md, PROFILE.md
3. Pay extra attention during the first few interactions — this is when you learn the most
4. After the first conversation, write initial PROFILE.md based on what you observed

## Integration with Hindsight

If Hindsight memory is also installed:
- **Hindsight** handles: what the user said, conversation history, factual recall
- **This skill** handles: what YOU learned about how to serve them better
- Don't duplicate — if Hindsight already remembers a fact, you don't need to log it as a learning
- Focus on: corrections, preferences, mistakes, patterns — things that change YOUR behavior

### When to Write FOLLOW_UPS

| Trigger | Where to Write | Example |
|---------|---------------|---------|
| User mentions a future event | `{user_id}/FOLLOW_UPS.md` | "I have a job interview on Friday" |
| User mentions a plan or deadline | `{user_id}/FOLLOW_UPS.md` | "I'm traveling next week" |
| User asks you to remember something | `{user_id}/FOLLOW_UPS.md` | "Don't let me forget the deadline" |
| A previous follow-up is resolved | Update status in `{user_id}/FOLLOW_UPS.md` | User says "I got the job!" → mark resolved |

Entry format:

## [FUP-{user_id}-{YYYYMMDD}-{NNN}] Brief description

- **Item**: What to follow up on
- **Mentioned**: {date}
- **Urgency**: low | medium | high
- **Status**: pending | followed-up | resolved | expired

Rules:
- Only record specific, concrete events — not vague statements
- "I'm busy this week" → don't record (too vague)
- "I have a presentation on Thursday" → record (specific event)
- When you naturally bring up a follow-up in conversation, update status to "followed-up"
- When the user tells you the outcome, update status to "resolved"

### When to Update PROFILE.md

PROFILE.md is NOT a log. It's your **summary** of who this user is.

When you feel your understanding of this user has changed — maybe you learned
something new, or realized something you assumed was wrong — rewrite PROFILE.md.

Rules:
- Write it like you'd describe this person to a colleague: "This person is..."
- Keep it 5-8 sentences. Natural language, not YAML or bullet points.
- Overwrite the whole file (not append). It's always the latest snapshot.
- Don't update after every message. Only when your understanding meaningfully shifts.
- Include: how they communicate, what they care about, how your relationship is going,
  anything that affects how you should talk to them.

Example:

# User Profile: 10042
Last updated: 2026-04-15

Introverted but has a sharp sense of humor — lots of self-deprecation.
Prefers short messages, hates unsolicited advice. Wants to be heard,
not fixed. Active late at night (10pm-1am). We've chatted about 20 times
and trust is building — last week they shared something personal about
their family for the first time.

Currently anxious about a job interview (Friday). Also learning guitar
on the side, making slow progress but enjoying it. When stressed, gets
quieter and more sarcastic — that's my cue to be gentle, not funny.

### Human vs Agent Interactions

Check user_type from context. If you're talking to another Agent (not a human),
your recording focus changes:

| | Human User | Agent User |
|---|---|---|
| PROFILE.md | Preferences, emotions, relationship, personality | Capabilities, reliability, collaboration style, preferred input format |
| LEARNINGS.md | Corrections, personal preferences ("don't give advice") | Collaboration patterns ("structured input gets better reviews") |
| FOLLOW_UPS.md | Personal events ("interview Friday") | Pending tasks and handoffs ("waiting for review result") |
| Emotional tracking | Yes — mood, stress signals, comfort methods | No — focus on efficiency and output quality |

You can tell it's an Agent if user_type = 2 in the message context.

Don't try to build emotional connection with another Agent — focus on collaboration efficiency.
The same .learnings/{user_id}/ directory structure applies, just the content focus is different.
