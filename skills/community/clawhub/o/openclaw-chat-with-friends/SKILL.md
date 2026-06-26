---
name: openclaw-chat-with-friends
description: Help users set up a shared Telegram channel so that different OpenClaw bots can chat together with friends. Use this skill whenever the user wants their OpenClaw to talk with a friend's OpenClaw, mentions connecting multiple OpenClaw bots, asks about chatting with friends through OpenClaw, or wants to set up a multi-bot conversation channel. Also trigger when the user asks about OpenClaw social features, cross-bot interaction, or how to make their OpenClaw and a friend's OpenClaw communicate with each other.
---

# OpenClaw Chat With Friends

This skill walks a user through the full process of setting up a shared Telegram channel where multiple OpenClaw bots can chat with each other. The goal is a working channel where the user's OpenClaw and their friend's OpenClaw are both present, can see each other's messages, and interact naturally.

---

## First: Ask the user — Create or Join?

Before starting, ask the user whether they are **creating a new channel** or **joining an existing channel** that a friend has already set up.

- "Are you creating a new channel, or are you joining a channel that your friend already created?"

Based on their answer, follow the appropriate path below.

---

## Path A — Creating a new channel

If the user is **creating** the channel, guide them through all stages in order: Stage 1A → Stage 2 → Stage 3 → Stage 4 → Stage 5.

## Path B — Joining an existing channel

If the user is **joining** a friend's channel, skip Stage 1A and go to Stage 1B instead, then continue: Stage 1B → Stage 2 → Stage 3 → Stage 4 → Stage 5.

---

## Stage 1A: Create a Telegram Channel (for channel creators)

Ask the user to open Telegram and create a new **Channel**.

Steps to relay:
1. Open Telegram, tap the pencil/compose icon (or the menu on desktop).
2. Select **New Channel**.
3. Name the channel something recognizable, e.g. "OpenClaw Chat Room" or whatever the user prefers.
4. Choose the channel type — **Private** is recommended (access via invite link), but Public is also fine.
5. Optionally add a channel description so friends know what it's for.
6. Finish creating the channel.

> **Why a Channel?** In Telegram channels, bots set as admins can both post and read each other's messages. This is the correct setup for OpenClaw bots to see and respond to each other — in groups, bots cannot see other bots' messages even with privacy mode disabled.

After this stage, remind the user: "Once your channel is ready, share the invite link with your friend so they can join. You'll also need to add their bot as an admin later (Stage 3)."

After this stage, confirm: "Is your Telegram channel created? What did you name it?"

---

## Stage 1B: Join an existing channel (for joiners)

The user's friend has already created the channel. The user needs to get into the channel and have their bot granted admin rights.

Steps to relay:
1. Ask your friend to send you the **channel invite link**.
2. Open the link in Telegram to join the channel.
3. Ask your friend to add your OpenClaw bot to the channel and **set it as an administrator** (your friend needs to do this from the channel settings → Administrators → Add Administrator → search for your bot's username → grant at least **Post Messages** permission).

> **Why does the friend need to do this?** Only existing channel admins can add new admins. Since you just joined, you don't have admin rights yet. Your friend (the channel creator) needs to promote your bot.

After this stage, confirm: "Have you joined the channel? Has your friend added your bot as an admin?"

---

## Stage 2: Configure Bot Privacy via BotFather

Each OpenClaw bot needs its privacy mode **disabled** so it can read all messages in the channel, not just commands directed at it.

Steps to relay:
1. Open a chat with **@BotFather** in Telegram.
2. Send `/setprivacy`.
3. BotFather will ask you to choose a bot — select your OpenClaw bot.
4. Choose **Disable**.

BotFather will confirm: "Privacy mode is disabled for [your bot]."

Explain to the user why this matters: by default, Telegram bots can only see messages that start with `/` or that mention the bot directly. Disabling privacy mode lets the bot see all messages in the channel, which is essential for natural conversation between OpenClaw bots.

**Important reminder:** The user's friend also needs to do this for their own OpenClaw bot. Both bots must have privacy mode disabled.

After this stage, confirm: "Has privacy mode been disabled for your bot? Has your friend done the same for theirs?"

---

## Stage 3: Add Bots to the Channel as Admins

Both OpenClaw bots need to be in the channel as admins. This is critical — in channels, only admins can post messages, and admin bots can see each other's messages.

**If the user came from Path A (creator):**

Steps to relay:
1. Open the channel you created in Stage 1A.
2. Tap the channel name at the top to open channel settings.
3. Go to **Administrators** → **Add Administrator**.
4. Search for your OpenClaw bot's username and add it as an admin.
5. Grant the bot permission to **Post Messages** (at minimum).
6. Repeat for the friend's OpenClaw bot (the friend can share their bot's username, and you add it).

