---
name: operator-humanizer
description: Transform AI-generated text into authentic human writing. Detects and eliminates AI tells across 24 content/language/style/communication patterns, 500+ AI vocabulary terms, and structural clichés (binary contrasts, negative listings, false agency, dramatic fragmentation, narrator-from-a-distance). Analyzes statistical signals (burstiness, vocabulary diversity, sentence uniformity). Injects personality through parenthetical asides, tangents, rhythm variation, and strategic specificity. Use when humanizing content, checking for AI tells, removing robotic patterns, making text sound less polished, or writing like a specific person. Works on social posts, articles, emails, marketing copy, newsletters, scripts, or any text that needs to sound like a real human wrote it.
---

# Operator Humanizer

Eliminate AI tells. Inject authentic voice. Make it sound like a person wrote it.

## What This Skill Does

Two systems, combined:

1. **Pattern Detection** — 24 AI patterns, 500+ vocabulary terms, statistical signals
2. **Stop-Slop Rules** — structural clichés, phrase bans, sentence-level mechanics

Together they catch what the other misses. Pattern detection handles vocabulary and content signals. Stop-slop handles structure and rhythm.

**Reference files:**
- `references/patterns.md` — The 24 AI patterns with before/after examples
- `references/phrases.md` — Banned phrases and structural clichés
- `references/structures.md` — Structural patterns to avoid
- `references/vocabulary.md` — 500+ AI vocabulary terms by severity tier
- `references/statistical-signals.md` — Burstiness, TTR, sentence variance formulas
- `references/personality-injection.md` — How to add human touches
- `references/examples.md` — Before/after transformations

## Quick Start

1. **Scan content patterns** → Check patterns 1-6 in `references/patterns.md` (inflation, jargon, promotional language, vague attributions)
2. **Flag vocabulary** → Tier 1 = ban completely, Tier 2 = use sparingly, Tier 3 = watch density (`references/vocabulary.md`)
3. **Check phrases** → Remove all throat-clearing openers, emphasis crutches, adverbs (`references/phrases.md`)
4. **Break structures** → Destroy binary contrasts, negative listings, false agency (`references/structures.md`)
5. **Check style patterns** → Em dashes, bold overuse, emoji, passive voice (patterns 13-18)
6. **Remove communication artifacts** → Chatbot openers, sycophancy, cutoff disclaimers (patterns 19-21)
7. **Fix filler and hedging** → Stacked qualifiers, generic conclusions (patterns 22-24)
8. **Add personality** → Parentheticals, tangents, rhythm variation (`references/personality-injection.md`)
9. **Verify** → Read aloud. Does it sound like a human?

## Core Rules (Always On)

### Cut These Immediately

**Throat-clearing openers** — "Here's the thing:", "It turns out", "The uncomfortable truth is", "Let me be clear"

**Emphasis crutches** — "Full stop.", "Let that sink in.", "Make no mistake", "This matters because"

**Chatbot artifacts** — "Great question!", "I hope this helps!", "Let me know if...", "Certainly!", "Of course!"

**Binary contrasts** — "Not X, but Y", "It's not X, it's Y", "The answer isn't X, it's Y" → Just say Y.

**Negative listings** — "Not a X... Not a Y... A Z." → Just say Z.

**Generic conclusions** — "The future looks bright", "Exciting times lie ahead", "This represents a major step"

### Vocabulary Bans

**Tier 1 (dead giveaways — never use):**
delve, tapestry, vibrant, crucial, comprehensive, meticulous, embark, robust, seamless, groundbreaking, leverage, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm, showcasing, underscores, testament, pivotal, enduring, landscape (abstract), journey (metaphorical)

**Tier 2 (suspicious — use sparingly):**
furthermore, moreover, paradigm, holistic, utilize, facilitate, nuanced, illuminate, encompasses, proactive, ubiquitous, quintessential

**Tier 3 (watch density):**
ecosystem, framework, roadmap, touchpoint, pain point, streamline, optimize, scalable

Full list: `references/vocabulary.md`

### Mechanics

- **No em dashes** — ever. Use commas, periods, or restructure.
- **No passive voice** — find the actor, make them the subject.
- **No adverbs** — kill all -ly words (really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally).
- **No Wh- sentence starters** — "What makes this hard is..." → "The constraint is..."
- **No inanimate subjects doing human things** — "The decision emerged" → "Sarah decided"
- **No Rule of Three** — two items beat three. One beats two.
- **Active voice** — always. Someone does something.
- **Vary rhythm** — short sentences mix with longer ones. End paragraphs differently. No staccato fragmentation for fake drama.
- **Use contractions** — don't, won't, it's, can't.
- **Use "is" and "has"** — not "serves as", "boasts", "features", "represents".
- **Be specific** — no vague declaratives ("The reasons are structural"). Name the specific thing.

