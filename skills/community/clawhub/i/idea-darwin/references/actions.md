# Standard Actions Reference

This file describes the purpose, applicable scenarios, and execution requirements for each standard action in the Idea Darwin Engine.

## 1. Tagging

**Purpose**: Standardize idea categorization for scheduling, similarity matching, and crossbreeding.

**Tag Dimensions**:
- Topic tags: AI / Education / SaaS / Content / Creator Economy / ...
- Problem type: Efficiency / Innovation / Business Validation / Collaboration / Automation
- Stage tags: seed / exploring / refining / validated / dormant
- Style tags: High-innovation / High-risk / Practical / Research-oriented / Platform-type
- Resource tags: Low-cost / High-cost / Data-dependent / Engineering-heavy / Requires user ops

**Execution Requirements**:
- Each idea needs at least 3 tags, no more than 8
- Tags should be specific — avoid overly broad labels (e.g., "technology" is too vague; use "natural language processing" instead)
- Write tags into the card's YAML frontmatter `tags` field

---

## 2. Card Generation

**Purpose**: Transform a natural-language idea into a structured card the system can process.

**Generated Content**:
- Core question: What is this idea really trying to answer?
- Full description: 2–4 paragraphs covering origin, importance, and most promising current form
- Current tension: The key contradiction or open question
- Directions for deepening
- Cross candidates

**Execution Requirements**:
- Strictly follow the `assets/card-template.md` format
- The core question must be a clear, well-formed question
- The full description is a structured distillation, not a copy-paste of the original text

---

## 3. Deepen

**Purpose**: Turn vague ideas into clear ones and rough ideas into complete ones.

**When to Use**:
- The idea has potential but is poorly articulated
- The logic is incomplete
- Target users, scenarios, or paths need to be specified

**Deepening Angles**:
- 5W1H (Who / What / Where / When / Why / How)
- First principles decomposition
- User scenario concretization
- Technical roadmap mapping
- Business model exploration
- Risk and constraint identification
- MVP path design
- Failure point enumeration

**Execution Requirements**:
- This is not a rewrite — it's about filling logical gaps
- Preserve the idea's core intent
- Output must include: enriched description, core assumptions, user scenarios, MVP version, risks, and suggested next action
- Update the card's "Full Description" and "Directions for Further Deepening"

---

## 4. Derive

**Purpose**: Split an idea into variants to expand the search space.

**Derivation Dimensions**:
- Different user segments
- Different business models
- Different technical implementations
- Different scenarios
- Different difficulty levels
- Different product forms
- Different time horizons (short-term / long-term)

**Execution Requirements**:
- Produce 2–3 child ideas per derivation (never more than 3, to prevent combinatorial explosion)
- Each child must retain the parent's core DNA but have a clear differentiator
- Do not generate variants that are merely rephrased duplicates
- Each child gets a new IDEA-XXXX ID automatically
- Update the parent's `child_ids` and each child's `parent_ids`
- Each child requires full card generation and initial scoring

---

## 5. Cross / Hybridize

**Purpose**: Fuse different ideas to generate new perspectives.

**Two Types**:
1. **Neighbor cross**: Cross with similar ideas → convergent optimization
2. **Distant cross**: Cross with unrelated ideas → innovative breakthroughs (primarily used in disruption rounds)

**Cross Analysis Flow**:
1. Analyze commonalities between the two ideas
2. Analyze complementary strengths
3. Analyze conflicts and boundaries
4. Generate 1–3 new hybrid ideas
5. Evaluate each hybrid's core mechanism and value

**Execution Requirements**:
- New ideas get auto-assigned IDs
- New ideas' `parent_ids` include both source idea IDs
- Update both source ideas' `child_ids`
- Crossing is not mechanical concatenation — extract the valuable parts from each to form a genuinely new concept

---

## 6. Critique

**Purpose**: Force-find weaknesses to prevent the system from becoming an echo chamber.

**Checklist**:
- Is it self-contradictory?
- Are the assumptions too strong?
- Is there a lack of real demand?
- Is the cost prohibitively high?
- Is this just a repackaged old idea?
- Is there no validation path?
- What's the most likely point of failure?

**Execution Requirements**:
- Output: list of core flaws, risk level, recommendation to continue or not, what to fix first
- After critique, update the card's "Current Tension"
- If serious issues are found, lower the corresponding score dimensions

---

## 7. Validate

**Purpose**: Determine whether an idea is worth continuing to invest resources in.

**Layer 1: Fatal Flaw Check** (4 Yes/No questions):
1. Does it have a logical flaw? (Is the core assumption self-contradictory or clearly invalid?)
2. Does it lack real demand? (Is there no identifiable target user or use case?)
3. Is it completely infeasible? (Are there insurmountable barriers in technology/resources/path?)
4. Is it a near-duplicate of an existing idea? (Is it just a rephrased version?)

Any "Yes" → `validated: false`.

**Layer 2: Value Judgment** (only if Layer 1 is all "No"):
1. Is it worth continuing to invest?
2. What should the next action be?
3. What is the current biggest risk?

**Execution Requirements**:
- Validation failure → lower Priority Score, report to user
- The user decides whether to dormant or remove — the system only recommends
- Validation pass → may recommend state promotion (e.g., exploring → refining)

---

## 8. Merge / Deduplicate

**Purpose**: Prevent the idea pool from bloating with highly redundant content.

**Trigger Conditions**:
- Two ideas share the same core assumption
- They differ only in wording
- Tags heavily overlap and descriptions are similar

**Handling**:
- Merge into a primary idea + variant record
- Mark the absorbed idea as `merged_into: IDEA-XXXX`
- Preserve the branch but lower its priority

**Execution Requirements**:
- A similarity check across the full pool is mandatory at the end of every round
- Similarity judgment is based on tag overlap rate + core question similarity
- When merging, keep the version with richer information as the primary idea
- Record merge history in the card's "Change Log"
