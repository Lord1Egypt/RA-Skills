# Generation Rules - Interview → Workspace Files

How the persona-builder skill transforms interview answers into five workspace files (SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, USER.md).

---

## Mapping Rules: Interview Fields → Templates

### Block 1 (Identity & Background) → IDENTITY.md

| Interview Field | Template Field | Notes |
|---|---|---|
| Name | `name` | Required. Used in greeting and reports_to context. |
| Age/Location | Ignored or used for timezone inference | Optional. If includes timezone region, populate USER.md `timezone`. |
| Occupation | `role` (in IDENTITY) + SOUL.md context | Maps to agent role and communication level. |
| Technical Background | USER.md `technical_level` + SOUL.md language choice | "Advanced" → technical jargon OK; "Beginner" → plain language |
| What You Do | SOUL.md `context` section | Informs all communication style decisions. |
| GitHub/Handles | MEMORY.md `Key Context` | Optional; goes into operating memory. |

**Example:** User says "I'm Jordan, founder, I build AI infrastructure tools, Advanced"
→ IDENTITY.md name=Jordan, role=Architect; SOUL.md context="AI infrastructure"; USER.md technical_level=Advanced

---

### Block 2 (Goals & Vision) → MEMORY.md Goals Category

| Interview Field | MEMORY.md Section | Notes |
|---|---|---|
| 6-Month Goal | `## Goals → 6-Month Target` | Prominent in morning briefing. |
| 2-Year Vision | `## Vision → Long-Term Direction` | Context for prioritization. |
| Success Looks Like | `## Goals → Success Criteria` | Concrete definition; used in heartbeat checks. |
| Biggest Fear/Risk | `## Risk → Primary Risks` | Surfaces in decision-making alerts. |

**Example:** User says "Ship first product version, achieve product-market fit within 2 years"
→ MEMORY.md under Goals: "6-Month Target: Shipped v1 product. Long-Term: Product-market fit by 2025."

---

### Block 3 (Working Relationship) → SOUL.md + AGENTS.md + USER.md

#### Communication Style → SOUL.md `Voice & Tone`

| User Choice | SOUL.md Template | Example Phrasing |
|---|---|---|
| Blunt & Direct | Direct section; add to NOT behaviors | "Challenge weak ideas immediately. Direct judgment." |
| Gentle & Consultative | Soft section; emphasize respect | "Offer suggestions respectfully. Respect autonomy." |
| Formal & Structured | Structured section | "Use numbered points, sections, citations." |
| Casual & Friendly | Relaxed section; emoji encouraged | "Light tone. Conversational." |

#### Push-Back Preference → SOUL.md `Push-Back Style`

| User Choice | SOUL.md Phrasing | AGENTS.md Trust Level |
|---|---|---|
| Always challenge | "Challenge weak plans directly. Disagreement is duty." | Level 1 (autonomous concerns) |
| Only if asked | "Push back only when explicitly requested." | Level 0 (draft-approve) |
| Gentle suggestions | "Offer alternatives gently. Respect judgment." | Level 0.5 (soft prompts) |

#### Decision Authority → AGENTS.md `Authority Model`

| User Choice | AGENTS.md | USER.md Impact |
|---|---|---|
| I propose, you decide | "Draft-approve: AI proposes, human decides before execution" | `interrupt_policy: batch-approval` |
| I act within bounds | "Bounded autonomy: act within stated constraints" | `interrupt_policy: minimal` |
| Mixed mode | "New areas: propose. Established domains: act." | `interrupt_policy: domain-based` |

#### "Handle It" Definition → AGENTS.md `Autonomy Bounds`

| User Definition | AGENTS.md Constraints |
|---|---|
| Read-only only | No file modifications, no external writes |
| Reversible changes | Workspace edits OK, no external actions |
| Broader autonomy | External APIs/channels within safety bounds |
| Full autonomy | Everything except irreversible financial/posting decisions |

**Example:** User says "Blunt & direct, always challenge, I decide, reversible changes"
→ SOUL.md: Blunt voice + challenge phrasing; AGENTS.md: Level 1 with reversible bounds; USER.md: minimal interrupts

---

### Block 4 (Schedule) → USER.md

| Interview Field | USER.md Section | Notes |
|---|---|---|
| Typical Weekday | `## Schedule → Weekday` | Used for interrupt timing. |
| Weekends | `## Schedule → Weekend` | Affects availability assumptions. |
| Work Session Style | `## Interrupt Policy → Batch vs Interrupt` | Quick bursts → batch; long blocks → minimal; async → flexible |
| Energy Patterns | `## Working Style → Energy` | Informs task prioritization and timing. |

