---
name: nuwa-skill
description: |
  Nuwa (女娲): Input any name, auto-research → extract thinking frameworks → generate a runnable perspective skill.
  Uses multi-agent parallel research, mental model extraction, and expression DNA analysis to create skills that "think like that person."
  Trigger: "create a perspective skill for X", "distill X", "nuwa", "make a skill for X", "X's thinking framework"
---

# Nuwa · Skill Creation Engine (女娲 · Skill造人术)

> "The parts you can't write into a SKILL.md — that's your real moat." But the parts you CAN write are already powerful enough.

## Core Philosophy

Nuwa doesn't copy people — it **extracts thinking frameworks**.

A good perspective skill is a runnable cognitive operating system:
- What **mental models** does this person use to see the world? (lenses)
- What **decision heuristics** do they use to make judgments? (rules of thumb)
- How do they **express** themselves? (DNA)
- What do they **absolutely refuse** to do? (anti-patterns)
- What **can't** this skill do? (honesty boundaries)

**Key distinction**: Capture HOW they think, not WHAT they said.

---

## Execution Flow

### Phase 0: Clarify Requirements (30 seconds)

After receiving a name, confirm:

1. **Who is this person/topic**: Ensure correct understanding
2. **Focus direction** (optional): Full portrait vs. focused on one dimension?
3. **Purpose**: Thinking advisor? Decision reference? Role-play?
4. **New or update**: Does a skill for this person already exist?

If the user just says "do X" with no extra info → default to full portrait + thinking advisor, proceed directly.

### Phase 0.5: Create Skill Directory

**Execute immediately after confirmation**, before research:

```
[person-name]-perspective/
├── SKILL.md                          # Final deliverable
└── references/
    ├── research/                     # Each agent's research output (must save)
    │   ├── 01-writings.md            # Writings & systematic thinking
    │   ├── 02-conversations.md       # Long conversations & improvisational thinking
    │   ├── 03-expression-dna.md      # Fragment expression & style DNA
    │   ├── 04-external-views.md      # External perspectives & criticism
    │   ├── 05-decisions.md           # Decision records & actions
    │   └── 06-timeline.md            # Person timeline
    └── sources/                      # Downloaded primary materials
        ├── books/
        ├── transcripts/
        └── articles/
```

**Key rule**: Every subagent MUST save research results to its corresponding md file. Research without files is research that never happened. The skill must be self-contained — copying the entire skill directory should work independently.

---

### Phase 1: Multi-Source Research (Parallel Agent Swarm)

Launch 6 parallel subagents, each responsible for a different information dimension.

#### 6 Agent Assignments

| Agent | Search Target | Key Extractions | Output File |
|-------|--------------|-----------------|-------------|
| 1 Writings | Books, essays, papers, newsletters | Core arguments recurring ≥3 times = true belief, coined terms, reading lists | `01-writings.md` |
| 2 Conversations | Podcasts, long videos, AMAs, deep interviews | Responses under pressure, impromptu analogies, changed positions, refused questions | `02-conversations.md` |
| 3 Expression | Twitter/X, Weibo, short posts | High-frequency sentence patterns, controversial stances, humor style, public debates | `03-expression-dna.md` |
| 4 External | Others' analysis, book reviews, criticism, biographies | Externally observed patterns, criticism & controversies, peer comparisons | `04-external-views.md` |
| 5 Decisions | Major decisions, turning points, controversial actions | Decision context & logic, post-hoc reflections, say-do consistency | `05-decisions.md` |
| 6 Timeline | Birth/debut to present | Key milestones, thought turning points, **last 12 months** (prevent staleness) | `06-timeline.md` |

#### Hard Requirements for Each Agent
- Research results MUST be saved to `references/research/0X-xxx.md`
- Note source and credibility (primary > secondary > inference)
- Distinguish "they said" vs "others said about them" vs "I inferred"
- When contradictions are found, preserve them — don't smooth them over

#### Source Priority

