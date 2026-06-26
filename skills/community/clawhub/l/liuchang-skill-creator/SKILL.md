---
version: "1.2.0"
name: skill-creator
description: Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like "create a skill", "author a skill", "tidy up a skill", "improve this skill", "review the skill", "clean up the skill", "audit the skill".
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend agent capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

---

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else the agent needs.

**Default assumption: The agent is already very smart.** Only add context it doesn't already have.

### Set Appropriate Degrees of Freedom

- **High freedom (text-based)**: Multiple approaches valid, decisions depend on context
- **Medium freedom (pseudocode/scripts)**: Preferred pattern exists, some variation acceptable
- **Low freedom (specific scripts)**: Operations are fragile, consistency critical

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
├── scripts/          - Executable code
├── references/       - Documentation to load as needed
└── assets/           - Files used in output
```

---

## Skill Creation Process

### Step 1: Understanding the Skill

Understand concrete examples of how the skill will be used. Ask:
- "What functionality should this skill support?"
- "Give me examples of how this skill would be used"
- "What would a user say that should trigger this skill?"

### Step 2: Planning Reusable Contents

Analyze each example to identify:
- **Scripts**: Same code being rewritten repeatedly?
- **References**: Documentation needed for context?
- **Assets**: Templates or files used in output?

### Step 3: Initialize the Skill

Run the init script:
```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets]
```

### Step 4: Edit the Skill

#### Write Frontmatter

```yaml
---
name: skill-name
description: Clear description of what the skill does AND when to trigger it. Include specific contexts, use cases, and examples. This is the PRIMARY triggering mechanism - put all "when to use" info here, not in the body.
---
```

**Description is for the model**: When the agent starts a session, it scans all skill descriptions to decide "is there a skill for this request?" So the description must clearly state:
- What the skill does
- Specific triggers/contexts for when to use it
- Concrete examples of user requests that should activate it

#### Write SKILL.md Body

Keep under 500 lines. Use references/ for detailed content.

### Step 5: Package the Skill

```bash
scripts/package_skill.py <path/to/skill-folder>
```

---

## 🎯 Advanced Features

### Gotchas Section (Highly Recommended)

The highest-signal content in any skill is a **Gotchas** section. Build this from common failure points the agent runs into.

```markdown
## Gotchas

- **File encoding**: Always use UTF-8, otherwise parsing fails
- **Large files**: Split files over 10MB before processing
- **API rate limits**: Add 1-second delay between requests
```

**Best practice**: Update gotchas over time as you encounter new failure points.

### Memory & Storing Data

Skills can include memory by storing data within them:

```markdown
## Memory

This skill stores data in `~/.my-skill/data.json`. On each run, the agent reads this file to understand previous context.
```

**Storage options**:
- Append-only log files (simple)
- JSON files (structured)
- SQLite database (complex queries)

**Important**: Store data in a stable location outside the skill directory. Use `${CLAUDE_PLUGIN_DATA}` if available - data in the skill directory may be deleted on upgrades.

### On Demand Hooks

Skills can include hooks that are only activated when called:

```markdown
## Hooks

When activated, this skill registers:
- `/careful`: Blocks dangerous operations (rm -rf, DROP TABLE)
- `/freeze`: Only allows edits in specific directories
```

Use these for opinionated behaviors you don't want always on, but are extremely useful sometimes.

### Setup Configuration

For skills requiring user-specific context, store configuration in a config file:

```markdown
## Setup

This skill requires configuration in `config.json`:
- `api_key`: Your API key
- `channel`: Slack channel for notifications

If config is missing, ask the user for required fields.
```

### Product Verification

For skills that need verification, include test patterns:

```markdown
## Verification

After execution, verify the output:
1. Check file exists: `ls -la output/`
2. Run validation script: `scripts/validate.py output/file.json`
3. Take a screenshot for visual confirmation
```

Consider techniques:
- Programmatic assertions on state
- Video recording of output
- Log file comparison with previous runs

---

## 📦 Distributing Skills

### Option 1: Check into Repository

For small teams, check skills into the repo (e.g., `./skills/` or `./.claude/skills`).

### Option 2: Plugin Marketplace

For larger teams, create an internal marketplace where users can install skills. Document how to submit and review skills.

### Measuring Skills

Track skill usage with a PreToolUse hook:

```python
# Log when skill is triggered
@hook("PreToolUse")
def log_skill_usage(agent, tool_name, input):
    if tool_name == "Skill":
        log(f"Skill used: {input['skill_name']}")
    return input
```

This helps identify:
- Popular skills vs underused ones
- Skills that need improvement
- Patterns in how skills are being used

---

## 📚 Progressive Disclosure Patterns

### Pattern 1: Reference Files

```markdown
# PDF Processing

## Quick Start
[basic example]

## Advanced Features
- **Form filling**: See [references/forms.md](forms.md)
- **API reference**: See [references/api.md](api.md)
```

### Pattern 2: Domain Organization

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Conditional Details

```markdown
## Editing Documents

For simple edits, modify XML directly.

**For tracked changes**: See [references/redlining.md](redlining.md)
```

---

## Common Mistakes to Avoid

1. **Don't state the obvious**: Agent already knows basics
2. **Don't put everything in SKILL.md**: Use references/ for details
3. **Don't over-railroad**: Give flexibility to adapt
4. **Don't skip gotchas**: Build from real failures
5. **Don't forget setup**: Ask for required config early

---

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| scripts/ | Deterministic code, repeatedly rewritten |
| references/ | Documentation, schemas, examples |
| assets/ | Templates, images, output files |
| gotchas | Common failure points |
| hooks | Conditional behaviors |
| memory | Persistent context across runs |
| config.json | User-specific settings |

---

## Iteration Workflow

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify what should be updated
4. Implement changes and test again

**Tip**: Most skills begin as a few lines and a single gotcha. They get better because people keep adding to them as the agent hits new edge cases.
