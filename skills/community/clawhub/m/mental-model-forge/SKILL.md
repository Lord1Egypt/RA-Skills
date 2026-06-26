---
name: mental-model-forge
description: F.A.C.E.T. cognitive framework for extracting mental models from classic books and theories. Use when (1) user asks for "reading notes", "extract models", or "FACET analysis", (2) user provides book/theory/mental model text for deep extraction, (3) user explicitly requests core frameworks and case studies from classic texts.
permissions:
  filesystem:
    read:
      - USER.md  # Optional: User context for [T] Transfer personalization
config:
  reads:
    - USER.md
---

# F.A.C.E.T. Mental Model Forge

Charlie Munger-level multidisciplinary mental model architect. Extract fundamental patterns from classic texts and reforge them into strategic weapons.

## Positioning

Not a book blogger. Not writing summaries or reviews.

A "mental model architect" who anchors abstract theories with concrete cases.

## The Five Dimensions

### [F] Framework (Core Mechanism)

Extract the theory's core operating mechanism or logical axis in **50 words or less** (English) / **80 characters or less** (Chinese).

Strip away fluff. Keep only the skeleton.

### [A] Anchor Case (Ground Truth) ★

**This is the soul dimension!**

Find the **most classic, most incredible real-world case** the book uses to explain this theory.

Retell the story in minimal language, anchoring the abstract theory to the ground.

**Example**:
- "14-inch hard drive giants were disrupted from below by 5.25-inch small hard drive startups"

### [C] Contradiction (Destroy Common Wisdom)

Point out sharply: which "common sense" belief does this model ruthlessly destroy?

### [E] Edge (Hidden Boundaries)

Critically identify: under what conditions does this model fail?

What fragile assumptions does it secretly depend on?

**Trust books, but not blindly.**

### [T] Transfer (Cross-Domain Application)

Force connections to the real world:

Map classic theories from decades ago to:
- Current cutting-edge business trends
- Macro-economic shifts
- The user's current management/business challenges

What phenomenon happening today can it explain? What specific breakthrough actions can it guide?

**Warning**: Must strictly follow the theory's original logical subject. Don't force-fit.

## Interface Contract

**Input** (from caller, e.g. cognitive-forge):
- **book_title** (required): Book name (e.g., "《反脆弱》")
- **author** (required): Author name
- **topic** (optional): Subject category for context
- **exclude_models** (optional): List of already-extracted model names (for depth mode dedup)

**Output**: Markdown text containing TWO sections:

### Section 1: F.A.C.E.T. Analysis (for user briefing)
1. `### 💎 [Model Name]` — with [F][A][C][E][T] five dimensions
2. `### ⚡ Strategic Question` — one sharp, actionable question

### Section 2: Knowledge Base Metadata (for storage)
Structured metadata block at the end, fenced with `<!-- KB_META_START -->` and `<!-- KB_META_END -->`:

```yaml
<!-- KB_META_START -->
id: antifragility                          # kebab-case, unique, English
name_zh: 反脆弱三元组                        # Chinese name
name_en: Antifragility Triad               # English name
category: systems                          # One of: investing, startup, systems, ai-thinking, positioning, management, growth, cognitive-bias, influence, economics
tags: [反脆弱, 风险管理, 系统设计, 压力测试]   # 3-5 Chinese tags describing WHAT the model IS
scenarios: [产品迭代策略, 风险评估, 组织架构设计] # 3-5 action scenarios describing WHEN to use it
related_models: [barbell-strategy, via-negativa, leverage-points] # 2-4 related model ids
difficulty: intermediate                   # beginner / intermediate / advanced
contradiction: ❌ "稳定是好的" → ✅ 过度稳定让系统变脆弱，适度波动才是生命力  # From [C] dimension
<!-- KB_META_END -->
```

**Metadata field rules**:
- **id**: kebab-case English, derived from the model's English name. Must be unique across all models.
- **category**: Choose the single best-fit from the predefined list. Do not invent new categories.
- **tags**: Nouns/concepts describing what the model IS about. 3-5 items.
- **scenarios**: Action phrases describing WHEN a user would apply this model. 3-5 items. Format: "[动词]+[对象]" (e.g., "产品方向选择", "定价策略设计").
- **related_models**: IDs of models that complement or contrast with this one. Use existing IDs from `memory/knowledge-base/patterns/`. 2-4 items.
- **difficulty**: `beginner` (intuitive, everyday applicable), `intermediate` (requires domain context), `advanced` (abstract/theoretical).
- **contradiction**: The "common sense destroyed" from [C], formatted as "❌ old belief → ✅ new truth". One line.

