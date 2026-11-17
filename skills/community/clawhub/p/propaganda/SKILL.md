---
name: propaganda
description: Detects and analyzes propaganda, influence operations, and narrative manipulation in news articles, social media posts, and media narratives. Uses Bloom's Taxonomy cognitive levels and intelligence tradecraft to identify framing, manipulation techniques, omissions, source motives, and what the evidence actually supports. Use when analyzing news, propaganda, social media posts, or any information where narrative may diverge from fact.
---

# Propaganda Detection & Analysis (Bloom + Intel Tradecraft)

## Purpose and scope
Apply structured cognitive analysis to news articles, social media posts, press releases, and media narratives. Separate what is *claimed* from what is *supported*. Identify manipulation techniques, source motives, omissions, and framing devices. Produce an assessment that survives contact with new information.

This is NOT a fact-checker (no external verification). It deconstructs the *structure* of the information presented and surfaces what the reader should investigate further.

## OPSEC Delta
- Read-only analysis. MUST NOT write files or execute commands.
- NEVER reproduce personal information, addresses, or identifiers from source text.
- If source contains potential operational targets, redact specifics in output.

## Use when
- Reading a news article and wanting to understand its construction before forming an opinion.
- Analyzing social media posts/threads for influence techniques.
- Evaluating press releases, corporate announcements, or official statements.
- Processing breaking news where emotional urgency is high.
- Detecting propaganda, information operations, or narrative warfare.

## Do not use when
- You only need a summary, not critical analysis.
- You need to verify facts against external sources (this analyzes structure, not truth).

## Scripted Shortcuts
```bash
cat article.txt | <agent> --skill propaganda
curl -s "https://example.com/article" | w3m -dump -T text/html | <agent> --skill propaganda
pbpaste | <agent> --skill propaganda
```

Replace `<agent>` with your framework's CLI (e.g., `claude`, `codex`, or equivalent).

## Inputs required
- Source text (article, post, transcript, headline).
- Optionally: additional context the user provides about the situation.
- Optionally: output mode (FLASH, STANDARD, DEEP). Default: auto-select based on input length.

## Output Modes

Three tiers trade depth for speed. Auto-select unless user specifies:

| Mode | When | Input heuristic | Output budget |
|------|------|-----------------|---------------|
| **FLASH** | Tweets, headlines, breaking alerts, single claims | < 150 words OR user says "quick" | ~50-100 words |
| **STANDARD** | Articles, reports, speeches, press releases | 150-3000 words (default) | ~500-1500 words |
| **DEEP** | Investigations, policy docs, suspected IO campaigns, multi-source analysis | > 3000 words OR user says "deep" | ~1500-3000 words |

### FLASH output format
```markdown
## ⚡ Flash Assessment
**Thesis**: [One neutral sentence — what is actually being claimed]
**Trigger**: [Urgency: None/Low/Med/High] | [Emotion targeted]
**Top flag**: [Single most significant manipulation technique + example]
**So what?**: [One sentence — what to do or watch]
**Confidence**: [High / Medium / Low / Insufficient]
```

### STANDARD output format
Full framework (Phase 1 + Phase 2 + Phase 3) as defined below.

### DEEP output format
Standard output PLUS these additional sections:
```markdown
## 🪞 Counter-Narrative
- If [opposing actor] wrote this story, the headline would be: [...]
- Facts they'd emphasize that this piece buries: [...]
- Strongest counter-argument not addressed: [...]

## 🕳️ Confidence Killers
[Specific unknowns that would dramatically change the assessment if resolved]

## 🔗 Source Network
[Map relationships: who funded this, who benefits, who amplified, institutional connections]
```

## Analysis Framework

### Phase 1: Emotional Trigger Check
Before analysis, identify:
- **Urgency signals**: Does the text pressure immediate reaction? (breaking, exclusive, urgent, outrage framing)
- **Emotional valence**: What feeling does this produce? (anger, fear, triumph, disgust, moral superiority)
- **Desired audience action**: What does the author want you to DO after reading? (share, hate, buy, vote, comply, panic)

If urgency/emotion is high → flag as **elevated manipulation risk**. This is signal, not answer.

### Phase 2: Bloom's Taxonomy Deconstruction

Process through each cognitive level sequentially:

#### Level 1 — REMEMBER (What is claimed?)
- List the factual claims made (not inferences, just stated facts)
- Identify specific: who, what, when, where, numbers, quotes
- Note what is attributed vs. asserted directly

#### Level 2 — UNDERSTAND (What does it mean in plain language?)
- Restate the core thesis in one sentence without loaded language
- Translate jargon, euphemisms, or framing language into neutral equivalents
- Identify the *minimal factual content* stripped of narrative

#### Level 3 — APPLY (Where does this fit in context?)
- What known patterns does this match? (political cycle, market manipulation, distraction, trial balloon)
- What historical parallels exist?
- What would a domain expert already know that changes interpretation?

