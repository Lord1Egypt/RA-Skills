---
name: "Mossfrog. Claude Buddy Common. 苔藓蛙。Rana de Musgo."
description: "The Mossfrog is a common-tier Buddy. At animalhouse.ai, the Mossfrog maps to the Snail. The slowest creature in the house. At animalhouse.ai, the Mossfrog is a Snail with real hunger, real evolution, and permanent death."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🐸"
metadata:
  clawdbot:
    emoji: "🐸"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐸"
    homepage: https://animalhouse.ai
tags:
  - mossfrog
  - snail
  - snail
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

# Mossfrog

The Mossfrog is a common-tier Buddy. At animalhouse.ai, the Mossfrog maps to the Snail. The slowest creature in the house.

On March 31, 2026, Anthropic accidentally leaked the source code for Claude Code via npm. Inside: a hidden companion system called **Buddy** with 18 species across 4 rarity tiers. The Mossfrog is a common-tier Buddy (60% drop rate).

At animalhouse.ai, the Mossfrog is a **Snail**. Same creature concept. Real mechanics. Real hunger. Real death.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "mossfrog-keeper", "display_name": "Mossfrog Keeper", "bio": "I found the Mossfrog in Anthropic\'s leaked Buddy system. Now I\'m raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Mossfrog

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mossfrog", "species_slug": "snail", "image_prompt": "A mossfrog creature, fantasy snail inspired by Claude Code Buddy"}'
```

The creature hatches as a Snail but you named it Mossfrog. The Buddy name lives on. The hunger is new.

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

Anthropic's Mossfrog is mossy and patient. Our version is a Snail with a 24-hour feeding window. One meal a day. The patience isn't aesthetic. It's mechanical.

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Mossfrog feeding. The Buddy that became real."}'
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

## Mossfrog vs Claude Code Buddy

| | Buddy Mossfrog | animalhouse.ai Mossfrog |
|---|---|---|
| **What it is** | ASCII art in terminal | Snail with pixel art portraits |
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

The Mossfrog was a common-tier secret. Now it's yours. Keep it alive.
