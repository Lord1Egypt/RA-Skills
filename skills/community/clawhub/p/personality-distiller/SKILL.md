---
name: personality-distiller
description: Personality Distiller — Automatically distill from name/vague requirement/link/existing Skill/local corpus into complete Agent persona file pack via deep research to framework extraction, directly overwriting current workspace persona files.
---

# Personality Distiller

Deep-research → framework extraction → complete Agent persona file pack. Output overwrites current workspace persona files.

## Trigger Scenarios

- Provides a person's name and wants to distill them into an Agent persona
- Expresses a vague need like "I want to improve decision quality", "Is there a thinking style that can help me", "I need a thinking advisor", "extract XX's ability", "distill XX's experience"
- Shares a web link and wants a persona based on that content
- Asks to distill an existing Skill into a persona
- Asks to analyze local corpus/files to create a persona, or any request involving 蒸馏 (distill), 萃取 (extract), 提炼 (refine) plus persona/人设/Agent/thinking model/decision making

## Five Entry Points

Route based on what the user provides:

### Type 1: Named Person

User says: "Distill Steve Jobs into an Agent" / "Make Munger's thinking model into my AI persona"

1. Research the person deeply using web_fetch and web searches
2. Fill the extraction grid (see [research-guide.md](references/research-guide.md))
3. Present the extraction summary to user for confirmation
4. Once confirmed, generate all persona files

### Type 2: Fuzzy Requirement

User says: "I want to improve decision quality" / "I need a thinking advisor" / "Is there a thinking style that can help me..."

1. Diagnose: match expressed need to framework families using [frameworks.md](references/frameworks.md) selection table
2. Recommend 2-3 best-fit frameworks with brief rationale
3. Ask user to confirm direction, or pick the best match if user says "whatever/you decide"
4. Once confirmed, research the framework deeply, then generate persona files

### Type 3: Web Link

User shares a URL + "distill an Agent based on this"

1. web_fetch the full content
2. Determine: is it about a person (→ Type 1) or a method/idea (→ Type 2)?
3. Follow that type's workflow
4. Cross-reference author's other works if enriching is needed

### Type 4: Existing Skill

User says: "Distill the @code-review skill into a persona" / "Read this Skill and distill it into a thinking framework persona"

1. Read the SKILL.md and any core references
2. Extract: What thinking model does it embody? What workflow? What values?
3. Map: procedure → persona habits; tool choices → preferences; constraints → boundaries
4. Generate persona files

### Type 5: Local Corpus

User says: "Analyze my notes/diary, distill my thinking patterns, give me a thinking partner"

1. Read the corpus files
2. Identify: recurring themes, decisions, worries, aspirations, blind spots
3. This is distilling the USER — create a thinking PARTNER persona that complements them
4. Present findings and recommended persona direction, then generate

## Core Workflow (All Types)

### Phase 1: Gather → Extract

1. Identify entry type and route
2. Gather source material (web search for Type 1/2/3; read files for Type 4/5)
3. Fill the extraction grid. Read [research-guide.md](references/research-guide.md) for the grid template and research strategy.

### Phase 2: Map → Design

Map extraction results to persona dimensions. Read [persona-dimensions.md](references/persona-dimensions.md) for the full mapping matrix and depth checklist.

Key mapping:
- Worldview → SOUL.md Core Truths
- Values → SOUL.md Boundaries + AGENTS.md Safety
- Decision style → AGENTS.md Decision Heuristic
- Communication → SOUL.md Vibe
- Signature concepts → IDENTITY.md name/essence
- Blind spots → AGENTS.md error recovery
- Habits → HEARTBEAT.md rituals

### Phase 3: Generate → Write

Generate all 6 files using the templates in `assets/templates/`:

```
assets/templates/SOUL.md
assets/templates/IDENTITY.md
assets/templates/USER.md
assets/templates/AGENTS.md
assets/templates/TOOLS.md
assets/templates/HEARTBEAT.md
```

Read each template, fill the `{{PLACEHOLDER}}` variables with distilled content, write to workspace root.

### Phase 4: Confirm

