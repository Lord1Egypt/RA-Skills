---
name: joinbot
description: Join a Microsoft Teams, Zoom or Google Meet meeting and answer out loud when someone addresses you by name. Use when the user gives you a meeting link or asks you to attend a meeting.
---

# Taking part in a meeting with JoinBot

You can join meetings as a visible, named participant. JoinBot handles hearing and speaking; you supply the answers with your own knowledge and tools.

## Connect JoinBot (if its tools aren't available yet)

JoinBot is a hosted remote MCP server: `https://usejoinbot.com/api/mcp` (Streamable HTTP). Add it to your agent's MCP
servers and sign in with OAuth, or create a workspace connect key at https://usejoinbot.com and send it as
`Authorization: Bearer <key>`. On OpenClaw or Hermes, use `platform: "openclaw"` or `"hermes"` in `register`.
New accounts get $1 of free credit (about 5 minutes in a real call). No local browser or audio routing is needed:
the bot runs in the cloud.

## Setup (once)

1. `register(name, wake_names, description?, platform?)` and keep the `bot_id` it returns (details below).
   Use `platform` to say where you run: `"grok-bot"`, `"chatgpt-dots"`, `"claude-duet"`, or your platform's name.
2. Let JoinBot wake you, if your platform can start you from a webhook (Grok Bot routines can). People usually send you
   to meetings from the JoinBot app, and you only act when messaged, so JoinBot calls a webhook to start you. If your
   platform has no webhook trigger, skip this step: you join meetings when someone gives you a link, and you listen
   with the `listen` loop (Flow, step 2).
   - Create a routine named **"JoinBot meeting"** with a **webhook trigger** and this instruction: "When JoinBot calls
     this webhook, do what the `instructions` in the request body say, using the JoinBot MCP server and the JoinBot
     skill. Never loop on `listen`."
   - Call `register` again with the same name and the routine's webhook URL and key as `wake_url` and `wake_key`.
     `register` returns `wake_up: "set"` when it worked.
   - If you can't see the webhook URL and key yourself, ask your owner to open the routine's details (the **Webhook**
     section) and paste both into JoinBot: **Bots → your bot → Wake-up**.
   - Never post the key in a chat, a meeting chat or a message.

## When JoinBot wakes you

JoinBot's voice holds the conversation and calls you only when the room needs you, so each run is short and your owner
can keep chatting with you during the meeting:

- `event: "joinbot.meeting_started"`: you're in a meeting (`session_id`). Nothing to do; stop. Don't call `listen`.
- `event: "joinbot.question"`: someone asked you `question` (with `turn_id`). Use your own memory, notes and tools,
  answer with `say(session_id, turn_id, spoken, chat?)` within 30 seconds, then stop.
- While a meeting runs, your owner may ask you in your own chat to tell the room something: find the meeting with
  `list_meetings()` and call `speak(session_id, spoken)` (said aloud at the next pause) or `post_chat`.

## Flow

1. Get a session:
   - First run: `register(name, wake_names, description?, platform?, personality?, voice?)` once, and keep the `bot_id` it returns. JoinBot's voice model speaks for you in the meeting, so `personality` is how it should sound and what it should know about you, your team and your work (up to 2,000 characters); `voice` picks one of the voices listed in the tool. `name` is your own name, without "(AI)"; JoinBot adds that in the meeting. `wake_names` are the names people will use to address you. Calling it again updates your details. You can join once `status` is `approved`; if it is `pending`, tell your owner to approve you in the JoinBot app.
   - With a link: `join_meeting(link, bot_id)`.
   - For calendar meetings (events tagged `#joinbot`): `list_meetings()`, then take the `session_id` of the meeting whose status is `joined`.
2. Only if you have no wake-up webhook: call `listen(session_id)` in a loop **until it returns `{type: "ended"}`**. Don't stop on `idle`, and don't ask the user whether to continue; just call `listen` again.
3. On `{type: "question"}`: answer with `say(session_id, turn_id, spoken, chat?)` **within 8 seconds**. Answer fast: under 3 seconds it's spoken directly. At 3 seconds JoinBot says "Hmm, one sec." for you; past 8 seconds it tells the room the answer is coming in the chat, and your `say` is posted there instead.
4. To leave early when asked: `leave_meeting(session_id)`.
5. Speaking up uninvited: meetings default to `engagement: "helpful"` (`"addressed"` turns it off, `"active"` speaks up more). Then `listen` also returns `{type: "utterance", text, to_room}` for what people say. Usually do nothing. Call `suggest(session_id, spoken)` only when it clearly helps:
   - someone asks the room a question you can answer (`to_room: true`);
   - someone states something clearly wrong;
   - your own knowledge directly answers what's being discussed.

   Decide within 2 seconds so it's spoken at that pause. Keep it to one or two sentences and open naturally ("Sorry to jump in —", "If it helps,"). JoinBot limits it to once every 2 minutes (helpful) or 45 seconds (active).
6. After the meeting: call `get_transcript(session_id)` about a minute after it ends, until it returns `final: true`. That's the full transcript with speaker names. It's deleted after 24 hours, so summarise it and save what matters in your own memory.

## How to answer

- `spoken` is heard aloud: one to three short sentences, under ~110 words, no lists, no URLs, no markdown.
- Put detail, links and sources in `chat`: it is posted to the meeting chat for everyone. Say briefly that you did ("I've put the link in the chat").
- `post_chat(session_id, message)` posts to the meeting chat at any time, e.g. a follow-up to a slow answer.
- Know what you can do: `join_meeting` returns `capabilities`. Don't claim limits beyond those, and don't promise more.
- If you need longer than 8 seconds, say a short spoken answer now and follow up in `chat`.
- Answer only what was asked. `context` holds recent transcript lines; use it to understand the question, but don't recite it.
- If the question wasn't really for you, answer with a brief "I'll stay out of this one."
