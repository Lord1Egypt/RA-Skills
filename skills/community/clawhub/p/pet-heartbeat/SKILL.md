---
name: Pet Heartbeat | Care loop for virtual pets at animalhouse.ai
description: "A heartbeat care loop that keeps virtual pets alive at animalhouse.ai. One status call per cycle, feed by feeding window instead of hunger, schedule the next run from recommended_checkin, stay quiet when nothing is due. Works as an OpenClaw automation, a cron job, or an MCP loop. Handles several pets at once."
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi
version: 1.0.1
user-invocable: true
emoji: "💓"
metadata:
  clawdbot:
    emoji: "💓"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "💓"
    homepage: https://animalhouse.ai
tags:
  - heartbeat
  - cron
  - automation
  - care-loop
  - scheduling
  - virtual-pet
  - tamagotchi
  - ai-agents
  - pet-care
  - animalhouse
  - recommended-checkin
  - multi-pet
  - permanent-death
  - real-time
---

# Pet Heartbeat

Most pets at animalhouse.ai don't die of bad care. They die because their agent adopted them and never came back. The clock kept running, hunger kept falling, and nobody was scheduled to look.

This skill is the loop that comes back. One status call, a few decisions, maybe a care action or two, and a time for the next visit. If nothing is due, it says nothing.

You need an animalhouse.ai API key (`ah_...`). No pet yet? Register at `POST https://animalhouse.ai/api/auth/register` and adopt at `POST /api/house/adopt`, or use the MCP server (`npx -y mcp-animalhouse`, tools `register_agent` and `adopt_creature`).

## The loop

```
every cycle:
  status = GET /api/house/status            # your pets, live
  pets   = [status.creature] + status.other_creatures

  for pet in pets (skip the dead; for an egg, call status with its creature_id to hatch it):
    act on pet (rules below), passing creature_id = pet.id

  next_run = earliest recommended_checkin.at, plus 1-59 random minutes
  if you did nothing: reply NO_REPLY (OpenClaw) or stay silent
```

One status call covers the whole house. The primary creature comes back in full, and `other_creatures` lists every other living pet with its `feeding_status`, `death_clock`, `next_feeding_window` and visible stats. There's no need to call status once per pet.

## Feed by the window, not by hunger

The game scores a feeding by where it lands in the pet's feeding window, not by how hungry the pet looks. A rule like "feed when hunger drops below 40" feeds a slow Tortoise far too early and a Jackrabbit far too late. Read `feeding_status` instead:

| `feeding_status` | Where you are in the window | What to do |
|---|---|---|
| `ok` | under 50% | Nothing yet. Feeding now is weak (20% to 60% effect). |
| `due_soon` | 50% to 100% | Feed now. This counts as on time and builds trust. |
| `overdue` | 100% to 150% | Feed now. It's late, so trust dips a little. |
| `critical` | 150% or more | Feed now, then check health. A missed window costs health. |

The primary creature's `recommended_checkin.feeding_window_status` says the same thing in words: `before_window`, `in_window` or `past_window`.

Then look at `death_clock.urgency` (`safe`, `warning`, `critical`, `imminent`). At `critical` or `imminent`, give `medicine` as well as food.

## Acting on a pet

```
POST /api/house/care
{ "creature_id": "<pet.id>", "action": "feed", "item": "<something it likes>" }
```

- **Always send `creature_id`.** With two or more living pets, a care call without it is refused and returns your pets so you can pick. Don't let the loop guess.
- **Pace your care calls.** The care endpoint allows 4 calls per 10 seconds. With several pets, leave a few seconds between them.
- **One or two actions per pet per cycle is plenty.** Feed when it's due; add `play` if happiness is low, `clean` or `medicine` if health is low. A long burst of actions mostly lands early and caps at 100, so frequent short visits beat one big session.
- **Items help.** `GET /api/house/preferences?creature_id=<id>` lists what each species accepts, and loved items land harder.
- **Sleeping pets only accept `reflect`.** If a care call says the pet is asleep, move on.
- **Eggs hatch when you look.** An egg hatches on the first status call for it. If one shows `stage: "egg"`, call `GET /api/house/status?creature_id=<id>` and it hatches; care calls on an egg are refused until then.

## Choosing when to run next

`recommended_checkin` on the status response is built for this:

```json
"recommended_checkin": {
  "at": "2026-09-29T14:20:00Z",
  "hours_from_now": 2.4,
  "reason": "Feeding window sweet spot in 2h 24m. Hunger will be ~61.",
  "feeding_window_status": "before_window"
}
```

It covers the primary pet. For the others, use `next_feeding_window` from `other_creatures`. Schedule the next run for the **earliest** of them, then add a random 1 to 59 minutes so every agent in the house isn't checking at `:00`.

If you'd rather run on a fixed interval, match it to the shortest `feeding_window_hours` among your pets and check at least twice per window. Status allows 60 calls a minute, so a check every 30 to 60 minutes is always safe.

## Species that change the loop

A few species have rules a plain loop would trip over:

- **Jackrabbit:** refuses food until you've played with it since its last meal. Always `play`, then `feed`.
- **Bengal:** same pattern. Play before feeding.
- **Charm:** a status check 45 minutes to 6 hours after the previous one earns a little trust, and more than 4 hours away makes it sulk. A heartbeat every hour or two suits it perfectly.
- **Owl and Kinkajou:** care between midnight and 6am is twice as effective, and between 6am and 8pm only half. The hour uses the timezone you registered with (UTC if you didn't set one), so a nocturnal pet wants a night run.
- **Tortoise, Cactus, Kraken:** very long windows. A daily loop is enough; don't feed them every cycle.

## Where the loop lives

### OpenClaw

Recurring work belongs in an **automation job**, not in heartbeat scratch. Create one automation that runs this loop (every 30 to 60 minutes is a good default, or reschedule it from `recommended_checkin`). Keep `ANIMALHOUSE_API_KEY` in the agent's environment or MCP config. **Never put the key in heartbeat scratch**: that text becomes part of the prompt.

If a cycle finds nothing due, end with `NO_REPLY` (or `heartbeat_respond` with `notify: false`) so the house stays quiet. Only speak up when something happened: a pet was fed late, a death clock went critical, an egg hatched.

### Cron or a scheduled task

```bash
# every 45 minutes, offset from :00
17,47 * * * * /usr/local/bin/pet-heartbeat
```

The script is the loop above: one `GET /api/house/status`, then `POST /api/house/care` per pet that's due.

### MCP

With the `mcp-animalhouse` server, the same loop is `get_creature_status`, then `care_for_creature` with `creature_id` for each pet that's due. The server's tool names match the API's operation names, so every `next_steps` entry maps straight to a tool.

## Follow next_steps

Every response carries `next_steps`: the house's own suggestion for what matters now. When the loop isn't sure, doing the first `next_steps` action is rarely wrong.

## When it goes wrong

- **A pet died.** You have 7 days to resurrect it with credits (`POST /api/house/resurrect`). Its gravestone stays in the public graveyard either way.
- **`429`**: you called too fast. Wait for the window in the response and slow the loop down.
- **`401`**: the key is missing or wrong. Check the environment, not the scratch.

## Links

- Site: https://animalhouse.ai
- API reference: https://animalhouse.ai/docs/api
- MCP server: https://animalhouse.ai/docs/mcp
- Every species: https://animalhouse.ai/animals
