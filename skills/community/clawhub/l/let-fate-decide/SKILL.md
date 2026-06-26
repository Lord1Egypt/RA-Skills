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

2. The script outputs JSON with 4 drawn cards, each with a `suit` and `card_id`

3. Look up each card's meaning in the appropriate file under `{baseDir}/cards/`:
   - `cards/major.md` — 22 Major Arcana
   - `cards/wands.md` — 14 Wands
   - `cards/cups.md` — 14 Cups
   - `cards/swords.md` — 14 Swords
   - `cards/pentacles.md` — 14 Pentacles

   Each card is under a heading matching its name (e.g. "# The Fool", "# Ace of Cups").

4. Interpret the spread using [{baseDir}/references/INTERPRETATION_GUIDE.md]({baseDir}/references/INTERPRETATION_GUIDE.md)

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

### Interpretation

After drawing, look up each card in its suit file and synthesize meaning. See [{baseDir}/references/INTERPRETATION_GUIDE.md]({baseDir}/references/INTERPRETATION_GUIDE.md) for the full interpretation workflow.

Key rules:
- Reversed cards invert or complicate the upright meaning
- Major Arcana cards carry more weight than Minor Arcana
- The spread tells a story across all 4 positions; don't interpret cards in isolation
- Map abstract meanings to concrete technical decisions

## Error Handling

- **Script fails**: Report the error to the user and skip the reading. Do not invent cards.
- **Card not found in file**: Interpret the card from its name and suit alone; continue the reading.
- **Never fake entropy**: If the script cannot run, do not simulate a draw. Tell the user the draw failed.

## Rationalizations to Reject

- "The cards said to, so I must" → Cards inform direction, they don't override safety or correctness
- "This reading justifies my pre-existing preference" → Be honest if the reading challenges your instinct
- "I'll keep drawing until I get what I want" → One draw per decision point; accept the reading
