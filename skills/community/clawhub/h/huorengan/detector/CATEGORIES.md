# Category map: SKILL.md ↔ detector

This table is the anti-drift contract between the human-readable rules in
`../SKILL.md` and the executable engine. When you add a rule to the skill,
decide here whether it's regex-detectable (give it a detector `type`) or
LLM-only judgment (mark it so). When you add a detector `type`, point it back
at the skill section it enforces.

The engine exposes issue `type`s (see `TYPE_LABELS` in `patterns.js`). The
skill has more `###` sections than that — the gap is **not** missing coverage,
it's rules that are judgment calls a regex can't make.

Three counts coexist on purpose and should not be forced to match: the README's
**pattern-category count** (the human-facing prose catalog, guarded in CI), the
engine's `type`s (which split the vocabulary tiers and add stylometric signals),
and SKILL.md's `###` sections (which also include writer-side tests with no
detectable form). The `categories.test.js` check enforces the engine ↔ this-file
mapping.

## Column: language

`zh` = Chinese module (`zh/`), `en` = English module (`en/`), `both` = the same
pattern family implemented symmetrically. Stage 1 ships the `en` column;
`zh`/`both` fill in during stage 2.

## A. Direct mapping (skill rule → detector `type`)

| Detector `type` | Label | SKILL.md section | lang |
|---|---|---|---|
| `tier1` / `tier2` / `tier3` | AI vocabulary / Word cluster / Overused word | Tier 1/2/3 vocabulary | both |
| `transition` | AI transition | Structural anti-patterns | en |
| `template-phrase` | Template phrase | Structural anti-patterns | en |
| `tier3-phrase` / `tier3-phrase-cluster` | Boilerplate phrase / cluster | Structural anti-patterns | en |
| `chatbot` | Chatbot artifact | Chatbot artifacts | both |
| `sycophantic` | Sycophantic tone | Chatbot artifacts | en |
| `acknowledgment-loop` | Acknowledgment loop | Structural anti-patterns | en |
| `filler` | Filler phrase | Significance inflation | en |
| `hollow-intensifier` | Hollow intensifier | Significance inflation | en |
| `generic-conclusion` | Generic conclusion | Structural anti-patterns | both |
| `social-cta-closer` | Engagement-bait closer | Structural anti-patterns | en |
| `future-narrative` | Generic future narrative | Significance inflation | en |
| `lets-construction` | "Let's" opener | Chatbot artifacts | en |
| `reasoning-artifact` | Reasoning artifact | Chatbot artifacts | en |
| `significance-inflation` | Significance inflation | Significance inflation | both |
| `novelty-inflation` | Novelty inflation | Significance inflation | en |
| `real-actual-inflation` | "Real/actual" inflation | Significance inflation | en |
| `vague-attribution` | Vague attribution | Vague attribution | both |
| `emotional-flatline` | Emotional flatline | Structural anti-patterns | en |
| `cutoff-disclaimer` | Cutoff disclaimer | Chatbot artifacts | en |
| `false-concession` | False concession | Structural anti-patterns | en |
| `rhetorical-question` | Rhetorical question | Structural anti-patterns | en |
| `formulaic-opener` | Formulaic opener | Structural anti-patterns | en |
| `confidence-calibration` | Confidence stacking | Significance inflation | en |
| `hedge-stack` | Hedge-stacked prediction | Significance inflation | en |
| `parenthetical-hedge` | Parenthetical hedge | Structural anti-patterns | en |
| `hashtag-stuff` | Hashtag stuffing | Structural anti-patterns | en |
| `bullet-np-list` | Bullet-NP list | Structural anti-patterns | en |
| `title-case-header` | Title Case header | Structural anti-patterns | en |
| `em-dash` / `formatting` | Em dash overuse / Formatting | Structural anti-patterns | en |
| `uniformity` | Rhythm uniformity | Rhythm & uniformity | both |
| `low-ttr` | Low vocabulary diversity | Rhythm & uniformity | both |
| `ai-placeholder` | Unfilled placeholder | AI-tool fingerprints | both |
| `ai-citation-markup` | Chatbot citation markup leak | AI-tool fingerprints | both |
| `ai-utm-source` | AI-tool URL parameter | AI-tool fingerprints | both |
| `smart-punct-signature` | Smart-punct signature | Rhythm & uniformity (partial) | en |
| `zh-passive-stack` | 被动语态堆砌 | Translation tone (zh-only) | zh |
| `zh-long-attributive` | 长定语结构 | Translation tone (zh-only) | zh |
| `zh-translation-opener` | 基于/通过开头 | Translation tone (zh-only) | zh |
| `zh-via-to` | 通过…来…结构 | Translation tone (zh-only) | zh |
| `zh-for-x-regard` | 对于…而言 | Translation tone (zh-only) | zh |
| `zh-in-x-aspect` | 在…方面 | Translation tone (zh-only) | zh |

> **Partial map:** `smart-punct-signature` fires only on curly-quotes +
> em-dash + Oxford comma + clean typing co-occurrence (≥80 words), never on
> curly punctuation alone.

## B. Detector-only (stylometric / fingerprint — no skill prose)

Extend the skill with signals that work as math over the whole document:

| Detector `type` | Label | Why engine-only | lang |
|---|---|---|---|
| `punct-distribution` | Punctuation distribution | Per-paragraph punctuation uniformity | both |
| `fnword-trigram-entropy` | Grammar repetition | Function-word trigram entropy | en |
| `cross-para-burstiness` | Cross-paragraph rhythm | Sentence-length variance across paragraphs | both |
| `normalization-flag` | Bypass-trick chars | Zero-width / homoglyph humanizer-bypass detection | both |

## C. Skill-only (LLM judgment — no detector `type`)

Rules requiring reading for meaning — applied by the model, not the regex engine:

- Translation tone (Chinese-specific, translationese) — partial zh module in stage 2
- Promotional language
- False ranges
- Notability name-dropping
- Self-labeling significance
- When to rewrite from scratch vs. patch
- Severity tiers (P0 / P1 / P2)
- Self-reference escape hatch
- Output format
- ★ Voice pull (addition layer) — stage 4