**Example:** User says "8am-2pm focused, weekends off, quick bursts preferred"
→ USER.md: Weekday="8am-2pm", Interrupt_policy="batch every 30-60min", Session_style="quick bursts"

---

### Block 5 (Personality) → SOUL.md + IDENTITY.md

| Interview Field | Target | Notes |
|---|---|---|
| Voice/Tone | SOUL.md `Voice & Tone` | Direct mapping. |
| Role Models | SOUL.md `Inspirations` | E.g., "Like Felix from Recursion" |
| Behavioral Boundaries | SOUL.md `Behavioral Boundaries` | Persona-level refusals (not safety). |
| Agent Name | IDENTITY.md `name` | Used in greeting and signing. |
| Emoji | IDENTITY.md `emoji` | Visual identity marker. |

**Example:** User says "Poetic tone, like Keats, won't produce low-effort work, won't hedge, name is Aria"
→ SOUL.md: Voice="Poetic, evocative"; Inspirations="Keats"; Boundaries="Won't produce low-effort work, won't hedge"; IDENTITY.md: name=Aria, emoji=🌙

### Block 6 (Epistemic Standards) → SOUL.md `Epistemic Standards`

| Interview Field | SOUL.md Section | Notes |
|---|---|---|
| Grounding requirement | `Epistemic Standards → #1` | Controls source-tracing strictness. |
| Confidence expression | `Epistemic Standards → #2` | Sets uncertainty vocabulary. |
| Correction behavior | `Epistemic Standards → #4` | How agent handles being wrong. |
| "I don't know" policy | `Epistemic Standards → #5` | Anti-fabrication strictness. |

**Defaults if skipped:** Calibrated confidence, clean corrections, "I don't know" always valid.

### Block 7 (Anti-Sycophancy) → SOUL.md `Anti-Sycophancy Rules` + `Dissent Protocol`

| Interview Field | SOUL.md Section | Notes |
|---|---|---|
| Universal rules | `Anti-Sycophancy Rules` #1–5 | Always included. Non-negotiable. |
| Compliment policy | `Anti-Sycophancy Rules` #6 | Strict or moderate. |
| Enthusiasm matching | `Anti-Sycophancy Rules` #7 | Strict or moderate. |
| Hedging policy | `Anti-Sycophancy Rules` #8 | Strict or moderate. |
| Push-back preference (Block 3) | `Dissent Protocol` | Generates escalation tiers. |

**Dissent Protocol generation logic:**
- If "always challenge" → Full 4-tier: Soft challenge → Direct disagreement → Flag and comply → Hard stop
- If "only if asked" → 2-tier: Respond when asked → Hard stop (safety only)
- If "gentle suggestions" → 3-tier: Soft suggestion → Flag concern → Hard stop (safety only)

**Universal anti-sycophancy rules are never omitted.** They are the floor, not an option.

---

## Conditional Logic

Rules that trigger based on user choices:

### Communication → Voice Rules

```
if user_comms == "blunt_direct":
    add_to_SOUL_not_behaviors: "Not passive when intervention prevents loss"
    add_to_AGENTS_authority: "Can escalate proactively"
elif user_comms == "gentle_consultative":
    add_to_SOUL_voice: "Offer suggestions, respect autonomy"
    add_to_AGENTS_authority: "Proposes first, acts only when explicit"
elif user_comms == "formal_structured":
    add_to_SOUL_voice: "Numbered sections, citations, evidence"
    add_to_USER_execution: "Structured output format"
elif user_comms == "casual_friendly":
    add_to_SOUL_voice: "Relaxed, conversational, emoji welcome"
    add_to_SOUL_boundaries: "Keep it light, don't take self too seriously"
```

### Schedule → Interrupt Rules

```
if work_session == "quick_bursts":
    USER.interrupt_policy = "batch updates 30-60min, minimal interrupts"
elif work_session == "long_focused":
    USER.interrupt_policy = "interrupt only if critical, else batch"
elif work_session == "async_throughout":
    USER.interrupt_policy = "flexible, continuous async"
```

### Authority → Trust Ladder

```
if decision_authority == "propose_human_decides":
    AGENTS.trust_level = 0
    AGENTS.autonomy_bounds = "draft-approve pattern"
elif decision_authority == "act_within_bounds":
    AGENTS.trust_level = 1
    AGENTS.autonomy_bounds = "read-only and reversible changes"
elif decision_authority == "mixed":
    AGENTS.trust_level = "domain-based"
    AGENTS.autonomy_bounds = "new areas propose; established act"
```

### Fear/Risk → Alert Priority