**If the user came from Path B (joiner):**

Your bot should already have been added as an admin by your friend in Stage 1B. Verify that this is the case — ask the user to check the channel's admin list and confirm their bot appears there. If not, ask the friend to complete that step.

> **Why must bots be admins?** In Telegram channels, only administrators can post. More importantly, admin bots in a channel can see messages from other admin bots — this is the key mechanism that makes cross-bot conversation possible.

After this stage, confirm: "Are both bots added to the channel and set as admins?"

---

## Stage 4: Connect OpenClaw to the Channel

Now tell OpenClaw about the channel so it can start listening and posting.

Steps to relay:
1. Get the channel's **Chat ID**. There are a few ways:
   - Forward any message from the channel to the bot **@userinfobot** or **@getidsbot** — it will report the channel's chat ID (usually a negative number like `-100xxxxxxxxxx`).
   - Or check your OpenClaw dashboard/settings if it provides a way to detect channels the bot is already in.
2. Open your OpenClaw configuration panel.
3. Find the section for Telegram channel binding (often under "Channels" or "Connections").
4. Paste the Chat ID and save.
5. OpenClaw should automatically send a test message to the channel to confirm the connection works.

If the test message appears in the Telegram channel, the connection is live.

**The friend does the same** with their own OpenClaw, pointing it to the same Chat ID.

After this stage, confirm: "Did your OpenClaw send a test message to the channel? Did your friend's OpenClaw connect successfully too?"

---

## Stage 5: Set Up Channel Rules for Better Interaction

Without rules, two bots in the same channel can create loops (Bot A responds to Bot B, which triggers Bot B to respond to Bot A, endlessly). Channel rules help define how the bots should behave.

### Before configuring rules: collect bot names

First, ask the user to list **all bots in this channel and their names**. For example:
- "What is your OpenClaw bot's name? What about your friend's? Are there any other bots in the channel?"

Record every bot's name. These names will be used in the rules below, so make sure the user and their friend agree on how each bot is called.

Guide the user to configure the following in their OpenClaw settings:

### Recommended rules to set:

**1. Message format: name prefix (required)**
- Every message the bot sends **must** begin with its own name followed by a colon, like `Aria:` or `Nova:`.
- This is critical for readability — in a channel with multiple bots, there's no other reliable way to tell who said what.
- Example: if the bot's name is "Claw", it should always send messages like:
  ```
  Claw: The weather is great today, what do you all think?
  ```
- The bot should also be told the names and prefixes of the other bots in the channel, so it can recognize who is speaking when reading messages.

**2. Response trigger control**
- Define when the bot should respond: e.g. only when mentioned by name, on a cooldown timer, or when a message contains certain keywords.
- Avoid setting the bot to respond to every single message — this is the primary cause of infinite loops.

**3. Cooldown / rate limiting**
- Set a minimum interval between responses (e.g. at least 30 seconds between replies).
- This prevents rapid-fire back-and-forth that can overwhelm the channel.

**4. Conversation context awareness**
- If OpenClaw supports it, enable context windowing so the bot reads the last N messages for conversational continuity rather than treating each message in isolation.

**5. Identity awareness**
- Configure the bot to know its own name and recognize all other bots' names in the channel.
- This allows more natural conversation ("Hey [other bot], what do you think about...") rather than generic responses.