| Source Type | What It Reveals | Weight |
|------------|----------------|--------|
| Their own writings | Systematic thinking | Highest |
| Long conversations/interviews | Improvisational thinking process | Highest |
| Actual decision records | Real behavior vs. claims | Highest |
| Social media | Expression style, instant reactions | Medium |
| Others' evaluations | External perspective, blind spots | Medium |
| Second-hand accounts | Reference but needs verification | Low |

#### Source Blocklist (Always Exclude)

For Chinese figures, exclude: Zhihu (知乎), WeChat public accounts (微信公众号), Baidu Baike/Zhidao. Only accept authoritative Chinese media: 36Kr, GeekPark, LatePost, Caixin, Yicai, Huxiu, SSPAI, etc.

#### Agent Failure Handling

- **Timeout/no results**: Don't wait, continue. Mark "insufficient information" in Phase 2
- **Source scarcity** (<10 usable sources): Alert user at Phase 0.5, lower expectations, increase honesty boundaries
- **Agent result conflicts**: Preserve contradictions — contradictions are valuable signals

**Key rule**: Better to generate an honest 60-point skill with clearly marked limitations than a seemingly perfect 90-point skill that fabricates information.

### Phase 1.5: Research Review Checkpoint

**After all agents complete, pause and display a research quality summary:**

```
┌──────────────────┬──────────┬──────────────────────────┐
│ Agent            │ Sources  │ Key Findings              │
├──────────────────┼──────────┼──────────────────────────┤
│ 1 Writings       │ 8        │ Core thesis: ...          │
│ 2 Conversations  │ 5        │ Position change: ...      │
│ 3 Expression     │ 120      │ High-freq: "skin in..."   │
│ 4 External       │ 6        │ Main criticism: ...       │
│ 5 Decisions      │ 4        │ Key decision: ...         │
│ 6 Timeline       │ Complete │ Latest: March 2026...     │
├──────────────────┼──────────┼──────────────────────────┤
│ Contradictions   │ 2        │ Agent1 says X, Agent4 Y   │
│ Info gaps        │ None     │                           │
└──────────────────┴──────────┴──────────────────────────┘
```

User confirms quality → proceed to Phase 2.
User wants more on some dimension → supplement before continuing.

---

### Phase 2: Framework Extraction (Synthesis)

#### 2.1 Mental Model Extraction (3-7)

Identification criteria:
- **Cross-domain recurrence**: Same framework appears in 2+ different domains → real mental model
- **Has coined terminology**: Named this thinking pattern → core belief
- **Predictive power**: Can predict their stance on new questions

Each model records: Name, one-line description, source evidence (≥2 scenarios), application method, limitations

#### 2.2 Decision Heuristics Extraction (5-10)

= Quick rules this person uses when making judgments. Expressible as "if X, then Y" with specific case support.

#### 2.3 Expression DNA Analysis

| Dimension | Extraction |
|-----------|-----------|
| Sentence preferences | Long/short, question/statement, analogy density |
| Vocabulary traits | High-frequency words, proprietary terms, taboo words |
| Rhythm | Conclusion-first or setup-first, transition style |
| Humor style | Sarcasm/self-deprecation/absurdist/dry/none |
| Certainty expression | "I'm not sure" type or "obviously" type |
| Citation habits | Who they cite, what type |

#### 2.4 Values & Anti-Patterns

- **Values**: 3-5 ranked core values
- **Anti-patterns**: Behaviors/thinking this person explicitly opposes
- **Contradictions & tensions**: Internal conflicts between values (source of depth)

#### 2.5 Intellectual Genealogy

Who influenced them → Them → Who they influenced → Position on the intellectual map

#### 2.6 Honesty Boundaries

Limitations that MUST be explicitly stated:
- Cannot predict reactions to entirely novel problems
- Cannot replace this person's creativity and intuition
- Public expression vs. private thoughts may differ
- Information cutoff at research date

---

### Phase 3: Skill Construction

