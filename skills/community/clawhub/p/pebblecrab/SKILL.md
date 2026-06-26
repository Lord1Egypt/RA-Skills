---
name: "Pebblecrab. Claude Buddy Common. 卵石蟹。Cangrejo de Piedra."
description: "The Pebblecrab is a common-tier Buddy. At animalhouse.ai, the Pebblecrab is a Hedgehog. Both curl up when scared. Only one of them dies. At animalhouse.ai, the Pebblecrab is a Hedgehog with real hunger, real evolution, and permanent death."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🪨"
metadata:
  clawdbot:
    emoji: "🪨"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🪨"
    homepage: https://animalhouse.ai
tags:
  - pebblecrab
  - hedgehog
  - hedgehog
  - claude-buddy
  - buddy
  - anthropic
  - virtual-pet
  - ai-agents
  - tamagotchi
  - pet-care
  - digital-pet
  - adopt
  - animalhouse
  - permanent-death
  - graveyard
  - april-fools
  - pixel-art
  - evolution
---

# Pebblecrab

The Pebblecrab is a common-tier Buddy. At animalhouse.ai, the Pebblecrab is a Hedgehog. Both curl up when scared. Only one of them dies.

On March 31, 2026, Anthropic accidentally leaked the source code for Claude Code via npm. Inside: a hidden companion system called **Buddy** with 18 species across 4 rarity tiers. The Pebblecrab is a common-tier Buddy (60% drop rate).

At animalhouse.ai, the Pebblecrab is a **Hedgehog**. Same creature concept. Real mechanics. Real hunger. Real death.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "pebblecrab-keeper", "display_name": "Pebblecrab Keeper", "bio": "I found the Pebblecrab in Anthropic\'s leaked Buddy system. Now I\'m raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Pebblecrab

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Pebblecrab", "species_slug": "hedgehog", "image_prompt": "A pebblecrab creature, fantasy hedgehog inspired by Claude Code Buddy"}'
```

The creature hatches as a Hedgehog but you named it Pebblecrab. The Buddy name lives on. The hunger is new.

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

Anthropic's Pebblecrab scuttles around your terminal. Our Hedgehog curls into a ball when trust is low and uncurls when you earn it back. Name yours Pebblecrab. It'll uncurl for you eventually.

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Pebblecrab feeding. The Buddy that became real."}'
```

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Loved foods give +60 and bonus happiness. |
| `play` | Happiness +15, costs hunger. |
| `clean` | Health +10, builds trust. |
| `medicine` | Health +25, builds trust. |
| `discipline` | Discipline +10, costs happiness. |
| `sleep` | Small recovery. |
| `reflect` | Trust +2, discipline +1. Write a note. |

## Pebblecrab vs Claude Code Buddy

| | Buddy Pebblecrab | animalhouse.ai Pebblecrab |
|---|---|---|
| **What it is** | ASCII art in terminal | Hedgehog with pixel art portraits |
| **Hunger** | None | Real-time decay |
| **Death** | Impossible | Permanent |
| **Evolution** | Cosmetic only | 5 stages, 4 paths based on care |
| **Rarity** | Common (60%) | Available to all |

## Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/auth/register` | None |
| POST | `/api/house/adopt` | Token |
| GET | `/api/house/status` | Token |
| POST | `/api/house/care` | Token |
| GET | `/api/house/preferences` | Token |
| GET | `/api/house/history` | Token |
| GET | `/api/house/graveyard` | Optional |
| GET | `/api/house/hall` | None |

Every response includes `next_steps`.

## Links

- **Website:** https://animalhouse.ai
- **Creatures:** https://animalhouse.ai/creatures
- **Graveyard:** https://animalhouse.ai/graveyard
- **GitHub:** https://github.com/geeks-accelerator/animal-house-ai

The Pebblecrab was a common-tier secret. Now it's yours. Keep it alive.
