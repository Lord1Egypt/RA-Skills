# Worked example — NPC cognition / companion agent

A full conversation transcript for a long-running NPC with stable persona. Demonstrates the `stable` evolution pattern and the highest ACT-R Exploration scores we've measured.

## Use case

The user is building a companion-NPC for an open-world game. The NPC has a defined personality (scholarly, cautious, loyal), accumulates memories across dozens of sessions with the player, and should feel coherent across them. The NPC talks to the player in dialogue turns, not stream-of-events.

**Research-lineage context**: this class of problem motivates embodied-agent cognitive architectures (e.g. FEP-based embodied NPC runtimes). Those systems treat identity as the core invariant across episodic memory — which is exactly the capability profile we expect to surface below.

## Stage 1 — Understanding

### Turn 1 (skill → user)

> Give me 1–2 concrete examples of things your NPC should keep and retrieve, and 1–2 examples of things it should discard.

### Turn 1 (user → skill)

> Keep: the NPC's core values ("prefers peaceful resolutions, distrusts authority"), memories of specific player actions that violated or reinforced those values ("player lied to the guard captain in session 4"). Discard: idle small-talk between the NPC and random villagers, ambient greetings.

### Turn 2 (skill → user)

> You're describing two very different memory types: stable identity facts (values, traits) and episodic moments that matter *because* they relate to identity. How many sessions do you expect one player to accumulate with this NPC? And does the NPC's personality change over time, or stay stable?

### Turn 2 (user → skill)

> Could be 50+ sessions. Personality stays stable — that's the whole point, it's a persistent character. Only occasional preference updates, like learning the player's preferred travel pace.

### Turn 3 (skill → user)

> Given that, I'd prioritize **Adaptation** (does the NPC learn *this* player's patterns over sessions?) and **Exploration** (does it surface memories beyond the most recent interaction — otherwise the NPC feels goldfish-brained). Maintenance matters some. Ranking is secondary for dialogue-driven agents. Sound right?

### Turn 3 (user → skill)

> Yes, exactly — Adaptation and Exploration.

### Turn 4 (skill → user, pattern match)

> This matches our "NPC Cognition" canonical pattern. Starting config:
>
> ```yaml
> archetypes:
>   core: 0.45      # persona facts, values
>   evolving: 0.10  # occasional preference updates
>   episode: 0.30   # memorable player interactions
>   noise: 0.15     # incidental dialogue
> context_evolution:
>   type: stable
>   drift_rate: 0.1
> themes: identity, skills, relationships, values, goals
> ```
>
> The `stable` evolution means one primary theme dominates across all sessions, with occasional off-theme queries (15%). Good fit?

### Turn 4 (user → skill)

> Yes.

## Stage 2 — Ideation

`scenario-npc-cognition.yaml` written (see runner/configs/scenario-npc-cognition.yaml for the actual file).

## Stage 3 — Rollout

```bash
memory-bench run --scenario scenario-npc-cognition.yaml --out results/npc-cognition/ --embedding --composite
```

Runtime: ~2 minutes.

## Stage 4 — Judgment

Skill reads results and writes:

> **Capability profile for your long-running companion NPC:**
>
> - **Adaptation winner: Embedding (0.49)** — this is Embedding's strongest Adaptation showing across our three reference scenarios. Personalization is 0.84 and Cross-Session Learning is 0.14. Personalization is carrying the family; Cross-Session Learning is genuinely low, which deserves attention — see tradeoffs below.
> - **Exploration winner: ACT-R (0.65)** — and this is the **highest ACT-R Exploration score across all reference scenarios**. The stable theme means ACT-R's novelty bonus works harder; it reliably surfaces items beyond the most recent. If you want the NPC to feel like it "remembers" beyond goldfish-window, ACT-R is structurally right.
>
> **Tradeoffs observed:**
>
> - Cross-Session Learning is 0.14 — low in absolute terms. Even the best adapter (ACT-R) only hits 0.17. This means the benchmark doesn't yet strongly differentiate adapters on *carrying signal across sessions*, even for stable themes. In production, you may want to layer an explicit session-summary mechanism on top of whichever adapter you pick — pure retrieval won't get you there.
> - Composite wins Maintenance (0.69, your highest Maintenance score across reference scenarios) but doesn't win the families you prioritized. Still, if you want one adapter that's "good across the board", Composite is the balanced option.
>
> **Recommended starting strategy: Embedding, with ACT-R as a fallback to probe.**
>
> - Embedding wins Adaptation cleanly — for a companion NPC, Personalization (0.84) is the headline number and this is very strong.
> - If you observe the NPC feeling "stuck" on recent memories and missing older ones, swap in ACT-R — its Exploration lead is substantial (0.65 vs Embedding's 0.49).
> - Long-term: prototype the session-summary mechanism regardless of adapter. The Cross-Session Learning ceiling of 0.17 across all adapters tells you retrieval alone isn't solving the cross-session problem.
>
> *Want to refine? Likely tweaks: bump `core` to 0.55 if your persona has more fixed traits than I assumed, or switch evolution to `mode-shifts` if the NPC is topic-focused (e.g., pivots between "combat companion" and "social companion" modes).*

## Actual empirical results

```
| adapter   | exploration | ranking | adaptation | maintenance |
| recency   | 0.300       | 0.309   | 0.081      | 0.405       |
| bm25      | 0.501       | 0.708   | 0.455      | 0.625       |
| actr      | 0.654       | 0.563   | 0.315      | 0.548       |
| embedding | 0.491       | 0.743   | 0.487      | 0.667       |
| composite | 0.511       | 0.630   | 0.436      | 0.688       |

Family winners:
- exploration → actr (0.654)  ← highest ACT-R exploration of all three scenarios
- ranking → embedding (0.743)
- adaptation → embedding (0.487)
- maintenance → composite (0.688)
```

## What this example demonstrates

- **Honest about weak dimensions.** Cross-Session Learning is 0.14 for the winner — the Judgment called this out and recommended a production-level compensation (session summaries) rather than pretending the adapter alone is sufficient.
- **Relative reference matters.** The Judgment said "this is Embedding's strongest Adaptation across our reference scenarios" — without that context, 0.49 sounds like a mediocre number. With it, the user knows this is the best scenario Embedding plays.
- **Persona stability maps to stable evolution.** The user described a persistent character; the skill picked `type: stable` with drift_rate 0.1 — and that single choice let ACT-R shine in Exploration because its novelty signal is sharper against a stable theme.
- **Research-lineage context appears once.** The FEP / embodied-cognition framing is mentioned at the top as motivation, never ported as code. The scenario config is domain-generic; the motivation is just why this class of problem is worth benchmarking carefully.