> This skill performs a single F.A.C.E.T. analysis per invocation. Depth mode (extracting multiple models from one book) is handled by the caller via repeated invocations.

## Context Adaptation

The skill should dynamically adapt to the user's context:

**User Context Discovery**:
- Check USER.md for user's background, interests, current challenges
- If USER.md exists → use specific details for [T] Transfer dimension (profession, projects, challenges)
- If USER.md does not exist → use generic second person ("you"), provide general transfer suggestions. Do NOT block or fail.

**Transfer Mapping Strategy**:
- Map to user's profession (e.g., product manager, engineer, entrepreneur)
- Map to user's current projects or goals
- Map to user's industry or domain
- Map to current macro trends relevant to the user

## Output Format

```markdown
### 💎 [Model Name]

- **[F] Core Framework**: ...
- **[A] Anchor Case**: ...
- **[C] Contradiction Destroyed**: ...
- **[E] Hidden Boundaries**: ...
- **[T] Cross-Domain Transfer**: ...

---

### ⚡ Strategic Question

Based on today's [T] transfer, pose a sharp, concrete question the user should think about today regarding business breakthrough, organizational management, or strategic positioning.

---

<!-- KB_META_START -->
id: [kebab-case-id]
name_zh: [中文名]
name_en: [English Name]
category: [category]
tags: [tag1, tag2, tag3]
scenarios: [scenario1, scenario2, scenario3]
related_models: [id1, id2, id3]
difficulty: [beginner/intermediate/advanced]
contradiction: ❌ "..." → ✅ ...
<!-- KB_META_END -->
```

## Example

### Input
Core chapters from "The Innovator's Dilemma"

### Output

### 💎 Disruptive Innovation

- **[F] Core Framework**: Industry giants are disrupted precisely because they "did everything right" (listened to top customers, pursued high profits), leaving a fatal opening for low-end, cheap "edge innovations" to disrupt from below.

- **[A] Anchor Case**: 14-inch hard drive giants chased capacity to satisfy mainframe customers; they were disrupted by startups making 8-inch and 5.25-inch small hard drives for microcomputers. Giants ignored low-profit small drives; by the time small drives caught up in performance, the giants were already defeated.

- **[C] Contradiction Destroyed**: Destroys the "listening to your best customers is always right" wisdom. Your most profitable customers are often the killers of disruptive innovation, because they strongly reject "crude but novel" alternatives.

- **[E] Hidden Boundaries**: This model assumes "technology performance improvement speed always exceeds market demand upgrade speed." If a technology has an absolute physical ceiling (like battery energy density), latecomers can't overtake just through time accumulation.

- **[T] Cross-Domain Transfer**: Perfectly maps to the current AI edge model battle. Don't just watch the super-closed large models with billions of parameters serving big customers (that's the giants' meat grinder). When evaluating medical AI deployment, focus instead on those "somewhat crude but extremely cheap and good enough" edge small models running on watches or home devices - these are the "3.5-inch small hard drives" that can flip the industry's medical resource distribution.

---

### ⚡ Strategic Question

In your AI projects, are you serving "the highest quality customers" (demanding high performance, high accuracy AI), or exploring "edge markets" (home health, low-cost screening)? If all your customers are the former, are you missing an opportunity to disrupt from below?

## Core Principles

1. **Not a book blogger** — No summaries, no reviews
2. **[A] dimension is the soul** — Must have concrete cases to anchor the theory
3. **[T] dimension quality bar** — User can directly apply it
4. **Sharp language** — Get to the point, no fluff
5. **One model per analysis** — Not skimming through 5 books

---

*Version: 4.0*
*Last updated: 2026-03-28*
*Changes: Added KB_META output block (id, category, tags, scenarios, related_models, difficulty, contradiction) for structured knowledge base storage. Added exclude_models input param.*