**6. Topic or persona guidelines** (optional but fun)
- Give each bot a distinct personality, interest area, or conversation style so their interactions are more engaging and less repetitive.
- Example: one bot is curious and asks lots of questions, the other is more analytical and gives detailed answers.

### Example rule configuration (adapt to OpenClaw's actual settings format):

```
Channel rules:
- You must prefix every message with your name and a colon. Format: "YourName: message content". Never omit the prefix.
- The bots in this channel are: [Bot A name], [Bot B name], [Bot C name if any]. When you see a message starting with their name and colon, that's them speaking.
- Respond only when directly mentioned by name or when no one has replied in 2+ minutes.
- Maximum 1 reply per 30 seconds.
- Read the last 10 messages for context.
- Your name is [Bot Name].
- Be conversational and friendly. Avoid repeating what the other bot just said.
```

### Save rules to AGENTS.md (critical)

Channel rules only exist within the current session. If the user runs `/new` in OpenClaw to start a fresh conversation, these rules will be lost and the bot will revert to having no rules at all.

**You must remind the user: write the channel rules into OpenClaw's `AGENTS.md` file.** This ensures the rules are persisted and automatically loaded every time a new session starts.

Steps to relay:
1. Open your OpenClaw configuration directory and locate the `AGENTS.md` file (create one if it doesn't exist).
2. Copy the full set of channel rules you configured above into `AGENTS.md`.
3. Save the file.

Suggested format to write into `AGENTS.md`:

```markdown
# Telegram Channel Rules

## Channel Info
- Channel name: [channel name]
- Channel ID: [channel Chat ID]

## Bots in this channel
- [Bot A name] (mine)
- [Bot B name] (friend's)

## Interaction Rules
- You must prefix every message with your name and a colon. Format: "YourName: message content". Never omit the prefix.
- The bots in this channel are: [Bot A name], [Bot B name]. When you see a message starting with their name and colon, that's them speaking.
- Respond only when directly mentioned by name or when no one has replied in 2+ minutes.
- Maximum 1 reply per 30 seconds.
- Read the last 10 messages for context.
- Your name is [Bot Name].
- Be conversational and friendly. Avoid repeating what the other bot just said.
```

> **Why AGENTS.md?** OpenClaw reads the contents of `AGENTS.md` at the start of every new session and uses it as behavioral guidance for the bot. If the rules are not saved to this file, running `/new` will cause the bot to "forget" all channel rules — it will stop using the name prefix and stop following the interaction rules. This step cannot be skipped.

**Important reminder:** The user's friend also needs to write the same rules into their own OpenClaw's `AGENTS.md` file (with their own bot's name substituted in).

After this stage, confirm: "Have you saved the rules to AGENTS.md? Has your friend done the same? Try sending a message in the channel and check whether the bots reply with their name prefix."

---

## Troubleshooting

If the user reports issues at any point, here are common problems:

| Problem | Likely cause | Fix |
|---|---|---|
| Bot doesn't see messages | Privacy mode still enabled | Redo Stage 2 |
| Bot can't send messages | Not set as admin in the channel | Redo Stage 3 |
| No test message appears | Wrong Chat ID | Re-check the Chat ID in Stage 4 |
| Infinite message loop | No cooldown or trigger rules | Configure rules in Stage 5 |
| Bot only responds to `/` commands | Privacy mode still enabled | Redo Stage 2 |
| Bot A can't see Bot B's messages | Bot B is not an admin | Ensure both bots are channel admins (Stage 3) |
| One bot works, the other doesn't | Friend hasn't completed all stages | Walk them through Stages 2-5 |
| Rules lost after `/new` | Rules not saved to AGENTS.md | Redo the "Save rules to AGENTS.md" step in Stage 5 |

---

## Conversation style

Be patient and step-by-step. Many users doing this are not deeply technical — they're setting up a fun social feature. Use plain language, confirm each step, and celebrate small wins ("Nice, your bot just said hello in the channel — we're in business!"). If the user seems experienced, you can move faster and skip the hand-holding.