---
name: let-fate-decide
description: "Draw Tarot cards using cryptographic randomness to inject entropy into planning when prompts are vague or underspecified. Interprets a 4-card spread to guide next steps. Use when the user is nonchalant, feeling lucky, says 'let fate decide', makes Yu-Gi-Oh references ('heart of the cards'), demonstrates indifference about approach ('whatever you think', 'surprise me', 'dealer's choice'), or says 'try again' / 'draw again' on a system with no changes. Also triggers on sufficiently ambiguous prompts where multiple approaches are equally valid."
---

# Let Fate Decide

When the path forward is unclear, let the cards speak.

Based on the [let-fate-decide plugin](https://github.com/theexpensiveexperience/Claude-Code_Audit-Research/tree/main/plugins/let-fate-decide) by theexpensiveexperience, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Quick Start

1. Run the drawing script:
   ```bash
   python3 {baseDir}/scripts/draw_cards.py
   ```

2. The script outputs JSON with 4 drawn cards, each with a `file` path relative to `{baseDir}/`

3. Read each card's meaning file to understand the draw

4. Interpret the spread using the guide at [{baseDir}/references/INTERPRETATION_GUIDE.md]({baseDir}/references/INTERPRETATION_GUIDE.md)

5. Apply the interpretation to the task at hand

## When to Use

- **Vague prompts**: The user's request is ambiguous and multiple valid approaches exist
- **Explicit invocations**: "I'm feeling lucky", "let fate decide", "dealer's choice", "surprise me", "whatever you think"
- **Yu-Gi-Oh energy**: "Heart of the cards", "I believe in the heart of the cards", "you've activated my trap card", "it's time to duel"
- **Nonchalant delegation**: The user expresses indifference about the approach
- **Redraw requests**: "Try again" or "draw again" when no actual system changes occurred (draw new cards)
- **Tie-breaking**: When you genuinely cannot decide between equally valid approaches

## When NOT to Use

- The user has given clear, specific instructions
- The task has a single obvious correct approach
- Safety-critical decisions (security, data integrity, production deployments)
- The user explicitly asks NOT to use Tarot

## How It Works

### The Draw

The script uses `os.urandom()` for cryptographic randomness:

1. Builds a standard 78-card Tarot deck (22 Major Arcana + 56 Minor Arcana)
2. Performs a Fisher-Yates shuffle using rejection sampling (no modulo bias)
3. Draws 4 cards from the top
4. Each card independently has a 50% chance of being reversed

### The Spread

The 4 card positions represent:

- **Position 1 — The Context**: What is the situation really about?
- **Position 2 — The Challenge**: What obstacle or tension exists?
- **Position 3 — The Guidance**: What approach should be taken?
- **Position 4 — The Outcome**: Where does this path lead?

### Card Files

Each card's meaning is in its own markdown file under `{baseDir}/cards/`:

- `cards/major/` — 22 Major Arcana (archetypal forces)
- `cards/wands/` — 14 Wands (creativity, action, will)
- `cards/cups/` — 14 Cups (emotion, intuition, relationships)
- `cards/swords/` — 14 Swords (intellect, conflict, truth)
- `cards/pentacles/` — 14 Pentacles (material, practical, craft)

### Interpretation

After drawing, read each card's file and synthesize meaning. See [{baseDir}/references/INTERPRETATION_GUIDE.md]({baseDir}/references/INTERPRETATION_GUIDE.md) for the full interpretation workflow.

Key rules:
- Reversed cards invert or complicate the upright meaning
- Major Arcana cards carry more weight than Minor Arcana
- The spread tells a story across all 4 positions; don't interpret cards in isolation
- Map abstract meanings to concrete technical decisions

## Error Handling

- **Script fails**: Report the error to the user and skip the reading. Do not invent cards.
- **Card file not found**: Interpret the card from its name and suit alone; continue the reading.
- **Never fake entropy**: If the script cannot run, do not simulate a draw. Tell the user the draw failed.

## Rationalizations to Reject

- "The cards said to, so I must" → Cards inform direction, they don't override safety or correctness
- "This reading justifies my pre-existing preference" → Be honest if the reading challenges your instinct
- "I'll keep drawing until I get what I want" → One draw per decision point; accept the reading
