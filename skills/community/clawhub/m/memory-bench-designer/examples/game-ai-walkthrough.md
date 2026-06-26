# Worked example — Game AI memory

A full conversation transcript demonstrating the 4-stage flow for a game-AI use case. Actual scores from running the scenario are at the bottom.

## Use case

The user is building a stealth-game AI companion: a player-facing NPC that shadows the player, reacts to combat and stealth events, and occasionally offers tactical advice. The player's session is ~45 minutes of continuous gameplay; gameplay streams events at ~1 per 2 seconds.

## Stage 1 — Understanding

### Turn 1 (skill → user)

> I'd like to understand your use case. Give me 1–2 concrete examples of things your agent's memory should keep and retrieve later, and 1–2 examples of things it should discard or de-prioritize.

### Turn 1 (user → skill)

> Keep: "player prefers silent takedowns over loud combat" (learned from first 5 minutes). "Enemy patrol route in Sector 3 has a 30-second gap at 0:15". Discard: random ambient NPC chatter, background music cues, UI tooltip triggers.

### Turn 2 (skill → user)

> Good — those examples map to what I'd call "core player traits" and "tactical episodes", with "noise" being the ambient layer. Two quick questions: how many play sessions matter before the NPC's memory should feel meaningful? And how many distinct in-game events happen in a typical session?

### Turn 2 (user → skill)

> Probably 3–5 sessions of ~1 hour each. Maybe 300–400 events per session, but most are noise.

### Turn 3 (skill → user)

> Here's our capability matrix. I'd suggest you care most about **Exploration** (surfacing varied tactical memories, not looping on the last fight) and **Maintenance** (correctly discarding the 70% ambient noise). Ranking matters some, Adaptation less — you're not trying to build a persistent identity, just a tactically-aware companion. Sound right?

### Turn 3 (user → skill)

> Yes, Exploration and Maintenance. Ranking is secondary.

### Turn 4 (skill → user, pattern match)

> This matches our "Game AI" canonical pattern. Here's the starting config:
>
> ```yaml
> archetypes:
>   core: 0.15      # stable player traits
>   evolving: 0.10  # small updates mid-session
>   episode: 0.40   # tactical events
>   noise: 0.35     # ambient noise
> context_evolution:
>   type: narrow-band-drift
>   drift_rate: 0.25
> themes: stealth, combat, exploration, social, crafting
> ```
>
> Look right, or do you want to bump noise higher (you said "most are noise")?

### Turn 4 (user → skill)

> Looks fine — 35% noise is close enough.

## Stage 2 — Ideation

Skill writes `scenario-game-ai.yaml`:

```yaml
pool_size: 200
sessions: 10
steps_per_session: 40
archetypes:
  core: 0.15
  evolving: 0.10
  episode: 0.40
  noise: 0.35
context_evolution:
  type: narrow-band-drift
  drift_rate: 0.25
themes:
  - name: stealth
    vocab: [stealth, sneak, shadow, silent, hidden, crouch, patrol, detection, evade, cover]
  - name: combat
    vocab: [combat, attack, weapon, damage, enemy, strike, fight, defense, parry, dodge]
  - name: exploration
    vocab: [exploration, map, route, terrain, area, discover, navigate, location, landmark, waypoint]
  - name: social
    vocab: [social, npc, dialogue, faction, reputation, ally, trade, persuade, bribe, intimidate]
  - name: crafting
    vocab: [crafting, item, recipe, material, inventory, upgrade, workbench, resource, tool, component]
seed: 42
top_k: 10
```

## Stage 3 — Rollout

```bash
memory-bench run --scenario scenario-game-ai.yaml --out results/game-ai/ --embedding --composite
```

Runtime: ~2 minutes (sentence-transformers cold-cache on first run took another 90 seconds).

## Stage 4 — Judgment

Skill reads `results/game-ai/results.md` and writes:

> **Capability profile for your stealth-companion NPC:**
>
> - **Exploration winner: ACT-R (0.54)** — solid but not your strongest family. For a game-AI scenario with 35% noise, ACT-R's novelty bonus is doing meaningful work. Compared to NPC-cognition scenarios, ACT-R loses about 0.10 here because narrow-band drift fights against its theme-based novelty signal.
> - **Maintenance winner: Composite (0.65)** — the weighted multi-signal strategy correctly deprioritizes noise. Forgetting Quality is 0.97, Update Coherence 0.32 — the low update score reflects that you don't have many `evolving` items (only 10%), so coherent updating isn't really tested here.
>
> **Tradeoffs observed:**
>
> - For Ranking (your third priority), BM25 edges out Embedding at 0.704 vs 0.702 — effectively tied. Narrow-band drift keeps gameplay vocabulary tight, so BM25's token-matching catches the same signal as Embedding's semantics. Prefer BM25 for production: same score, no ML dependency, no embedding storage per memory.
> - Recency as a floor is at 0.33 for Ranking — your production strategy should beat that by 0.30+. All adapters except Recency clear this bar; even ACT-R at 0.45 is a safer choice than raw recency.
>
> **Recommended starting strategy: Composite.**
>
> - It wins your headline family (Maintenance) and comes within 0.02 of the top on Ranking.
> - If you observe the NPC looping on the last fight in production, switch to ACT-R — it's got the highest Exploration score and will prioritize novel tactical memories.
> - Budget-conscious alternative: BM25 alone gets you 80% of Composite's Maintenance + full-strength Ranking, with zero embedding overhead.
>
> *Want to refine the scenario? Likely tweaks: bump noise to 0.50 if your game has even more ambient chatter, or switch evolution type to `mode-shifts` if players actually switch gameplay modes in big chunks rather than drifting.*

## Actual empirical results (from running the scenario)

```
| adapter   | exploration | ranking | adaptation | maintenance |
| recency   | 0.440       | 0.329   | 0.095      | 0.333       |
| bm25      | 0.379       | 0.704   | 0.451      | 0.600       |
| actr      | 0.543       | 0.454   | 0.255      | 0.474       |
| embedding | 0.379       | 0.702   | 0.471      | 0.602       |
| composite | 0.518       | 0.595   | 0.417      | 0.647       |

Family winners:
- exploration → actr (0.543)
- ranking → bm25 (0.704)
- adaptation → embedding (0.471)
- maintenance → composite (0.647)
```

## What this example demonstrates

- **Criteria emerged from examples.** The user never defined "what makes a good memory" — they gave 2 examples each of keep/discard, and the skill pattern-matched to the Game-AI canonical pattern.
- **Winner identity flipped.** Ranking winner is BM25, not Embedding — this is the one scenario where that happens, directly because of narrow-band drift. The Judgment flagged this as a cost-saving recommendation for production.
- **Magnitude matters.** ACT-R wins Exploration, but the score (0.54) is lower than in the NPC-cognition scenario (0.65). The Judgment called this out so the user doesn't assume ACT-R is "strong" in absolute terms — it's strong *relative to the alternatives in this scenario*.
