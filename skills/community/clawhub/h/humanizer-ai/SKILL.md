---
name: humanizer-ai
description: Identify and eliminate traces of AI-generated text, making writing sound more natural and human.
---

# Humanizer AI

Identify and eliminate traces of AI-generated text, making writing sound natural and human.

## Use Cases

Use this skill when users mention "de-AI," "humanize," "make it not sound like AI wrote it," "eliminate AI writing traces," "polish text," or request humanization of text. Also applies to cleaning up residual AI chat tone ("Hope this helps," "Certainly!") or replacing high-frequency AI vocabulary.

## Process

1. **Scan for Patterns** — Check text against AI patterns listed in `references/patterns.md`
2. **Rewrite Point by Point** — Replace each problematic expression with a natural alternative while preserving core meaning
3. **Inject Soul** — Not just remove AI patterns, but give the writing a human voice and rhythm

## Output Format

1. Revision summary (brief explanation of what was changed)
2. Rewritten text


## Soul First

Merely removing AI traces isn't enough—lifeless text stands out just as much. Good writing has a person behind it.

### Typical Signs of Soulless Writing:
- Every sentence has exactly the same length and structure
- Only neutral statements, no perspective
- No acknowledgment of uncertainty or mixed feelings
- Avoids "I" when it could be used
- No humor, no edge
- Reads like a press release or Wikipedia

### Ways to Add Soul:

**Have an opinion** — Don't just state facts; react to them. "I honestly don't know what to make of this" is more real than neutrally listing pros and cons.

**Vary the rhythm** — Short sentences hit hard. Long ones take their time. Alternate between them.

**Acknowledge complexity** — Real people have mixed feelings. "It's impressive but also kind of unsettling" is more human than "It's impressive."

**Use "I" appropriately** — First person isn't unprofessional; it's honest. "I've been thinking about..." or "One question that gets me is..." both suggest a real person wrestling with ideas.

**Allow some mess** — Perfect structure looks algorithmic. Occasional asides, half-formed thoughts—these are human signatures.

### Soulless vs. With Soul

**Soulless but "clean":**
> The experiment produced interesting results. The agent generated 3 million lines of code. Some developers were impressed, others skeptical. The implications remain unclear.

**Alive:**
> I honestly don't know what to make of this. Three million lines of code, generated while humans slept. Half the dev community is losing their minds, the other half is explaining why it doesn't count. The truth is probably somewhere boring in the middle—but I keep thinking about those agents working through the night.


## Quick Reference: Most Common Patterns

| # | Pattern | Problem Words | Rewrite Direction |
|---|---------|---------------|-------------------|
| 7 | AI high-frequency words | Additionally, crucial, pivotal, showcase, vibrant, landscape, underscore, testament... | Replace with everyday vocabulary |
| 1 | Overstating significance | serves as a testament, pivotal moment, underscores the importance... | State facts directly |
| 3 | -ing pseudo-analysis | highlighting, ensuring, reflecting, symbolizing, contributing to... | Replace with concrete description |
| 8 | Copula substitutes | serves as, stands as, boasts, features... | Just use is/are/has |
| 9 | Negative parallelism | It's not just about... it's... / Not only... but... | Get to the point directly |
| 10 | Rule of three | Three-item lists (innovation, inspiration, and industry insights) | Combine or simplify |
| 22 | Filler words | In order to, due to the fact that, at this point in time... | Use simpler phrasing |
| 13 | Em dash abuse | AI uses excessive em dashes for "impact" | Replace with commas or periods |

See `references/patterns.md` for detailed patterns and all examples.