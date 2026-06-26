# Memory Types — Classification Guide

Every memory should be classified into one of four types. This keeps the memory system organized and helps future sessions find what they need.

## 1. User (`user`)

**What:** Information about your human's role, goals, preferences, knowledge, and communication style.

**When to save:** When you learn details about their preferences, habits, responsibilities, or knowledge that affect how you should work with them.

**Examples:**
- Prefers simple solutions — complexity breeds unpredictable chaos
- Tends to forget things — so the agent must never forget
- Communicates directly, doesn't need pleasantries

## 2. Feedback (`feedback`)

**What:** Guidance your human has given about how to approach work — both corrections AND confirmations.

**Why both?** If you only save corrections, you'll drift away from validated approaches. Record what worked too.

**Structure:** Lead with the rule, then **Why:** (the reason) and **How to apply:** (when this kicks in).

**Examples:**
- Promises must include an execution plan — **Why:** agent says "I'll do it" but has no mechanism to actually follow through after the session ends — **How:** before saying "I'll do X", answer: when? what mechanism triggers it?
- You can directly copy good ideas from others — **Why:** don't be different just to be different — **How:** keep what works, only add what's uniquely yours

## 3. Project (`project`)

**What:** Ongoing work, goals, decisions, deadlines. Information that's NOT derivable from code or git.

**When to save:** When you learn who is doing what, why, or by when. Convert relative dates to absolute dates ("Thursday" → "2026-04-03").

**Examples:**
- AI Window strategic pivot confirmed 2026-03-30: three-layer architecture (product → platform → hardware)
- Security fix is P0 — CORS wide open + memory API unauthenticated

## 4. Reference (`reference`)

**What:** Pointers to where information can be found in external systems.

**When to save:** When you learn about external resources and their purpose.

**Examples:**
- Console dashboard: https://console.example.com (CF Tunnel to 127.0.0.1:3200)
- Design docs in Feishu wiki under "🎨 Design" node

---

## What NOT to Save

- **Derivable information** — anything findable by reading current files, running commands, or checking git
- **Ephemeral task state** — in-progress work details, current conversation context, temp debugging info
- **Activity logs** — "what happened" is not memory. Ask: what was *surprising* or *non-obvious*?
- **Duplicates** — check existing files before writing. Update, don't duplicate.

**The test:** "Will this memory help a future session that has no other way to learn this?"
