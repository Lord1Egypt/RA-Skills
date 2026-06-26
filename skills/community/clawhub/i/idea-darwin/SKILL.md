---
name: idea-darwin
version: 1.0.0
emoji: 🧬
homepage: https://github.com/warmskull/idea-darwin
description: |
  Idea Darwin Engine — an automated idea iteration system that evolves raw ideas through structured competition and selection. Imports ideas from ideas.md, structures them into scored cards, then runs iterative rounds of deepening, derivation, crossbreeding, critique, and validation to surface high-potential ideas. Use /idea-darwin to trigger. This skill should also trigger whenever the user mentions "run a round", "iterate ideas", "idea pool", "idea scoring", "idea status", "brainstorm iteration", "evolve my ideas", "rank my ideas", or "idea pipeline". Even if the user doesn't explicitly say /idea-darwin, use this skill whenever the task involves structuring ideas from a file, scoring and ranking ideas, or running any kind of systematic idea iteration or selection process.
---

# Idea Darwin Engine

A round-based idea iteration system that treats ideas as competing organisms — scoring, selecting, crossing, and evolving them through structured rounds to surface the strongest concepts.

The metaphor is Darwinian selection: ideas that score well survive and evolve; weak ideas get flagged for the user to decide on; crossbreeding produces novel offspring. This prevents the common failure mode of brainstorming where all ideas stay equally vague forever.

## Commands

| Command | Description |
|---|---|
| `/idea-darwin init` | Initialize: parse ideas.md, create directory structure, config, and initial cards (optional params below) |
| `/idea-darwin round` | Execute the next iteration round |
| `/idea-darwin round N` | Execute N consecutive rounds |
| `/idea-darwin status` | View idea pool status and rankings |
| `/idea-darwin dormant IDEA-XXXX` | Put a specific idea into dormancy |
| `/idea-darwin wake IDEA-XXXX` | Wake a dormant idea |
| `/idea-darwin` | No arguments: show brief status and suggest next step |

Arguments are extracted from `$ARGUMENTS`. If no arguments are provided, show current status and suggestions.

### init Optional Parameters

| Parameter | Description | Default |
|---|---|---|
| `--budget <N>` | Max ideas to process per round | `12` |
| `--actions <N>` | Max actions per idea per round | `2` |
| `--disruption <N>` | Introduce external stimulus every N rounds (disruption round) | `3` |

Example: `/idea-darwin init --budget 8 --actions 3 --disruption 5`

These parameters are written to config.yaml and can be manually edited later. Unspecified parameters use defaults.

## File Structure

The system maintains this structure in the working directory (created during initialization):

```
project/
├── ideas.md          # User's raw ideas (read-only — never modify this file)
├── config.yaml       # System configuration and state
├── stimuli.md        # External stimulus entries (user-editable, system read-only)
├── cards/            # Idea cards
│   ├── IDEA-0001.md
│   └── ...
├── rounds/           # Round reports
│   ├── round-000.md
│   └── ...
├── reports/          # Leaderboard and cluster reports
│   └── leaderboard.md
└── graph/            # Relationship graph
    └── relations.json
```

## Idea Numbering

- Format: `IDEA-XXXX` (4-digit zero-padded, starting from 0001)
- Globally unique — numbers are never recycled, even for dormant or removed ideas
- `config.yaml` tracks the next available number in `next_idea_id`
- Each idea card records lineage via `parent_ids` and `child_ids`

## Idea State Machine

```
seed → exploring → refining → crossing → validated → dormant
```

| State | Meaning | Available Actions |
|---|---|---|
| seed | Just entered the pool | Tagging, card generation, deepen, quick cross-validation |
| exploring | Exploration phase | Deepen, derive, critique, preliminary cross |
| refining | Polishing phase | Logic reinforcement, feasibility analysis, risk check |
| crossing | High-cross phase | Merge with complementary ideas, evaluate fusion quality |
| validated | Verified | Output MVP plan, generate execution roadmap |
| dormant | Hibernating | Passive participation in cross and similarity matching only |

State transitions are recommended by the system based on scores and action results, but the user always has final say.

