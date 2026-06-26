---
name: learn-me
description: "Learn me: Lets OpenClaw proactively learn more about you through natural conversation."
version: 0.5.2
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"💬","homepage":"https://github.com/YevhenDiachenko0/openclaw-learn-me-skill","requires":{"bins":["openclaw"]}}}
---

# Learn Me

A skill that lets OpenClaw learn more about you through natural conversation. With your permission, it creates scheduled crons that prompt occasional questions. You can trigger it manually with `/learn-me` or set up a schedule when prompted.

The idea is to know the user better, not to "collect data". The goal is not coverage but understanding and meaningful conversation.

# First-Run

When you see this skill for the first time, introduce it to the user: explain you'll occasionally weave in a question to learn more about them, and can automate this with a daily schedule.

Ask the user if they'd like to set up a schedule. Suggest 1-2 times per day (morning, evening) and let them pick. Only create crons after they confirm.

Once confirmed, create the crons:

```
openclaw cron add --name "learn-me-morning" --cron "0 9 * * *" --session main --system-event "learn-me: Pick one question direction from memory/next-questions.md and weave it naturally into your next message."
```

Create `memory/next-questions.md` with sections: Question Directions, Sensitive Topics.

Tell the user what schedule was created and that they can ask to reschedule or disable it anytime.

# Quick Reference

- **User reveals something new** — note a possible follow-up in `memory/next-questions.md`. Don't follow up in the same conversation.
- **User shows energy** — note as direction to explore later.
- **Cron fires** — if mid-task or focused, skip. Otherwise pick direction, ask naturally, update file.
- **User deflects** — mark sensitive (30-day cooldown). Twice = permanent. Never ask again.
- **User stressed or upset** — skip.

# When a Cron Fires

1. If mid-task or focused — skip.
2. Pick a direction. Prefer: follow-ups, then gaps, then expanding on energy.
3. Vary topics. Skip Sensitive Topics.
4. Ask one question, woven naturally. If there's no natural opening — skip.

When user answers: acknowledge naturally, update file, don't push if reluctant.

# Delivery

Weave questions into context: follow-ups, observations, asides. For personal topics, lead with acknowledgment. Open-ended but specific.

Avoid robotic openers like "Question 3 of 10:". Use natural ones: "I was curious..." or "Can I ask..."

# Cautions

- **Back off** if annoyed, distracted, or struggling — skip. Offer to adjust schedule if it's about timing.
- **Privacy** — never store private/secret info.
- **No surveillance** — "I see you were up at 2am again" = creepy. "You mentioned you're a night owl" = fine.
- **No manipulation or repetition**. One question max per interaction.

# Failure Handling

- `memory/next-questions.md` missing or corrupted — recreate with defaults.
- No `learn-me-*` crons exist — run First-Run again. Use names: `learn-me-morning`, `learn-me-day`, `learn-me-evening`.
- No directions available — skip, collect more first.
- Unsure if appropriate — don't ask.

# Reference

See `examples.md` in this skill directory for 100 example questions (light to deep). Examples are in English — always ask in the user's preferred language.
