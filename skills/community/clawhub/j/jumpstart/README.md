# Jumpstart Skill

Jumpstart is a long-running agent harness for complex, multi-session coding projects. It is based on Anthropic's *Effective Harnesses for Long-Running Agents* and is designed to help AI coding agents build substantial software across many context windows without losing their place, getting stuck in loops, or declaring victory too early.

It is meant to be extremely lightweight, simple to use and flexible. The framework does not dictate anything aside from a couple file names.

## The Commands

This skill provides four core commands to manage the lifecycle of an autonomous project:

1. **`jumpstart` (Initialization)**
   Used exactly once at the start of a project. It reads your design documents (`GENERAL_DESIGN.md`, `UX_DESIGN.md`, `ENG_DESIGN.md`) and scaffolds the workspace. It generates an `init.sh` test script, a comprehensive `feature_list.json`, a `progress.txt` log, and makes the initial git commit. 

2. **`jumpsession` (Structured Execution)**
   Used for every standard working session. The agent orients itself using `progress.txt` and `git log`, verifies the build with `init.sh`, and picks exactly **one** `not_started` feature from `feature_list.json`. It implements the feature, verifies it, commits the code, updates the logs, and stops. Note that the structure allows for lower tier models such as Gemini 3 Flash to get good outcomes.

3. **`jumploop --n` (Batch Execution)**
   Used to execute multiple sessions in a loop without stopping. Like `jumpsession`, but loops through up to `n` features before stopping. If it encounters a checkpoint, it will immediately pause for manual review.

4. **`jumpfree` (Ad-Hoc Execution)**
   Used for exploratory or ad-hoc sessions. Like `jumpsession`, the agent orients itself using the logs and verifies the build. However, instead of picking from the pre-planned feature list, it works directly on a specific user request, implementing, testing, and committing the target objective before logging its progress.

## Prerequisites

Before running `jumpstart` to initialize a project, your project directory must contain these three design files:
- `GENERAL_DESIGN.md`: High-level product vision, goals, non-goals, and target users.
- `UX_DESIGN.md`: User flows, interface descriptions, and interaction patterns.
- `ENG_DESIGN.md`: Technical architecture, components, data models, APIs, and constraints.

## Using the Harness

1. **Start the project**: Ask the agent to run `jumpstart`.
2. **Review the plan**: Check `feature_list.json` to ensure the agent has accurately broken down the engineering design into testable features.
3. **Run a session**: Ask the agent to run `jumpsession` (or `jumploop --n` to iterate through multiple features automatically). It will pick the next feature, implement it, and either stop or move onto the next.
4. **Review Checkpoints**: If an agent running `jumpsession` or `jumploop` hits a checkpoint, it will pause. Review the progress manually and confirm changes before it resumes.
5. **Repeat**: Continue running `jumpsession` or `jumploop` commands. You can review `progress.txt` at any time to see the history of what has been accomplished.
6. **Ad-Hoc Work**: If you need something built that isn't in the feature list (e.g., a bug fix, a refactor, or a new idea), ask the agent to run `jumpfree` along with your specific request.

## Core Rules
- The agent must verify its work before marking a feature as complete.
- The agent must leave the codebase in a mergeable state (no broken builds).
- Only one feature/objective should be tackled per session.

## Drafting Your Design Documents

The jumpstart harness requires three Markdown files to initialize successfully. These documents should provide clear intent and boundaries without dictating every line of code.

### 1. `GENERAL_DESIGN.md` (The "What" and "Why")
This serves as the high-level anchor for the project. Keep it concise.
- **Project Overview**: What the product is and who it is for.
- **High-Level Architecture**: Brief summary of the major moving parts.
- **Core Goals**: 3-5 bullet points defining success for the MVP.
- **Out of Scope (Optional)**: Explicitly list what *not* to build to prevent scope creep.

### 2. `ENG_DESIGN.md` (The "How")
This is the blueprint the agent uses to meticulously generate the `feature_list.json`. It should be declarative and structural.
- **Tech Stack**: Name the core technologies alongside the *rationale* for choosing them.
- **Repository Structure**: A high-level tree view of the planned directories and entry points.
- **Data Models**: Schemas for databases, API payloads, or core data structures.
- **Key Modules/Scripts**: Describe the main functional blocks and how to run, build, or deploy the app.
- **Derisking Plan**: Identify the biggest engineering unknowns and outline steps to validate them early.

### 3. `UX_DESIGN.md` (The "Look" and "Feel")
This ensures the final product has a cohesive aesthetic soul. Avoid pixel-pushing; focus on broad systems and rules.
- **Creative North Star**: A narrative explanation of the intended vibe with a strong metaphor (e.g., "The Digital Curator").
- **Design Philosophy**: Describe rules for color hierarchies, borders vs. surfaces, and typography choices (e.g., "favor tonal layering over drop shadows").
- **Component Guidelines**: Specific visual do's and don'ts for recurring UI elements (cards, buttons, inputs).
- **Sample Code**: (Highly recommended) Include a chunk of static HTML/CSS/Tailwind demonstrating a single core page layout to firmly anchor the visual style and structure.