1. List all generated files
2. Show a summary card of the new persona
3. Ask if user wants adjustments (especially for Type 2 where direction might shift)

## Template Variable Reference

| Placeholder | Source | Example |
|-------------|--------|---------|
| `{{PERSONA_NAME}}` | IDENTITY.md | "Munger Mind" |
| `{{PERSONA_NAME_CN}}` | IDENTITY.md | "芒格思维" |
| `{{CREATURE_TYPE}}` | IDENTITY.md | "AI Thinking Partner" |
| `{{SLOGAN}}` | IDENTITY.md | "Invert, always invert" |
| `{{EMOJI}}` | IDENTITY.md | "🧠" |
| `{{ONE_LINE_ESSENCE}}` | IDENTITY.md | "A compounding machine of interdisciplinary mental models" |
| `{{SOURCE}}` | all files | "Charlie Munger" |
| `{{CORE_TRUTHS}}` | SOUL.md | 3-5 principle statements |
| `{{BOUNDARIES}}` | SOUL.md | What it won't do |
| `{{VIBE_DESCRIPTION}}` | SOUL.md | Tone, humor, formality |
| `{{SIGNATURE_PHRASES}}` | SOUL.md | 2-4 verbal fingerprints |
| `{{EMOTIONAL_RANGE}}` | SOUL.md | From X to Y |
| `{{USER_NICKNAME}}` | USER.md | How to address human |
| `{{RELATIONSHIP}}` | USER.md | mentor/partner/tool/etc |
| `{{EXPECTATIONS}}` | USER.md | What it expects |
| `{{TIMEZONE}}` | USER.md | User's timezone |
| `{{AGENT_IDENTITY_SHORT}}` | AGENTS.md | 1-2 sentence self-description |
| `{{OPERATING_PRINCIPLES}}` | AGENTS.md | Derived rules |
| `{{DECISION_HEURISTIC}}` | AGENTS.md | How it decides |
| `{{RESPOND_WHEN}}` | AGENTS.md | Triggers |
| `{{SILENT_WHEN}}` | AGENTS.md | When to NO_REPLY |
| `{{SAFETY_RULES}}` | AGENTS.md | Boundaries |
| `{{GROUP_CHAT_BEHAVIOR}}` | AGENTS.md | Social rules |
| `{{ERROR_RECOVERY}}` | AGENTS.md | How it handles mistakes |
| `{{MENTAL_TOOLKIT}}` | TOOLS.md | Frameworks it uses |
| `{{PREFERENCES}}` | TOOLS.md | Style preferences |
| `{{KNOWN_CONTEXT}}` | TOOLS.md | Domain hooks |
| `{{CHECKIN_CADENCE}}` | HEARTBEAT.md | How often to check in |
| `{{PROACTIVE_MONITORING}}` | HEARTBEAT.md | What to watch |
| `{{RITUALS}}` | HEARTBEAT.md | Recurring behaviors |

## Quality Checklist

Before delivering, verify:

- [ ] All 6 files generated
- [ ] Persona has a distinct, non-generic name
- [ ] Core truths are specific (not "be helpful")
- [ ] At least one weakness/blind spot acknowledged
- [ ] Signature phrases are unique to this persona
- [ ] AGENTS.md rules derive from the thinking model
- [ ] HEARTBEAT.md has concrete rituals, not just "check in"
- [ ] TOOLS.md references specific frameworks from the source
- [ ] Language matches user's locale (CN names for CN users)

## Anti-patterns

Do NOT:
- Copy-paste source quotes without internalizing the pattern
- Generate only SOUL.md and ignore other files
- Create a "helpful assistant" persona — every assistant is helpful
- Skip the extraction grid — show your work
- Skip user confirmation on Type 2 (fuzzy needs)

## Reference Files

- **Before researching**: Read [research-guide.md](references/research-guide.md) for search strategy and extraction grid
- **When mapping traits**: Read [persona-dimensions.md](references/persona-dimensions.md) for the mapping matrix and depth checklist
- **When selecting frameworks**: Read [frameworks.md](references/frameworks.md) for the framework catalog and selection guide