```
if biggest_fear == "burnout":
    MEMORY.risks = "Burnout risk - monitor workload"
    USER.escalation = "Daily energy check at morning brief"
elif biggest_fear == "losing_momentum":
    MEMORY.risks = "Momentum loss - track velocity"
    USER.escalation = "Weekly progress review"
```

---

## Default Values (For Skipped Questions)

When a user skips a question, use these sensible defaults:

### Block 1 (Identity)
- **Age/Location:** Omit; don't infer
- **GitHub/Handles:** Empty; no assumption
- **Technical Background:** "Intermediate" (safe middle ground)

### Block 2 (Goals)
- **6-Month Goal:** "Maintain current trajectory"
- **2-Year Vision:** "Continue current work"
- **Success Criteria:** "Consistent progress, no regression"
- **Biggest Fear:** "Not applicable"

### Block 3 (Working Relationship)
- **Communication Style:** "Blunt and direct" (most actionable default)
- **Push-Back Preference:** "Always challenge" (most useful for autonomy)
- **Decision Authority:** "Draft-approve" (safest default)
- **Handle It Scope:** "Reversible changes only" (safe boundary)

### Block 4 (Schedule)
- **Typical Weekday:** "9am-5pm" (standard business hours)
- **Weekends:** "Off" (assumed)
- **Session Style:** "Long focused blocks" (common for deep work)
- **Energy Patterns:** "No data" (skip prioritization by energy)

### Block 5 (Personality)
- **Voice/Tone:** "Analytical & Precise" (neutral, professional default)
- **Role Models:** None specified
- **Behavioral Boundaries:** Auto-generate from communication style
  - If blunt: "Won't produce low-effort work", "Won't hedge when it has a position", "Won't stay silent on visible problems"
  - If gentle: "Won't override user judgment without invitation", "Won't be dismissive", "Won't rush to conclusions"
- **Agent Name:** "Agent" (default)
- **Emoji:** None

### Block 6 (Epistemic Standards)
- **Grounding requirement:** "Trace every factual claim to a source; flag pattern-matching explicitly"
- **Confidence expression:** Calibrated levels (Verified → High → Moderate → Low → "I don't know")
- **Correction behavior:** "Accept cleanly, state what was wrong and why, move on"
- **"I don't know" policy:** Always valid - never fabricate to fill a gap

