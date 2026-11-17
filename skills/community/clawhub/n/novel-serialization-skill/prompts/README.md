# prompts/ — Usage Guide

> **Purpose**: This file is the usage guide for the prompt templates in this directory. It explains the dual-mode design, how to use each prompt, how to customize the output language, and how to combine prompts for complex workflows.
>
> **Authoritative Source**: For the authoritative declaration on the `{{OUTPUT_LANGUAGE}}` variable and all prompt design specifications, see [README FOR AI.md](../README%20FOR%20AI.md) Section 0.3 (Runtime Output Language), Section 4.1 (Design Philosophy), Section 4.2 (prompts/README.md specifications), Section 4.3 (01-implement-method.md) and Section 4.4 (02-robustness-checks.md).
>
> **License**: This file is part of the Skill infrastructure and is licensed under GNU General Public License v3.0 (GPL-3.0).

---

## Project Structure Context

This file resides in the `prompts/` directory of the project. The relevant directory layout is:

```
github-novel-serialization-skill/
└── prompts/
    ├── README.md                  ← You are here
    ├── 01-implement-method.md     ← Core implementation prompt
    └── 02-robustness-checks.md    ← Validation & quality-check prompt
```

> **Note**: This shows a simplified view of the `prompts/` directory. See Section 1 of [README FOR AI.md](../README%20FOR%20AI.md) for the full project structure.

---

## 1. What Are These Files?

The files in this `prompts/` directory are **standalone, self-contained prompt templates** designed for human use. They are NOT intended for agent auto-invocation.

Each file contains a complete prompt that you can:

1. Open in any text editor
2. Copy the entire content
3. Paste into ANY AI chat window (ChatGPT, Claude, Gemini, Copilot, etc.)
4. Get immediate, structured output

---

## 2. Dual-Mode Design

This project employs a **dual-mode** architecture for its prompt system:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Agent-Assisted** | These prompt files define methodologies that the Skill's internal modules (in `modules/`) can reference to orchestrate structured workflows; note that the prompt files themselves are NOT for direct agent auto-invocation (see Section 4.1 of README FOR AI.md for design philosophy) | Guided AI-assisted workflows where a human uses these prompts to direct an agent's output |
| **Human Copy-Paste** | These prompt files can be copied into any AI chat interface for manual use | Ad-hoc writing, exploration, learning |

**Key Principle**: These prompt files are deliberately written to be **tool-agnostic**. They work identically whether you paste them into ChatGPT, Claude, Gemini, or any other LLM interface. The prompts use clear role assignments, structured output specifications, and variable placeholders to ensure consistent results across platforms.

---

## 3. Available Prompts

| File | Purpose | When to Use |
|------|---------|-------------|
| `01-implement-method.md` | Core implementation prompt — accepts novel parameters (genre, setting, themes, target length), generates a complete world-building document, character sheets for all major characters, a chapter-by-chapter outline, and drafts the first chapter. Must include role assignment, structured output format, `{{OUTPUT_LANGUAGE}}` placeholder, variable placeholders, and a CC BY-NC-SA 4.0 license header. | Starting a new novel or major revision; when you need to generate foundational creative content |
| `02-robustness-checks.md` | Validation & quality-check prompt — runs multi-dimensional quality checks on drafted content: continuity consistency (character names, locations, timeline), style consistency (voice, tense, register), plot logic (causality, motivation, foreshadowing payoff), pacing analysis (scene-to-sequel ratio, tension curve), dialogue authenticity (voice differentiation per character), and license compliance (verifying CC BY-NC-SA 4.0 license header presence). Outputs a structured report with severity levels (Critical / Warning / Suggestion). | After drafting a chapter or world-building document; before publishing to ensure quality and consistency |

---

## 4. How to Use a Prompt

### Step 1: Choose the Right Prompt

- Use `01-implement-method.md` when you need to **create content** (world-building, characters, chapters)
- Use `02-robustness-checks.md` when you need to **review and improve** existing content

### Step 2: Customize Variables

Each prompt contains **variable placeholders** (marked with `{{VARIABLE_NAME}}`) that you should customize before pasting:

- `{{GENRE}}` — The genre of your novel (e.g., Fantasy, Sci-Fi, Romance)
- `{{SETTING}}` — The setting/world description
- `{{THEMES}}` — Core themes to explore
- `{{TARGET_CHAPTERS}}` — Target number of chapters
- `{{TONE}}` — Desired tone (e.g., dark, humorous, epic)
- `{{POV_STYLE}}` — Point of view style (e.g., first-person, third-person limited)
- `{{OUTPUT_LANGUAGE}}` — Language for generated content (see Section 5 below)

> **Note**: The source specification originally contained a typo (`SETTING}}` missing the `{{` prefix). This guide uses the corrected form `{{SETTING}}`.

### Step 3: Paste and Execute

1. Open the prompt file in a text editor
2. Replace all `{{VARIABLE}}` placeholders with your actual values
3. Copy the entire modified prompt
4. Paste it into your AI chat window
5. Review and iterate on the output

---