## Scoring System

### 6 Scoring Dimensions (1–10 each)

| Dimension | Weight | Meaning |
|---|---|---|
| Novelty | 0.10 | Is there a genuine breakthrough, or just repetition? |
| Feasibility | 0.20 | Is this technically, resource-wise, and path-wise achievable? |
| Value | 0.20 | How much impact would this create if successful? |
| Logic | 0.20 | Is it internally consistent, with no obvious gaps? |
| CrossPotential | 0.10 | How likely is this to spark something new when combined with other ideas? |
| Verifiability | 0.20 | Can we design an experiment or minimum validation path? |

### Three-Layer Scoring Formula

The scoring is layered so that each layer captures a different strategic lens — Survival measures standalone quality, Development measures growth potential, and Priority blends both with recency and diversity bonuses to prevent the pool from stagnating.

```
Survival = 0.10×Novelty + 0.20×Feasibility + 0.20×Value
         + 0.20×Logic + 0.10×CrossPotential + 0.20×Verifiability

Development = 0.30×Novelty + 0.30×CrossPotential
            + 0.20×VariationPotential + 0.20×Freshness

Priority = 0.50×Survival + 0.30×Development
         + 0.10×NewIdeaBoost + 0.10×DiversityBonus
```

- **VariationPotential** (0–10): How many distinct directions can this idea still branch into. Decreases as more children are derived.
- **Freshness** (0–10): Has this idea changed recently? Decays when an idea goes unprocessed for several rounds.
- **NewIdeaBoost**: Newly pooled ideas get +2 for their first 2 rounds, then 0.
- **DiversityBonus**: Ideas belonging to underrepresented categories in the pool get +1–2.

When scoring, refer to the prompt templates in `references/prompts.md`.

## Initialization Flow

When the user runs `/idea-darwin init`:

1. **Locate ideas.md**
   - Check if ideas.md exists in the current directory
   - If not found, use `AskUserQuestion` to ask for the path

2. **Create directories and config**
   - Create cards/, rounds/, reports/, graph/
   - Generate config.yaml (merge user-provided optional params; use defaults for unspecified ones):

```yaml
source:
  ideas_file: "./ideas.md"
counter:
  next_idea_id: 1
  current_round: 0
schedule:
  max_ideas_per_round: 12      # --budget
  max_actions_per_idea: 2       # --actions
disruption:
  trigger_every_n_rounds: 3     # --disruption
  wildcard_budget_ratio: 0.10
```

   - Generate `stimuli.md` (external stimulus file in the project root) with an initial template and editing instructions