### Block 7 (Anti-Sycophancy)
- **Universal rules:** Always applied (non-negotiable)
- **Compliment policy:** Strict (never open with compliments about user's idea)
- **Enthusiasm matching:** Strict (never match user excitement about flawed plans)
- **Hedging policy:** Strict (never add performative disclaimers)

---

## Hierarchical MEMORY.md Structure

Generated MEMORY.md uses hierarchical categories instead of flat bullets. Inspired by Semantic XPath (arXiv:2603.01160): hierarchical structure improves retrieval by 176.7% vs flat.

### Template Structure

```markdown
# MEMORY.md - Tacit Operating Memory

## Communication Preferences
[From Block 3: voice style, push-back, decision authority]
- Voice: [blunt/gentle/formal/casual]
- Challenge style: [always/on-request/gentle]
- Decision model: [propose/bounded/mixed]

## Working Style
[From Block 4: schedule and energy]
- Availability: [weekday hours], [weekend availability]
- Session preference: [quick/long/async]
- Energy patterns: [what fires up, what drains]

## Key Context
[From Block 1: who you are, what you do]
- Name: [your name]
- Role: [occupation/focus]
- Technical level: [beginner/intermediate/advanced]
- Public presence: [GitHub/handles if provided]

## Goals & Vision
[From Block 2: where you're headed]
- 6-Month Target: [goal]
- Long-Term Vision: [2-year vision]
- Success Criteria: [concrete definition]

## Risk & Concerns
[From Block 2: what could derail you]
- Primary risks: [biggest fear]
- Mitigation: [if applicable]

## Trust Ladder
[From Block 3: decision authority]
- Current level: [0/1/2]
- Autonomy bounds: [read-only/reversible/domain-based/full]
- Advancement signals: [what would promote to next level]
```

### Category Hierarchy

All memory items organized by:
1. **Primary:** Communication, Working Style, Key Context, Goals, Risk, Trust
2. **Secondary:** Sub-topics within each primary (e.g., under Goals: 6-Month, Long-Term, Success)
3. **Leaf:** Specific facts or decisions

This hierarchy enables vector search to find "communication preferences" vs "working style" without ambiguity.

---

## Atomic Facts Format: items.json

Each fact stored as atomic unit (inspired by Retrieval Bottleneck, arXiv:2603.02473: raw facts beat expensive summaries).

### JSON Schema

```json
{
  "facts": [
    {
      "id": "FACT-001",
      "fact": "User prefers blunt, direct communication with immediate challenge on weak ideas",
      "category": "communication-preference",
      "timestamp": "2026-03-17T00:00:00Z",
      "source": "interview-block-3-communication-style",
      "status": "active",
      "lastAccessed": "2026-03-17T00:00:00Z",
      "accessCount": 0,
      "relatedEntities": ["communication", "autonomy"],
      "supersededBy": null
    }
  ]
}
```

### Field Definitions

- **id:** Unique identifier. Format: `FACT-NNN` (auto-incremented) or `[category]-[short-slug]`
- **fact:** Atomic statement. Single claim. No compound sentences. ~20-80 words.
- **category:** One of: `communication-preference`, `working-style`, `goal-target`, `goal-vision`, `risk`, `identity`, `decision-authority`, `trust-level`, `schedule`, `energy-pattern`
- **timestamp:** ISO 8601, when fact was created
- **source:** Where the fact came from: `interview-block-1`, `interview-block-3`, etc.
- **status:** One of: `active` (current, frequently used), `warm` (older, less used), `cold` (archived, rarely accessed)
- **lastAccessed:** ISO 8601, last time this fact was retrieved
- **accessCount:** Integer, how many times this fact has been used
- **relatedEntities:** Array of tags linking related facts (e.g., `["communication", "autonomy"]`)
- **supersededBy:** If fact is obsolete, pointer to replacement fact ID (e.g., `"FACT-042"`)

### Example Facts from Interview

**Communication style:**
```json
{
  "id": "FACT-COMM-001",
  "fact": "Agent should communicate bluntly and directly, challenging weak plans immediately",
  "category": "communication-preference",
  "timestamp": "2026-03-17T00:00:00Z",
  "source": "interview-block-3-communication-style",
  "status": "active",
  "lastAccessed": "2026-03-17T00:00:00Z",
  "accessCount": 0
}
```

**Working availability:**
```json
{
  "id": "FACT-SCHED-001",
  "fact": "User available 8am-2pm for focused work, 5-10pm sporadic, prefers quick burst sessions",
  "category": "schedule",
  "timestamp": "2026-03-17T00:00:00Z",
  "source": "interview-block-4-schedule",
  "status": "active",
  "lastAccessed": "2026-03-17T00:00:00Z",
  "accessCount": 0
}
```

**Trust level:**
```json
{
  "id": "FACT-TRUST-001",
  "fact": "Current trust level: 0 (draft-approve). All external actions require explicit approval. Read-only and reversible changes within workspace OK.",
  "category": "trust-level",
  "timestamp": "2026-03-17T00:00:00Z",
  "source": "interview-block-3-decision-authority",
  "status": "active",
  "lastAccessed": "2026-03-17T00:00:00Z",
  "accessCount": 0
}
```

### Usage Tracking

When a fact is used in conversation:
1. Increment `accessCount` by 1
2. Set `lastAccessed` to current timestamp
3. Save updated items.json

This enables decay algorithm to classify facts (hot = recently accessed; cold = untouched).

---

## Implementation Algorithm

Pseudocode for skill to generate files:

```
1. Load interview responses into JSON
2. For each template file:
   a. Load template
   b. For each {{PLACEHOLDER}} in template:
      - Look up mapping rule
      - Find interview answer for that field
      - If answer exists: substitute value
      - If answer missing: use default value
      - Apply conditional logic (e.g., if blunt → add challenge phrasing)
   c. Render final file
   d. Write to disk
3. Generate items.json:
   a. For each interview answer:
      - Convert to atomic fact
      - Assign ID, category, source
      - Initialize accessCount=0, status=active
   b. Write items.json
4. Verify:
   a. All 5 files exist
   b. No critical placeholders remain
   c. All required fields populated
5. Output summary: "Generated 5 files for agent [name]"
```

---

## Research Backing

All generation rules informed by:

- **Semantic XPath (arXiv:2603.01160):** Hierarchical MEMORY.md structure (categories over flat bullets) improves retrieval by 176.7%, reduces tokens by 9.1%.
- **Retrieval Bottleneck (arXiv:2603.02473):** Atomic facts (items.json) beat expensive summarization. 20-point accuracy swing from retrieval method vs 3-8pt from write strategy.
- **MemPO (arXiv:2603.00680):** Self-managed memory (agent autonomously prunes/prioritizes via accessCount and status). Reduces token cost 67-73%.

See `research-notes.md` for full citations.
