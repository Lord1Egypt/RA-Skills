# MindStudio Generate Text Block Prompting Skill

A Claude skill for writing production-ready prompts for MindStudio's Generate Text block. Covers text output, JSON output, variable injection, conditional logic, dot-notation data access, and the MindStudio Sample Output field.

---

## What This Skill Does

When triggered, this skill interviews you about your workflow before writing a single line of prompt. It asks about your input variables (by exact name), what the block needs to do, what the output format should be, and what comes next in the workflow. The result is a paste-ready prompt that uses your real variable names — not generic placeholders.

For JSON output, the skill delivers two things every time: the prompt itself with a schema at the bottom, and a separate Sample Output block with realistic example data ready to paste into MindStudio's Sample Output field.

---

## When to Use It

Use this skill whenever you need to:

- Write a new prompt for a Generate Text block
- Choose between Text and JSON output for a block
- Structure a prompt that injects multiple variables
- Set up JSON output that feeds into a Run Workflow block
- Add conditional logic (`{{#if}}`) to a prompt
- Access nested JSON fields with dot notation in a downstream prompt
- Generate the Sample Output for MindStudio's JSON block setting

---

## What Gets Produced

**For text output prompts:**
- A structured prompt using XML tags to wrap variables
- Clear task, style, and format instructions
- Block settings recommendation (Output Behavior + Output Schema)

**For JSON output prompts:**
- A structured prompt with the JSON schema at the bottom
- A separate Sample Output with realistic fake data to paste into MindStudio
- Block settings recommendation
- Dot notation examples for accessing fields downstream

---

## File Structure

```
mindstudio-generate-text-block-prompting-skill/
├── SKILL.md        — Main skill instructions for Claude
├── README.md       — This file
├── EXAMPLES.md     — Full worked examples (text + JSON scenarios)
└── skill.json      — Skill metadata
```

---

## How the Interview Works

Before writing anything, Claude will ask:

- What should this block do, and where is it in the workflow?
- What variables are available, and what are their exact names?
- Are any variables JSON objects or arrays? What does the structure look like?
- Should the output display to the user or be saved to a variable?
- What is the output format — text or JSON?
- What comes after this block?

You only need to answer what applies to your situation. Claude uses your exact variable names throughout the generated prompt.

---

## Key Concepts

**Variable injection** — wrap any workflow variable in `{{double curly braces}}` to inject it into a prompt at runtime.

**XML tag wrapping** — wrap injected variables in descriptive XML tags (e.g., `<jobDescription>{{jobDescription}}</jobDescription>`) to separate data from instructions.

**Output Schema** — choosing JSON in MindStudio requires a Sample Output field with realistic example data, not type placeholders.

**Dot notation** — access fields inside JSON variables using `{{variableName.fieldName}}` or `{{variableName.arrayName.[0].fieldName}}`.

**Conditional logic** — use `{{#if variable}}...{{else}}...{{/if}}` to branch prompt behavior based on whether a variable has a value.
