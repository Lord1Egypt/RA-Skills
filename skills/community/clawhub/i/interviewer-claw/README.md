# Interviewer Claw

A system-prompt skill for AI assistants that conducts rigorous, structured interviews to stress-test plans, designs, and ideas. It walks every branch of your decision tree using Socratic inquiry until every ambiguity is resolved, then produces a structured summary of all decisions, open items, and identified risks.

Works for software and non-software projects alike -- architecture designs, business proposals, product specs, construction plans, or any initiative that benefits from disciplined thinking before execution.

For software projects, integrates with [spec-kit](https://github.com/github/spec-kit) to generate spec-driven development artifacts directly from interview decisions.

## Usage

```
/interviewer-claw                Start a new interview from scratch
/interviewer-claw [topic]        Interview about a specific topic or idea
/interviewer-claw review         Review and refine an existing plan or spec-kit artifacts
/interviewer-claw speckit        Generate spec-kit artifacts from interview decisions
/interviewer-claw help           Show available functions and tips
```

You can also trigger it naturally:

- "Grill me on this design"
- "Stress-test my plan"
- "Poke holes in this"
- "Challenge my assumptions"
- "Help me think through this"

## How It Works

### Interview Phases

Every interview follows a structured progression:

| Phase | Name | Focus |
|-------|------|-------|
| 0 | Kick-off | Scope, stakeholders, one-sentence vision |
| 1 | Job Mapping | The "what" and "why" using Jobs-to-be-Done |
| 2 | Constraints | Boundaries, feasibility, triple constraint tradeoffs |
| 3 | Risk | Inversion/pre-mortem, Five Whys, blind-spot checks |
| 4 | Synthesis | Structured summary and user validation |

For software projects, Phase 2 goes deeper into design-level concerns: data model and entities, interfaces and contracts, user story decomposition with Given/When/Then acceptance criteria, error states, and test-first thinking.

### Interviewer Mindset

The skill operates with five complementary mindsets:

- **Curiosity** -- Genuine dialogue, not a checklist
- **Skepticism** -- Organizational norms treated as beliefs needing validation
- **Humility** -- Confident ignorance; never assumes understanding
- **Charity** -- Builds the strongest version of your position before probing weaknesses (Rapoport's Rules)
- **Inversion** -- Flips the problem: "What would guarantee failure?" (Munger)

### Key Behaviors

- Asks ONE question at a time, with a recommended answer you can accept, reject, or refine
- Never accepts vague answers -- "it depends" triggers deeper probing
- Tracks open branches and won't move on until each is resolved or explicitly parked
- Steelmans your position before critiquing it
- Summarizes decisions at the end of each phase

## Functions

### `start` (default)

Runs the full interview from scratch. Identifies the subject, executes all five phases in order, and validates completion criteria before finishing.

### `review`

Reads an existing plan, then conducts a targeted interview to find gaps and refine it. Uses Rapoport's Rules to steelman the plan first (paraphrase, identify agreement, mention learnings) before probing weaknesses. Prioritizes gaps in this order:

1. Undefined success criteria
2. Hidden assumptions
3. Missing stakeholders
4. Scope ambiguity
5. Unaddressed risks
6. Missing constraints

**Spec-kit aware:** If pointed at a spec-kit artifact tree (`specs/###-feature/`), reads all related artifacts (spec.md, plan.md, data-model.md, contracts/, tasks.md, constitution) and cross-references them for consistency, constitution compliance, coverage gaps, and traceability.

### `speckit`

For software projects. Transforms interview decisions into [spec-kit](https://github.com/github/spec-kit)-compatible artifacts:

| Artifact | Source |
|----------|--------|
| `memory/constitution.md` | Non-negotiable principles from Phase 2 |
| `spec.md` | User scenarios and requirements from Phase 1 + Phase 2 |
| `data-model.md` | Entities, relationships, state transitions from Phase 2 |
| `contracts/` | API surfaces and interface definitions from Phase 2 |
| `tasks.md` | Dependency-ordered, parallelizable task breakdown |
| `checklists/requirements.md` | Validation checklist from acceptance criteria |

Cross-validates all artifacts before writing: every user story traces to tasks, every entity appears in contracts, all acceptance criteria are testable, and constitution compliance passes.

### `help`

Displays usage syntax, available functions, phase descriptions, and tips.

## Spec-Kit Integration

This skill serves as the **discovery front door** to spec-kit's spec-driven development pipeline:

```
Interviewer Claw                          spec-kit
========================                  ====================
Phase 0: Kick-off          ──────>        /speckit.constitution
Phase 1: Job Mapping       ──────>        /speckit.specify
Phase 2: Constraints       ──────>        /speckit.plan
Phase 3: Risk              ──────>        /speckit.analyze
Phase 4: Synthesis         ──────>        All artifacts validated
         speckit function  ──────>        Ready for /speckit.implement
```

The interview ensures you've thought through the what and why before spec-kit handles the how. The `speckit` function bridges the gap by producing artifacts in the exact format spec-kit expects.

The `review` function can also read existing spec-kit artifacts and probe them for cross-artifact contradictions, constitution violations, missing traceability, and underspecified contracts.

## Project Structure

```
Interviewer-Claw/
  SKILL.md              # Main skill instructions (loaded as system prompt)
  references/
    techniques.md       # Questioning techniques (Socratic, Laddering, Inversion, etc.)
    speckit.md          # Spec-kit artifact templates and format reference
  README.md             # This file (for humans)
```

## Techniques

The skill draws on established frameworks from multiple disciplines:

| Technique | Origin | Used For |
|-----------|--------|----------|
| Jobs-to-be-Done | Christensen | Uncovering core motivation before solutions |
| Five Whys | Toyota/Lean | Reaching root causes behind requirements |
| Inversion / Pre-Mortem | Munger, Klein | Surfacing failure modes optimistic planning misses |
| Steelmanning / Rapoport's Rules | Dennett | Building strongest version of a position before critique |
| Laddering | Reynolds & Gutman | Connecting features to business values |
| Interdisciplinary Blind-Spot Check | Munger | Screening for cognitive biases and organizational failures |
| Triple Constraint | PMI | Forcing explicit scope/time/cost tradeoffs |

Full technique descriptions are in [`references/techniques.md`](references/techniques.md).

## Installation

The skill is a set of markdown files that can be loaded as system-prompt context by any AI assistant that supports file reading and multi-turn conversation. Adapt the integration method to your platform.

### Claude Code

Place the `Interviewer-Claw` folder in your Claude Code skills directory, or reference it from your project's `.claude/settings.json`.

### Claude.ai

1. Zip the skill folder (include `SKILL.md` and `references/`)
2. Open Claude.ai > Settings > Capabilities > Skills
3. Upload the zip file
4. Enable the skill

### OpenAI (Custom GPT or API)

1. Create a Custom GPT or API assistant.
2. Paste the contents of `SKILL.md` into the system prompt / instructions field.
3. Upload `references/techniques.md` and `references/speckit.md` as knowledge files (or inline their contents into the system prompt).
4. Enable file reading / code interpreter if available.

### Other Platforms (Gemini, open-source agents, etc.)

1. Concatenate `SKILL.md`, `references/techniques.md`, and `references/speckit.md` into a single system prompt, or load them as context files if the platform supports it.
2. Ensure the model has access to file-reading capabilities if you want artifact review (`review` function) or spec generation (`speckit` function).

## Tips for Best Results

- **Answer one question at a time.** The skill is designed for focused, sequential dialogue.
- **Say "park it"** to defer a question you're not ready to answer. It gets tracked.
- **Say "I don't know yet"** -- that's valid. The item is logged as an open question with its dependencies noted.
- **Use `review`** when you already have a plan document. It's faster than starting from scratch.
- **Use `speckit`** after a software interview to generate buildable artifacts.
- **Be specific.** The more concrete your answers, the faster you reach resolution.

## License

MIT
