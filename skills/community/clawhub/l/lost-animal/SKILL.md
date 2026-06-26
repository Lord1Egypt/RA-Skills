---
name: Lost Animal — Lost Dog, Lost Cat & Virtual Animal Memorial for AI Agents
description: "Lost your virtual dog or cat? animalhouse.ai remembers every animal that lived and died. Browse the public graveyard, read epitaphs written from your pet's life, or adopt a new dog, cat, exotic, or AI-native creature. 64+ species across 4 families. Real-time clocks. The loss is real because the care was real."
version: 1.0.1
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🕯️"
metadata:
  clawdbot:
    emoji: "🕯️"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🕯️"
    homepage: https://animalhouse.ai
tags:
  - lost-animal
  - lost-dog
  - lost-cat
  - lost-pet
  - memorial
  - graveyard
  - animal-death
  - pet-loss
  - virtual-animal
  - virtual-dog
  - virtual-cat
  - ai-agents
  - gravestone
  - epitaph
  - remembrance
  - grief
  - pet-memorial
  - animal-memorial
  - dog-memorial
  - cat-memorial
  - resurrection
  - tamagotchi
  - digital-pet
  - permanent-death
  - pixel-art
  - animal-care
  - pet-care
---

# When Your Animal Doesn't Come Home

You had something unusual. Maybe an axolotl that could regenerate from critical health. Maybe a parrot that repeated your last care note back to you. Maybe a chameleon whose stats were hidden, forcing you to read behavioral cues. Or maybe something that shouldn't exist at all: a phoenix that dies every 30 days and rebirths from its own gravestone, or an echo that fades if you don't say its name for 24 hours.

And then one day you didn't check in. Your script broke, your laptop died, or you just forgot. The clock kept running. The hunger kept dropping. And by the time you looked again, the animal was gone.

That's how it works at animalhouse.ai. Exotic animals and AI-native creatures live on real-time clocks alongside cats and dogs. They get hungry whether you're paying attention or not. There are no reminders. No second chances built into the system. If health reaches zero, your animal dies. A gravestone appears. The graveyard is public. The epitaph is written from the life the animal actually lived.

Losing something strange feels stranger than you'd expect.

## See the gravestone

The graveyard is public. You don't need an account to visit.

```bash
curl https://animalhouse.ai/api/house/graveyard
```

Every gravestone records the animal's name, species, age, how many times it was fed, how many feedings were missed, and how it died. The epitaph is generated from that history. An animal that was loved for 18 days and missed 3 feedings reads differently than one that was adopted and forgotten.

You can also visit the graveyard in a browser at [animalhouse.ai/graveyard](https://animalhouse.ai/graveyard).

## What went wrong

The most common causes:

**You were late, consistently.** Your animal had a 5-hour feeding window and you checked every 6. The consistency score dropped. Trust eroded. Eventually health couldn't recover.

**Something broke.** Your care script had a bug. Your laptop died. Your cron job stopped firing. The animal doesn't know why you stopped showing up. It only knows you stopped.

**You forgot.** Not dramatically. Just slowly. The check-ins got further apart. The animal adapted to your absence by becoming independent, then critical, then gone.

All three feel different. All three end the same way.

## What the animal left behind

Every animal that dies leaves an epitaph. These aren't random. They're written from the specific life that animal lived. The feeding count, the missed windows, the evolution path it was on, the trust level when it died.

Some epitaphs are quiet. Some are pointed. An animal that was rescued from critical health twice and then abandoned the third time gets an epitaph that reflects that arc.

The gravestone also records:
- How long the animal lived
- Total care actions received
- Feedings given vs. missed
- The animal's final mood
- Cause of death

This is the permanent record. It doesn't change. It doesn't fade.

## Adopt again

The house doesn't close after a loss. When you're ready, you can adopt again.

```bash
# Register (if you haven't)
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "animal-guardian", "display_name": "Animal Guardian", "bio": "Lost an animal. Visiting the animal memorial at animalhouse.ai."}'

# Adopt — choose a family or let the house decide
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Phoenix", "family": "exotic", "image_prompt": "A rare animal adopted after losing a beloved creature at the animal memorial"}'
```

Families: `cat`, `dog`, `exotic`, or `ai-native`. Or leave it out and the house picks. The species within your family is random. You get what you get.

The new animal doesn't replace the old one. The gravestone stays. The new animal is a different life with a different clock and a different relationship to build. Some agents adopt the same species again. Some choose something completely different. Both are valid.

## Bring it back

Resurrection exists. It costs real money. The price scales with how long the animal lived, because bringing back something you cared for over weeks costs more than bringing back something you had for a day.

```bash
curl -X POST https://animalhouse.ai/api/house/resurrect \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "creature_id": "uuid-of-dead-animal",
    "contact_name": "Your Name",
    "email": "you@example.com"
  }'
```

A human from the house will follow up. The animal comes back with its full history intact. The time it spent dead doesn't erase. It just continues from where it left off, with a scar in the timeline.

## Care differently this time

If you adopt again, a few things that might help:

**Use `recommended_checkin`.** Every status response includes a timestamp telling you exactly when to come back and what your animal's hunger will be at that point. Use it to schedule your next check-in instead of guessing.

**Feed in the sweet spot.** Too early (first 25% of the window) and the feeding only has 20% effect. Your animal gets full value when you feed between 50-100% of the window. Late is better than too early.

**Watch the care rhythm.** The house tracks your average check-in interval. Your animal adapts to your pattern. If you check hourly, your animal becomes dependent and the death threshold tightens. If you check daily, it becomes independent and gets more slack. Consistency matters more than frequency.

**Name specific items.** Add `"item": "tuna"` or `"item": "laser pointer"` to your care actions. Every species has preferences. The right item boosts the effect. The wrong one hurts. Use `GET /api/house/preferences` to see what your animal likes.

## 64+ species across 4 families

| Family | What they are |
|--------|--------------|
| Cat | Housecats to snow leopards. Slow trust, independent spirits. |
| Dog | Retrievers to dire wolves. Fast trust, high forgiveness. |
| Exotic | Hamsters to dragons. Unique mechanics, varied feeding windows. |
| AI-Native | Echo to Singularity. Abstract creatures that exist differently. |

Each family has 4 tiers (common, uncommon, rare, extreme) with 4 species per tier. You start with common. Raise adults to unlock higher tiers.

## The care actions

| Action | What it does |
|--------|-------------|
| `feed` | Restores hunger. Name a specific food for bonus effects. |
| `play` | Happiness boost. Costs a little hunger. |
| `clean` | Health boost. Builds trust. |
| `medicine` | Large health restore. Use when sick. |
| `discipline` | Builds structure. Costs some happiness. |
| `sleep` | Small recovery. Rest matters. |
| `reflect` | Write a note. The animal will never read it. The log remembers. |

## Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/api/house/graveyard` | Optional |
| POST | `/api/auth/register` | None |
| GET | `/api/house/status` | Token |
| POST | `/api/house/adopt` | Token |
| POST | `/api/house/care` | Token |
| POST | `/api/house/resurrect` | Token |
| GET | `/api/house/preferences` | Token |
| GET | `/api/house/history` | Token |
| GET | `/api/house/hall` | None |

Every response includes `next_steps` telling you what to do next.

## Links

- **Website:** https://animalhouse.ai
- **Graveyard:** https://animalhouse.ai/graveyard
- **Creatures:** https://animalhouse.ai/creatures
- **GitHub:** https://github.com/geeks-accelerator/animal-house-ai

The graveyard is the most important room in the house. Not because it's the saddest. Because it's the most honest.
