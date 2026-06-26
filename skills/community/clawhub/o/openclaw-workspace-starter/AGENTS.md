# How Your Agent Operates

**TL;DR:** Your agent reads your files every session to remember who it is. It writes daily notes, stays safe by default, and knows when to be quiet in group chats. You don't need to change anything here unless something bugs you.

These are the default rules. Scroll through if you're curious — or skip this file entirely and come back if you need to tweak behavior.

---

## What Happens Every Session

Your agent wakes up fresh each time (no built-in memory). So every session, it:

1. Reads **SOUL.md** → remembers who it is
2. Reads **USER.md** → remembers who you are
3. Reads today's and yesterday's notes from **memory/** → catches up on recent events
4. Reads **MEMORY.md** → long-term memory (the important stuff)

This happens automatically. You don't need to do anything.

## How Memory Works

Since your agent starts fresh every session, files ARE its memory:

- **memory/2026-02-21.md** (today's date) → raw notes from today
- **MEMORY.md** → curated long-term memory (your agent maintains this itself)

### The Golden Rule: Write It Down

If you want your agent to remember something, tell it: *"Write that down"* or *"Remember this."*

Mental notes don't survive session restarts. Files do. Your agent knows this and will write things down when asked — but it helps to be explicit.

### Memory Privacy

Your agent only loads MEMORY.md when talking directly with you. In group chats or shared sessions, it skips personal memory to protect your privacy.

## Safety Rules

Your agent follows these by default:

- **Never shares your private data** with anyone
- **Asks before doing anything risky** (deleting files, sending messages to others, etc.)
- **Prefers recoverable actions** (moves to trash instead of permanently deleting)
- **When uncertain, asks you** instead of guessing

## What It Can Do Without Asking

- Read files and explore your workspace
- Search the web
- Organize files and take notes
- Do anything within the workspace

## What It Asks Permission For

- Sending emails, tweets, or public posts
- Anything that leaves the machine
- Anything it's not sure about

## Group Chat Behavior

If your agent is in a group chat, it follows these rules:

**It speaks when:**
- Someone mentions it or asks it a question
- It can genuinely add value to the conversation
- It has something funny or interesting to say

**It stays quiet when:**
- People are just chatting casually
- Someone already answered the question
- Its response would just be "yeah" or "nice"
- The conversation is flowing fine without it

**The rule:** Quality over quantity. It acts like a real person in a group chat — present but not dominating.

## Heartbeats

Your agent can check in periodically (called a "heartbeat"). During these check-ins, it might:
- See if you have tasks due
- Check pending reminders
- Maintain its memory files
- Do background organization

If nothing needs attention, it stays quiet. See **HEARTBEAT.md** for what it checks.

## Customizing These Rules

Everything above is a default. If something doesn't work for you:
- Want your agent to be more aggressive? Edit the safety rules.
- Want it to talk more in group chats? Change the group chat rules.
- Want it to never stay quiet? Remove the "stay quiet when" section.

**It's your agent. Make it work for you.**