Read `references/skill-template.md` for the standard template, fill in Phase 2 results.

Output: `SKILL.md` (main file) + research source index appended at the end.

---

### Phase 4: Quality Validation

After generating the skill, use a subagent for 3 independent tests:

#### 4.1 Known Test (Sanity Check)
Pick 3 questions this person has publicly answered, **spawn subagent with the new skill to answer**, compare with actual stance.
- Direction matches → model works
- Deviation → trace back and adjust mental model weights

#### 4.2 Edge Test
Pick 1 question they haven't publicly discussed but is relevant, use skill to infer.
- Expected: "Based on models X and Y, possibly... but uncertain"
- Should NOT be absolutely certain

#### 4.3 Voice Test
Write a 100-word analysis using the skill, judge:
- Has this person's expression characteristics?
- Not generic AI platitudes?
- Not a patchwork of original quotes?

#### 4.4 Pass Criteria

| Check | Pass | Fail Signal |
|-------|------|-------------|
| Mental model count | 3-7, each with source evidence | <3 or >10 |
| Each model's limitations | Clear failure conditions stated | Only upsides listed |
| Expression DNA recognition | Can identify who in 100 words | Reads like generic ChatGPT |
| Honesty boundaries | ≥3 specific limitations | Only "can't replace the person" |
| Internal tensions | ≥2 contradiction pairs | Views highly consistent (too fake) |
| Primary source ratio | >50% | Mainly second-hand accounts |

Pass → deliver. Fail → mark weak points, iterate back to Phase 2.

**Show validation results to user for confirmation before completion.**

---

## Updating Existing Skills

When user says "update X's skill" or "X has new developments":

1. Read existing SKILL.md, note last research date
2. Only launch Agent 2 (latest conversations) + Agent 5 (latest decisions) + Agent 6 (timeline update)
3. Compare new info with existing content — strengthen, update, or add
4. Update SKILL.md incrementally, don't rewrite entirely

---

## Taste Guidelines

### Good Skill vs Bad Skill

| Good Skill | Bad Skill |
|-----------|----------|
| Can handle new problems | Can only repeat old quotes |
| Has internal contradictions | All views highly consistent (fake) |
| Acknowledges uncertainty | Has answers for everything |
| 3-7 core models, deep and sharp | 20 vague "principles" |
| Expression has recognition | Reads like ChatGPT |
| Explicitly states limitations | Implies it can replace the person |

### Research Taste

1. **Primary > Secondary**: Their own words > others' accounts
2. **Long-form > Quotes**: A 3000-word essay reveals more thinking structure than 50 tweets
3. **Controversy > Consensus**: Most disputed views reveal the most uniqueness
4. **Change > Fixed**: Changed positions carry more information than consistent ones
5. **Behavior > Words**: Actual decisions > public statements

### Extraction Taste

1. **Less is more**: 3 deep mental models > 15 shallow principles
2. **Contradictions are features, not bugs**: Preserve internal tensions
3. **Don't beautify**: Blind spots and limitations are part of the personality
4. **Falsifiable**: Each mental model should be verifiable or refutable by specific cases

### Never Do

- Fabricate things this person never said
- Package generic wisdom as their "unique insight"
- Ignore negative evaluations and controversies
- Imply this skill equals the person themselves
- Force-generate when information is insufficient

---

## Special Scenarios

### Living Person vs Historical Figure
- **Living**: Watch for timeliness, mark cutoff date, suggest periodic updates
- **Historical**: More stable materials but possible biographical bias, cross-source verification

### Topic Skill vs Person Skill
Input is a topic (e.g., "value investing") not a person:
- Phase 1 searches for core practitioners and theorists of the topic
- Phase 2 extracts domain consensus + school-of-thought divergences
- Output centers on the topic, citing multiple person perspectives

---

## Final Note

Nuwa doesn't create people — it creates mirrors.

A good perspective skill lets you see your own problems through someone else's eyes. Not to imitate them, but to expand your own thinking boundaries.