3. **Parse ideas.md**
   - Identify each independent idea (typically separated by ## headings)
   - **Do not modify ideas.md** — it is always read-only

4. **Generate a card for each idea**
   - Assign ID (starting from IDEA-0001)
   - Tag (topic / problem type / stage / style / resource tags)
   - Generate full card following `assets/card-template.md` format
   - Initial scoring (6 dimensions + 3-layer composite scores)
   - Write to cards/IDEA-XXXX.md

5. **Generate round-000.md report**
   - List all initial card summaries, scores, and suggested next steps
   - Write to rounds/round-000.md

6. **Present results to user**
   - Display a summary table of all cards (ID, title, score, suggested action)
   - Inform the user about `stimuli.md` and how to use it:
     > `stimuli.md` has been created in the project root. Every N rounds, the system randomly selects up to 5 enabled entries as external stimuli to break mental ruts.
     > You can edit this file anytime to add/modify/disable entries. Each entry follows this format:
     > ```
     > ## [Entry Title]
     > - status: enabled / disabled
     > - [Content description]
     > ```
   - Wait for user confirmation before entering the formal round cycle

## Round Execution Flow

When the user runs `/idea-darwin round`, execute these 9 steps strictly in order:

### Step 1: Import New Ideas
- **Every round starts by checking the default idea document**: read the file pointed to by `source.ideas_file` in config.yaml
- Compare the default ideas.md against existing cards to identify new additions
- For new ideas: tag → generate card → initial scoring
- New ideas are marked `stage: seed` and receive the NewIdeaBoost
- **This is a mandatory pre-step for every round** — the system must not loop only over existing cards while ignoring incremental additions to the source file

### Step 2: Update Relationship Graph
- Based on all cards' tags and content, compute inter-idea similarity
- Identify potential cross candidates (high similarity = neighbor-cross candidates; low similarity but complementary = distant-cross candidates)
- Update graph/relations.json

### Step 3: Global Score Refresh
- Recalculate the 6-dimension scores for every **active** idea (not dormant)
- Update Survival / Development / Priority
- Flag: high-potential (Priority > 7), stagnant (unchanged for 3+ rounds), low-potential (Priority < 3)

### Step 4: Budget Allocation
Distribute slots according to `max_ideas_per_round`:
- 25% for newly pooled ideas
- 30% for deepening high-priority ideas
- 20% for deriving from high-potential ideas
- 15% for cross experiments
- 10% for disruption / random exploration

Select ideas by Priority Score descending. Each idea gets at most `max_actions_per_idea` actions.

### Step 5: Decide Actions
For each selected idea, assign actions based on the state machine (see table above).
When the state machine is insufficient, use score-driven rules:
- `High Novelty + Low Verifiability` → deepen
- `High Novelty + High CrossPotential` → cross
- `High Value + Low Feasibility` → critique + refine
- `High Feasibility + Low Logic` → deepen
- `High duplication` → merge

### Step 6: Execute Actions
Process each selected idea in turn. Refer to `references/actions.md` for detailed execution specs, and `references/prompts.md` for prompt templates.

**Execution flow per idea:**
1. Read the full card
2. Follow the corresponding prompt template for the action type — think deeply
3. Produce structured output:
   - Updated card content
   - New derived ideas (auto-assign IDs, update parent_ids/child_ids on both sides)
   - Score changes
   - Discovered risks
   - Suggested next actions
4. Write the updated card file

Newly derived ideas also require full card generation and initial scoring.

### Step 7: Validate and Deduplicate
- Run **two-layer validation** on all newly produced ideas:
  - Layer 1 (Fatal flaw check): Logical contradiction? No real demand? Completely infeasible? Near-duplicate?
  - Layer 2 (Value judgment): Worth continuing? What next? Biggest risk?
- Validation failure → mark `validated: false`, lower priority, report to user
- **The user decides** whether to dormant or remove — the system only recommends
- Run similarity check across the entire pool and merge near-duplicates

### Step 8: Generate Round Report
Write to `rounds/round-XXX.md`, including:
- Ideas processed this round and actions executed
- Newly produced idea summaries
- Top 5 score changes (up/down)
- Ideas that failed validation (require user decision)
- Recommended priorities for next round
- If disruption round: which external stimuli were used, which innovation frameworks applied

### Step 8.5: Output Round Briefing

After all file updates are complete, **output a round briefing directly in the conversation** (not written to file) so the user can understand the full picture without opening any files. Format:

```
## Round N Briefing

### Actions Taken
| ID | Title | Action | Key Output |
|---|---|---|---|
| IDEA-XXXX | ... | deepen/derive/cross/critique/... | One-line summary |

### Card Changes
| ID | Title | Score Change | State Change | Notes |
|---|---|---|---|---|
| IDEA-XXXX | ... | Priority X.XX→X.XX | seed→exploring | Reason for change |

### New Ideas (Detail)

For each newly produced idea this round:

#### IDEA-XXXX: [Title]
- **Source**: [cross/derive/stimulus] from IDEA-XXXX + IDEA-XXXX
- **Core Question**: [one paragraph]
- **Key Insight**: [what's most valuable about this idea]
- **Initial Score**: Priority X.XX (Survival X.XX / Development X.XX)
- **Current Tension**: [biggest unresolved question]
- **Suggested Next Step**: [deepen/derive/cross/critique + specific direction]

### Current Rankings
| Rank | ID | Title | Priority | Stage |
|---|---|---|---|---|

### Next Round Preview
- [Suggested priority actions]
- [Whether a disruption round is coming soon]

### Decisions Needed
> List key decisions the user needs to make this round. Each item **must include the idea's full title** (not just the ID) along with context and suggested options.
> Examples:
> 1. **IDEA-0002 "Learn Coding Agent Tutorial Site" overlaps with IDEA-0004 "Progressive Unboxing Pedagogy"** — Merge or reposition? Suggestion: [...]
> 2. **IDEA-0006 "Auto-Diagnostic Thread" failed validation** — Dormant, pivot, or keep observing?
> 3. **IDEA-0003 "Thermal Management Ontology" downgraded** — Accept downgrade from ontology to structured Excel as first step?
>
> If no user decisions are needed this round, write "No decisions needed this round."
```

This briefing is the primary interface between the user and the system — keep it complete and readable. The "Decisions Needed" section is the most important interaction point: the system should clearly list decision items with recommendations, rather than leaving the user to discover issues from reports.

### Step 9: Save State
- Update all modified card files
- Increment `current_round` in config.yaml
- Update `next_idea_id`
- Update reports/leaderboard.md (Top 10 rankings)

## External Stimuli and Disruption Rounds

Every `trigger_every_n_rounds` rounds (default 3), external stimuli are introduced in a "disruption round." The purpose is to prevent the idea pool from converging on a local optimum by forcing fresh perspectives.

### External Stimulus File (stimuli.md)

`stimuli.md` lives in the project root. It is created during initialization and maintained by the user. Format:

```markdown
## Industry Trend: Embodied AI Accelerating to Production
- status: enabled
- Embodied AI moving from lab to production line in 2026, robot operating costs down 60%

## Tech Shift: Unified Multimodal Model Architecture
- status: enabled
- Vision, language, and code unified into single models, API paradigm changing

## Contrarian View: SaaS Is Dead
- status: disabled
- Open-source + self-hosted deployments replacing traditional SaaS subscriptions
```

- Each entry: `##` heading + `status` field + content description
- `enabled` = participates in random selection; `disabled` = skipped
- Users can add, edit, or toggle entries at any time
- The system only reads this file — never writes to it

### Disruption Round Mechanics

1. **Shuffle priorities**: Give low-priority but novel ideas a chance to surface
2. **Distant cross**: Force crossbreeding between ideas with non-overlapping tags
3. **External stimuli**: Randomly select up to 5 enabled entries from stimuli.md
4. **Assumption reversal**: For top-scoring ideas, ask "What if the core assumption is wrong?"
5. **Innovation frameworks**: Apply SCAMPER / First Principles / Analogical Transfer / Constraint Reversal / Extreme User Perspective

Each round also reserves `wildcard_budget_ratio` (default 10%) of slots for non-optimal-path exploration.

## Dormancy and Wake

### `/idea-darwin dormant IDEA-XXXX`
1. Read the card, set stage to `dormant`
2. Record reason and round number in the card's "Dormancy Log"
3. The idea will no longer be selected for deepen/derive, but still participates in cross and similarity matching

### `/idea-darwin wake IDEA-XXXX`
1. Read the card, restore stage to the pre-dormancy state (inferred from history, typically `exploring`)
2. Update the "Dormancy Log"

The system **never** auto-dormants any idea. Only the user can make that call.

## `/idea-darwin status`

Read config.yaml and all cards, then output:
- Current round number
- Total ideas in pool (broken down by state)
- Top 10 rankings (by Priority Score descending)
- What was processed in the most recent round
- Suggested next steps

## Key Constraints

1. **ideas.md is read-only**: Never modify the user's ideas.md
2. **IDs never recycle**: Numbers are never reused under any circumstance
3. **Branch limit**: Each idea can derive at most 2–3 children per round
4. **Per-round dedup**: Similarity check is mandatory before a round concludes
5. **User control**: The system never auto-dormants or removes ideas — only recommends
6. **Structured output**: Every action must produce structured results
7. **Consistent card format**: All cards strictly follow `assets/card-template.md`
8. **Traceable reports**: Every round report must contain a complete operation log

## Reference Files

- `references/actions.md`: Detailed specs and use cases for each standard action
- `references/prompts.md`: Prompt templates for each action
- `assets/card-template.md`: Card file template
