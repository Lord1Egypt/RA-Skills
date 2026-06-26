# Heuristics — Object Categorization & Validation

Rules for classifying ontology Objects and ensuring graph integrity.

---

## Object Classification

### Belief vs Prediction

| Criterion | Belief | Prediction |
|-----------|--------|------------|
| **Falsifiable?** | Generally no | Yes — can be proven wrong |
| **Time horizon?** | Timeless or indefinite | Specific timeframe |
| **Evidence changes it?** | Slowly, with significant counter-evidence | Directly — outcome resolves it |
| **Format** | "X is true" / "I believe X" | "X will happen by Y" |

**Examples:**
- ✅ Belief: "AI will transform society" (directional, no specific timeline)
- ✅ Prediction: "AI agents will be mainstream by end of 2026" (testable, dated)
- ✅ Belief: "People are meaning-seeking creatures" (about human nature)
- ✅ Prediction: "Twitter will add agent integration within 6 months" (specific, falsifiable)

**Edge case:** "AI will cause job displacement" 
- As-is: Belief (vague, unfalsifiable)
- Better as Prediction: "50% of knowledge workers will use AI daily by 2027"

**Rule:** If you can imagine a specific date where you'd know if you were right or wrong, it's a Prediction.

---

### Goal vs Project vs Task

| Criterion | Goal | Project | Task |
|-----------|------|---------|------|
| **Nature** | Outcome | Effort | Action |
| **Question answered** | What do I want? | How will I get it? | What's the next step? |
| **Timeframe** | Months to years | Weeks to months | Hours to days |
| **Completion** | Achieved or not | Delivered or abandoned | Done or not done |
| **Scope** | Could have multiple projects | Has multiple tasks | Atomic |
| **Lives in** | ontology/5-goals.md | ontology/6-projects.md | Daily notes / task manager |

**Examples:**
- ✅ Goal: "Build distribution via Moltbot ecosystem"
- ✅ Project: "Ship personal-ontology skill" (serves the Goal)
- ✅ Task: "Write SKILL.md" (part of the Project)

**Edge cases:**
- "Launch newsletter" — Goal if it's the outcome you want; Project if it serves a larger Goal (like "Build audience")
- "Learn Spanish" — Goal if you want fluency; Project if it serves "Move to Spain" Goal

**Rule:** Goals are about *having* something. Projects are about *building* something. Tasks are about *doing* something.

---

### Core Self Components

| Component | Question | Changes | Example |
|-----------|----------|---------|---------|
| **Mission** | Why am I here? | Rarely (years) | "Help people find meaning" |
| **Values** | What matters most? | Slowly (major life events) | "Family first", "Intellectual honesty" |
| **Strengths** | What am I good at? | Moderately (skill development) | "Synthesizing ideas", "Clear writing" |

**Rule:** If it feels changeable month-to-month, it's probably not Core Self — it might be a Goal or current interest.

---

## Link Validation Rules

### Required Links

| Object Type | Must Link To | Link Type |
|-------------|--------------|-----------|
| Project | At least one Goal | `serves` |
| Goal | Core Self (mission, value, or strength) | `serves` |
| Prediction | Optionally a Belief | `supports` or `tests` |
| Belief | Nothing required | — |

### Orphan Detection

An Object is **orphaned** if:
- Project with no `serves → Goal` link
- Goal with no `serves → Core Self` link
- Task (in daily notes) mentioned 3+ times without Project assignment

**Agent action:** Surface orphans in weekly review. Ask user to link or archive.

### Contradiction Detection

A **contradiction** exists when:
- Two Beliefs make incompatible claims
- A Prediction contradicts a Belief
- A Goal conflicts with a stated Value
- Two Goals require mutually exclusive resource allocation

**Agent action:** Surface immediately. Present both sides. User resolves.

---

## Validation Checklist

Run periodically (weekly or on-demand):

### Structural Integrity
- [ ] Every Project has at least one `serves → Goal` link
- [ ] Every Goal has at least one `serves → Core Self` link
- [ ] No orphan Projects (linked nowhere)
- [ ] No orphan Goals (linked nowhere)

### Temporal Integrity
- [ ] All Predictions have timeframes
- [ ] No overdue Predictions without resolution
- [ ] Completed Projects marked with completion date
- [ ] Parked items have pause reason

### Content Integrity
- [ ] No duplicate Objects (same thing named differently)
- [ ] Beliefs are belief-shaped (not predictions)
- [ ] Predictions are prediction-shaped (not beliefs)
- [ ] Goals are outcomes, not activities

---

## Confidence Levels (for Bootstrap)

When extracting candidate Objects from text:

| Level | Confidence | Action |
|-------|------------|--------|
| **High** | Clear, explicit statement matching pattern | Queue for user review |
| **Medium** | Implicit or partial match | Note in candidates, ask for clarification |
| **Low** | Possible interpretation | Don't surface unless asked |

**Patterns by confidence:**

**High confidence:**
- "I believe..." / "I think that..." / "I'm convinced..."
- "I predict..." / "By [date]..." / "My bet is..."
- "My goal is..." / "I want to achieve..."
- "I'm working on [Project name]..."

**Medium confidence:**
- "It seems like..." / "Probably..."
- "I should..." / "I need to..."
- Bulleted lists of priorities or values

**Low confidence:**
- General discussion of topics
- Quotes from other sources
- Historical statements ("I used to think...")

---

## Migration Rules

### When to Upgrade an Object
- Task mentioned 5+ times → Consider promoting to Project
- Project that's really about an outcome → Promote to Goal
- Prediction that became timeless → Convert to Belief
- Goal achieved → Archive with learnings

### When to Downgrade an Object
- Goal too vague → Clarify or demote to aspiration
- Project too small → Demote to task
- Belief too specific → Convert to Prediction

### When to Archive
- Goal completed
- Prediction resolved (confirmed/disconfirmed)
- Project delivered or abandoned
- Belief no longer held

---

## Object Naming Conventions

- **Goals:** Verb-noun phrase ("Build distribution", "Publish book")
- **Projects:** Specific deliverable ("personal-ontology skill", "Newsletter Q1")
- **Beliefs:** Statement form ("AI will transform work")
- **Predictions:** Dated statement ("AI agents mainstream by 2026")

Keep names short. Details go in description.
