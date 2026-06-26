---
name: skill-creator
description: Create a new agent skill from scratch with guided, step-by-step assistance. Generates a complete SKILL.md package with frontmatter, workflow, examples, and cross-platform metadata. Use when you need to create a skill, build a skill, scaffold a new skill, write a SKILL.md, make an agent skill, author a skill template, start a new skill project, or turn an idea into a publishable skill for ClawHub, skills.sh, OpenClaw, Cursor, Codex, or Claude Code.
metadata: { "openclaw": { "emoji": "🛠️", "requires": { "bins": ["python3"] } } }
---

# Skill Creator

Create agent skills from scratch through guided conversation. Collects requirements, generates a directory skeleton, and walks you through filling each section until the skill is ready to test and publish.

## Quick Start

1. Describe what the skill should do in one sentence.
2. The creator walks you through requirements, structure, and content.
3. A complete skill directory is generated and ready for testing.

## When to Use This Skill

Use when someone wants to create a new skill or does not know where to start.

Typical triggers:

- "I want to make a skill that does X"
- "Help me create a new skill"
- "Turn this workflow into a skill"
- "Scaffold a skill for me"

## Example Prompts

- `I want to create a skill that helps me generate weekly reports from Jira data.`
- `Help me build a new skill from scratch — I have no idea where to start.`
- `Turn this workflow I just did into a reusable skill I can publish on ClawHub.`
- `Scaffold a skill for converting CSV files to charts.`
- `Create a skill template for me, I need something that audits Terraform configs.`

## When Not to Use

Do not use this skill for tasks that already have a dedicated tool:

- Testing or evaluating an existing skill: use `skill-test`
- Optimizing search visibility of an existing skill: use `skill-seo`
- Debugging runtime failures inside a skill
- General code review unrelated to skill authoring

## Workflow

Follow these five phases in order. Do not skip phases unless the user explicitly asks.

### Phase 1: Understand the Need

Ask the user these questions one or two at a time, not all at once:

1. What should this skill help the agent do? (one sentence)
2. What would a user say to trigger it? (2-3 realistic examples)
3. What does the skill produce when finished? (files, reports, code, actions)
4. Does the skill need external tools or APIs? (env vars, CLI binaries)

Conclude this phase when the purpose, triggers, outputs, and dependencies are clear.

### Phase 2: Plan the Structure

Based on the answers, decide which type of skill to create:

- **Instruction-only**: SKILL.md + references/ (most skills)
- **Script-backed**: adds scripts/ for deterministic or repetitive tasks
- **Asset-backed**: adds assets/ for templates, images, or boilerplate

Read [references/skill-anatomy.md](references/skill-anatomy.md) for the full structure spec.

### Phase 3: Generate the Skeleton

Run the scaffold script:

```sh
python3 {baseDir}/scripts/init_skill.py <skill-name> --path <output-dir>
```

For script-backed skills, add `--type script`. For asset-backed skills, add `--type asset`.

The script creates the directory, SKILL.md template with TODO placeholders, and resource folders. Verify the output before proceeding.

### Phase 4: Fill the Content

Guide the user through each section in priority order. Read [references/writing-guide.md](references/writing-guide.md) for writing rules and [references/examples.md](references/examples.md) for good/bad comparisons.

1. **Frontmatter** (most critical):
   - `name`: lowercase-hyphen, must match directory name
   - `description`: use the template from writing-guide.md; cover action, object, outcome, and "Use when" triggers
   - `metadata.openclaw`: emoji and requires
2. **Example Prompts**: at least 3, written in realistic user language
3. **Workflow**: numbered steps describing the skill's process
4. **Commands**: runnable examples using `{baseDir}` paths
5. **Definition of Done**: measurable completion criteria
6. **When Not to Use**: explicit boundaries to reduce false triggers

After each section, confirm with the user before moving on.

### Phase 5: Verify and Optimize

After the skill is complete, run the quality toolchain:

1. Run `skill-test` to evaluate quality (target score >= 85)
2. Run `skill-seo` to check discoverability
3. Fix issues flagged by either tool and re-evaluate

The skill is ready to publish when skill-test reports no critical or high findings.

## Assistant Responsibilities

When using this skill:

- Ask questions gradually; do not overwhelm the user with all questions at once
- Explain jargon when the user appears non-technical
- Generate the skeleton before asking the user to write content
- Show the user what was generated and explain what each file is for
- Write draft content for the user to review rather than asking them to write from scratch
- Preserve the user's original intent; do not expand scope unless asked
- Always run the scaffold script rather than creating files manually

## Notes and Constraints

- SKILL.md files should stay under 500 lines. Move heavy content to references/.
- The `name` field must be lowercase letters, digits, and hyphens only (1-64 chars).
- The `name` must match the directory name exactly.
- Use `{baseDir}` for all command paths to ensure portability.
- Do not duplicate logic from skill-test or skill-seo.
- All generated skills should be compatible with OpenClaw, Codex, Claude Code, and Cursor.
- If the target directory already exists, the scaffold script will error and refuse to overwrite. Rename or remove the existing directory first.

## Definition of Done

- The scaffold script has run and the directory exists.
- SKILL.md has valid frontmatter with name, description, and metadata.
- At least 3 example prompts are present.
- A Workflow section documents the skill's process.
- A Definition of Done section states measurable completion criteria.
- skill-test scores the new skill at 85 or above with no critical findings.

## Resources

- Skill structure and cross-platform spec: [references/skill-anatomy.md](references/skill-anatomy.md)
- Writing rules, templates, and anti-patterns: [references/writing-guide.md](references/writing-guide.md)
- Good/bad comparison examples: [references/examples.md](references/examples.md)

## Commands

```sh
# Generate a new instruction-only skill
python3 {baseDir}/scripts/init_skill.py my-skill --path /path/to/output

# Generate a script-backed skill
python3 {baseDir}/scripts/init_skill.py my-skill --path /path/to/output --type script

# Generate an asset-backed skill
python3 {baseDir}/scripts/init_skill.py my-skill --path /path/to/output --type asset
```