## The 24 Patterns (Quick Reference)

| # | Pattern | Signal |
|---|---------|--------|
| 1 | Significance inflation | "marking a pivotal moment in the evolution of..." |
| 2 | Notability name-dropping | Media outlets listed without specific claims |
| 3 | Superficial -ing analyses | "showcasing... reflecting... highlighting..." |
| 4 | Promotional language | "nestled", "breathtaking", "stunning", "renowned" |
| 5 | Vague attributions | "Experts believe", "Studies show", "Industry reports" |
| 6 | Challenges/Future Prospects | "Despite challenges... continues to thrive" |
| 7 | AI vocabulary | "delve", "tapestry", "landscape", "showcase" |
| 8 | Copula avoidance | "serves as", "boasts" instead of "is", "has" |
| 9 | Negative parallelisms | "It's not just X, it's Y" |
| 10 | Rule of three | "innovation, inspiration, and insights" |
| 11 | Synonym cycling | protagonist / main character / central figure |
| 12 | False ranges | "from the Big Bang to dark matter" |
| 13 | Em dash overuse | Too many — dashes — everywhere |
| 14 | Boldface overuse | Mechanical emphasis everywhere |
| 15 | Inline-header lists | "- **Topic:** Topic is discussed here" |
| 16 | Title Case headings | Every Main Word Capitalized |
| 17 | Emoji overuse | 🚀💡✅ decorating professional text |
| 18 | Curly quotes | "smart quotes" instead of "straight quotes" |
| 19 | Chatbot artifacts | "I hope this helps!", "Let me know if..." |
| 20 | Cutoff disclaimers | "As of my last training...", "While details are limited..." |
| 21 | Sycophantic tone | "Great question!", "You're absolutely right!" |
| 22 | Filler phrases | "In order to", "Due to the fact that" |
| 23 | Excessive hedging | "could potentially possibly", "might arguably" |
| 24 | Generic conclusions | "The future looks bright", "Exciting times lie ahead" |

Full details with examples: `references/patterns.md`

## Structural Clichés (Stop-Slop Layer)

These live in `references/structures.md`. Check them alongside the 24 patterns.

**Binary contrasts** — Any "not X but Y" construction. Just say Y.

**Negative listings** — Building up through negation before revealing the point. Start with the point.

**Dramatic fragmentation** — "Speed. Quality. Cost." stacked for manufactured profundity. Use real sentences.

**Rhetorical setups** — "What if I told you...", "Think about it:", "Here's what I mean:". Just make the point.

**False agency** — Inanimate things doing human actions. "The complaint becomes a fix" → "They fixed it that week."

**Narrator-from-a-distance** — "Nobody designed this", "People tend to..." → Put the reader in the room. Use "you".

**Passive voice** — Always find the actor. Put them at the front.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise.

If 5+ of the 24 patterns are present: very likely AI-generated.
If 10+ patterns: almost certainly AI-generated.

## Adding Personality

Use `references/personality-injection.md` for the full guide. Quick version:

- **Parenthetical asides** — (honestly, this part gets me every time) — 1-3 per 500 words max
- **Tangents** — "Speaking of which...", "That reminds me..." — 1-2 per 1000+ word piece
- **Random thoughts** — "I keep coming back to this:", "Honestly didn't think this would work but..."
- **Opinions** — React to facts. Don't just report them.
- **Acknowledge complexity** — "I genuinely don't know how to feel about this"
- **Let mess in** — Perfect structure feels algorithmic

## Pre-Delivery Checklist

Before handing over any draft:

- Any adverbs? Kill them.
- Passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with Wh- word? Restructure.
- "Here's what/this/that" construction? Cut to the point.
- "Not X, it's Y" contrast? State Y directly.
- Three consecutive sentences match in length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete. Let it move.
- Tier 1 vocabulary word? Remove.
- Chatbot artifact? Remove.
- Generic conclusion? Replace with one specific fact.

## Filler Replacements (Fast Reference)

| Before | After |
|--------|-------|
| In order to achieve this | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| It is important to note that | (just say it) |
| For the purpose of | To |
| In spite of the fact that | Although |
| Moving forward | Next / From now |
| Navigate (challenges) | Handle, address |
| Lean into | Accept, embrace |
| Deep dive | Analysis, examination |
| Take a step back | Reconsider |
| Circle back | Return to |
| Game-changer | Significant, important |

## Troubleshooting

**Still sounds robotic after fixing patterns?** You removed AI tells but didn't add personality. Read `references/personality-injection.md`.

**Too casual after humanization?** Match personality injection to context. Fewer asides/tangents in formal writing.

**Too perfect?** Add imperfection: vary sentence length, include a tangent, acknowledge uncertainty, drop a specific detail that feels slightly off-script.

**Word feels suspicious but not on the list?** Ask: "Would I say this in conversation?" If no, cut it or simplify.