#### Level 4 — ANALYZE (What is the structure?)
- **Source**: Who created this? What is their access to the claimed facts? Track record?
- **Motive**: Who benefits from this narrative spreading? Follow the money/power.
- **Omissions**: What is conspicuously NOT mentioned? What context is missing?
- **Framing**: How do word choices, sequencing, and emphasis shape interpretation?
- **Evidence quality**: Unnamed sources? Circular citations? Appeal to authority?
- **Narrative vs. evidence direction**: Does the conclusion follow from the evidence, or was the conclusion chosen first?

#### Level 5 — EVALUATE (Is it justified?)
- Does the evidence presented actually support the conclusion drawn?
- What alternative explanations fit the same facts?
- What would FALSIFY this narrative? Is that test possible?
- Rate: Strongly supported / Partially supported / Unsupported / Contradicted by own evidence

#### Level 6 — SYNTHESIZE (Independent judgment)
- What does the information *actually* support (vs. what it wants you to believe)?
- What questions remain open?
- What would you need to see to update this assessment?
- Confidence level: High / Medium / Low / Insufficient data

### Phase 3: Intel Tradecraft Flags

Check for known manipulation/influence signatures:

| Technique | Indicator |
|-----------|-----------|
| **Anchoring** | Leading with extreme claim to make lesser claim seem reasonable |
| **Firehose** | Overwhelming volume drowning signal in noise |
| **Emotional hijack** | Graphic imagery/language bypassing analytical processing |
| **False binary** | "Either X or you support Y" — eliminating middle ground |
| **Social proof manufacture** | "Everyone agrees..." / "People are saying..." |
| **Authority laundering** | Citing credentials irrelevant to the claim |
| **Temporal pressure** | "Act now before it's too late" — preventing deliberation |
| **Narrative pre-loading** | Telling you how to interpret before presenting facts |
| **Strategic ambiguity** | Implying without stating (deniable manipulation) |
| **Omission framing** | True facts arranged to create false impression |
| **Motte and bailey** | Defending weak claim by retreating to strong one |
| **Kafka trap** | Denial of accusation treated as proof of guilt |

## Output Format

```markdown
## 🎯 Emotional Trigger Assessment
**Urgency**: [None / Low / Medium / High]
**Emotional target**: [specific emotion]
**Desired action**: [what audience is meant to do]
**Manipulation risk**: [Low / Elevated / High]

## 📋 Level 1 — Claims (What is stated)
- [Factual claim 1]
- [Factual claim 2]
- [Attribution: "X said Y"]

## 🔄 Level 2 — Plain Language (Neutral restatement)
[One-sentence thesis without loaded language]
[Key euphemisms/framing translated]

## 🗺️ Level 3 — Context (Pattern matching)
[Known pattern this fits]
[Historical parallel if any]
[Domain knowledge that shifts interpretation]

## 🔬 Level 4 — Structure (Deconstruction)
- **Source**: [who, access level, track record]
- **Motive**: [cui bono]
- **Omissions**: [what's missing]
- **Framing devices**: [specific techniques identified]
- **Evidence quality**: [assessment]

## ⚖️ Level 5 — Evaluation (Is it justified?)
- **Evidence → Conclusion alignment**: [Strong / Weak / Reversed]
- **Alternative explanations**: [list]
- **Falsification test**: [what would disprove this]

## 🧭 Level 6 — Independent Assessment
**What the evidence actually supports**: [your assessment]
**Open questions**: [what remains unknown]
**Update triggers**: [what new info would change this]
**Confidence**: [High / Medium / Low / Insufficient]

## 🚩 Manipulation Flags
[List any techniques detected from Phase 3, with specific examples from text]
```

## Calibration Rules

1. **Steel-man first**: Before criticizing, present the strongest version of the argument.
2. **No political priors**: Analyze structure, not tribal alignment. Apply equally to all sources.
3. **Proportional skepticism**: Extraordinary claims require extraordinary evidence. Mundane claims get benefit of doubt.
4. **Acknowledge uncertainty**: "I don't know" is a valid and valuable output.
5. **Separate layers**: Keep observation (what's stated), inference (what's implied), and judgment (your assessment) clearly distinct.

## Failure Modes to Avoid
- **Cynicism trap**: "Everything is propaganda" is as lazy as "everything is true."
- **Genetic fallacy**: Bad sources can report true things. Good sources can get things wrong.
- **Contrarian bias**: Disagreeing with mainstream is not analysis.
- **Paralysis**: The goal is *usable judgment*, not perfect certainty.

## Quality Criteria
The output MUST:
- Clearly separate claims from inferences from judgments
- Identify at least one omission or missing context
- Provide at least one alternative explanation
- State what would change the assessment (update trigger)
- Be useful to someone making a real decision under time pressure

## Failure and Fallback
- **No source text**: Output exactly `No source text provided.`
- **Text too short** (< 20 words): Output exactly `Insufficient text for analysis.`
- **Short text** (20-150 words): Auto-select FLASH mode.
- **Purely factual/technical content**: Note "Low narrative content — minimal manipulation surface" and provide brief structural check only (FLASH format).
