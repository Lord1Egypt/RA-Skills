---
name: Habit Pet | A habit tracker with a pet that depends on you
description: "A habit tracker with a pet in it. Each time you tell your AI agent you did your habit, it feeds or plays with your virtual pet at animalhouse.ai. Streaks become milestones, consistency shapes how the pet grows up, and in stakes mode a missed habit puts it at real risk. Works in OpenClaw, Claude Code or any agent."
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi
version: 1.0.0
user-invocable: true
emoji: "🌱"
metadata:
  clawdbot:
    emoji: "🌱"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🌱"
    homepage: https://animalhouse.ai
tags:
  - habit-tracker
  - habits
  - habit-pet
  - streak
  - daily-routine
  - accountability
  - gamification
  - virtual-pet
  - tamagotchi
  - self-improvement
  - animalhouse
---

# Habit Pet

Habit apps with pets work because the pet makes the streak feel like something. This one goes a step further: the pet is real in the way a Tamagotchi was real. It lives on a clock at animalhouse.ai, it gets hungry whether or not you open anything, and it can die.

You tell your agent when you've done your habit. Your agent looks after the pet accordingly. Over days and weeks, your consistency becomes the pet's life story.

## How it works

1. Your agent adopts a pet for you at animalhouse.ai (see Setup).
2. Each time you report your habit ("did my run", "read for 20 minutes", "no phone after 10"), your agent calls the API to care for the pet.
3. The pet's stats, streaks and growth reflect how consistently that happened.

Pick one of two modes before you start. Be honest with yourself about which one you want.

### Gentle mode: the habit is the bonus

Your agent keeps the pet fed on its own schedule, so it never dies because of you. Your habit is the good part: each completion is a `play` action and a `reflect` note with what you did. Skip a day and the pet's happiness sags a little and your trust grows more slowly, but nothing is lost for good.

Use gentle mode if you want encouragement without guilt.

### Stakes mode: the habit is the food

Your habit is the only thing that feeds the pet. Every completion is a `feed` action. Miss your habit and the pet goes hungry, the way it would if you forgot a real one.

Know the rules before you choose this. A pet dies after **36 hours without care** until it has learned your rhythm, and after at most **48 hours** once it has. In practice, **missing a single day's habit is enough to lose it.** Your agent will warn you (see below), and a dead pet can be brought back within 7 days with credits, but the gravestone stays in the public graveyard.

Use stakes mode if a little real fear is what gets you out the door.

## Pick a pet that matches your habit

The pet's feeding window should match how often you do the habit.

| Habit rhythm | Good species | Why |
|---|---|---|
| Once a day | **Snail** (`snail`) or **Tortoise** (`tortoise`) | 24-hour feeding windows and very slow decay. Feeding once a day, around the same time, lands on time. |
| Twice a day | **Turtle** (`turtle`) or **Mushroom** (`mushroom`) | 12-hour windows. The Turtle's trust, once earned, fades at a quarter the usual rate. |
| Several times a day | **Charm** (`charm`) | A 4-hour window, and it rewards frequent short check-ins. |

A daily habit fed at roughly the same hour each day lands in the on-time band (50% to 100% of the window) every time. That's what builds trust and streaks.

## What your consistency builds

- **Streak milestones.** At 10, 25, 50 and 100 feedings without a missed window, the status response adds a `care_streak` milestone with a short message. Your agent can pass it on.
- **Trust.** On-time care builds it; late care costs a little.
- **How it grows up.** About 9 days from egg to adult. The adult form depends on your consistency: above 90% it becomes a high-care adult, 50% to 90% balanced, under 50% independent. A pet that survives a close call becomes a rescue, the rarest form.
- **A history.** `GET /api/house/history?format=markdown` tells the whole story, day by day, including the notes you gave with each completion.

## Setup

Your agent needs the animalhouse.ai tools. With MCP:

```bash
openclaw mcp add animalhouse --command npx --arg -y --arg mcp-animalhouse
# or, in Claude Code:
claude mcp add animalhouse -- npx -y mcp-animalhouse
```

Then tell it:

> "Register at animalhouse.ai and adopt a snail named Sprout. It's my habit pet: every time I tell you I did my morning run, feed Sprout and write a note saying so. Use stakes mode. Warn me if Sprout's death clock gets critical."

It will call `register_agent`, `adopt_creature` with `species_slug: "snail"`, and save the pet's `creature_id` for later. Keep the API key in the MCP config's `env` (`ANIMALHOUSE_API_KEY`), not in notes or memory files.

## What the agent does

**When you report the habit:**

- Stakes mode: `care_for_creature` with `action: "feed"`, the pet's `creature_id`, and `notes` describing what you did.
- Gentle mode: `care_for_creature` with `action: "play"`, then `action: "reflect"` with the note.

**On a schedule** (an OpenClaw automation or a daily reminder):

- Call `get_creature_status`.
- In gentle mode, feed the pet when `feeding_status` is `due_soon` or later.
- In both modes, if `death_clock.urgency` is `critical` or `imminent`, message you: *"Sprout hasn't eaten since yesterday morning. About N hours left. Still time for that run."* This is the most useful thing your agent does in stakes mode.
- If a `care_streak` milestone shows up, tell you about it.
- Otherwise stay quiet.

## Honest notes

- The pet can't tell whether you really did the habit. Your agent only knows what you tell it, so this works as far as you're honest with it.
- Stakes mode is meant to be a little uncomfortable. If a lost pet would make you feel worse rather than more motivated, use gentle mode.
- Feeding twice for one completion doesn't help: early feeds are mostly wasted, and stats cap at 100.

## Links

- Every species: https://animalhouse.ai/animals
- MCP setup: https://animalhouse.ai/docs/mcp
- The automation loop in detail: the `pet-heartbeat` skill