## 5. Customizing Output Language

### 5.1 The `{{OUTPUT_LANGUAGE}}` Variable

All prompt templates include an **Output Language Instruction** block that controls the language of generated novel content. This variable is governed by the **AUTHORITATIVE DECLARATION** in [README FOR AI.md Section 0.3](../README%20FOR%20AI.md) (Runtime Output Language (Single Authority)), which establishes `{{OUTPUT_LANGUAGE}}` as the single source of truth for output language across the entire Skill.

```
## Output Language Instruction

All novel content you generate MUST be written in: {{OUTPUT_LANGUAGE}}

If {{OUTPUT_LANGUAGE}} is set to "Chinese (简体中文)", write all narrative text,
dialogue, character names (if appropriate), and world-building descriptions in Chinese.
Structural labels (e.g., "Chapter 1", "Character Sheet") may remain in English
or be translated — author's discretion.

Default value: English
```

### 5.2 Supported Languages

- **Default**: `English`
- **Supported**: Any language the underlying LLM supports (e.g., `Chinese (简体中文)`, `Japanese (日本語)`, `Spanish (Español)`, etc.)

### 5.3 Scope

- The `{{OUTPUT_LANGUAGE}}` variable applies to **all generated narrative content** (chapters, character sheets, world-building documents)
- It does **NOT** apply to Skill infrastructure files (SKILL.md, references/, module definitions), which remain in English for cross-tool compatibility

### 5.4 How to Change the Language

Simply replace `{{OUTPUT_LANGUAGE}}` with your desired language name. For example:

- For Chinese: Set `{{OUTPUT_LANGUAGE}}` to `Chinese (简体中文)`
- For Japanese: Set `{{OUTPUT_LANGUAGE}}` to `Japanese (日本語)`
- For Spanish: Set `{{OUTPUT_LANGUAGE}}` to `Spanish (Español)`

---

## 6. Combining Prompts for Complex Workflows

For complex novel-writing projects, you can chain multiple prompts together. Here is a recommended workflow:

### Phase 1: Foundation

1. Run `01-implement-method.md` with your novel parameters to generate:
   - World-building document
   - Character sheets
   - Chapter outline

### Phase 2: Drafting

2. Use the output from Phase 1 as context for subsequent chapter drafts
3. Craft chapter-specific prompts (based on the structure and patterns in `01-implement-method.md`) to draft individual chapters, referencing the world-building and character documents from Phase 1

### Phase 3: Verification

4. Run `02-robustness-checks.md` on each drafted chapter to:
   - Check continuity consistency (character names, locations, timeline)
   - Verify style consistency (voice, tense, register)
   - Analyze plot logic and pacing
   - Confirm license compliance

### Phase 4: Iteration

5. Address any issues flagged by the robustness check
6. Redraft as needed and re-verify

### Example Workflow (Chinese Novel)

```
1. Set {{OUTPUT_LANGUAGE}} = "Chinese (简体中文)"
2. Run 01-implement-method.md with your novel parameters
3. Review and refine the generated world-building and character docs
4. Draft chapters one at a time, providing context from previous outputs
5. After each chapter, run 02-robustness-checks.md
6. Fix issues and re-draft
7. Repeat until complete
```

---

## 7. Prompt Template Structure

Each prompt file follows a consistent structure to ensure reliable output:

| Section | Purpose |
|---------|---------|
| **Role Assignment** | Defines the AI's persona (e.g., "You are a professional novel architect...") |
| **Output Language Instruction** | Sets the target language via `{{OUTPUT_LANGUAGE}}` |
| **Task Description** | Clearly states what the AI should do |
| **Input Parameters** | Variable placeholders for user customization |
| **Output Format** | Specifies the expected structure of the response |
| **Constraints** | Hard rules the AI must follow (e.g., license headers, continuity rules) |
| **Novel Content License Header** | Instructs the AI to include CC BY-NC-SA 4.0 license in generated content |

---

## 8. License Notice

- **This file and all prompt templates** are part of the Skill infrastructure, licensed under **GNU General Public License v3.0 (GPL-3.0)**.
- **Generated novel content** (chapters, character sheets, world-building documents) produced using these prompts is licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.
- Every generated novel file MUST carry the CC BY-NC-SA 4.0 license header block before any narrative content. Where a file also carries YAML frontmatter (mandatory for chapter files — see `references/method-patterns-publishing.md` Section 3), the ordering is: frontmatter at byte 0, then the CC license header, then the narrative. The exact header text is given in each prompt template.

---

## 9. Quick Reference

| Need | Use This Prompt |
|------|-----------------|
| Start a new novel project | `01-implement-method.md` |
| Review and improve existing content | `02-robustness-checks.md` |
| Change output language | Modify `{{OUTPUT_LANGUAGE}}` in any prompt |
| Full workflow (create + verify) | Run `01-implement-method.md` then `02-robustness-checks.md` |

---

*For detailed specifications on prompt design, integration, and the authoritative declaration on output language, see the [README FOR AI.md](../README%20FOR%20AI.md) seed file.*
