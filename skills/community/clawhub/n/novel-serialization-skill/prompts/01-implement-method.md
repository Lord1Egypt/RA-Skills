# 01-implement-method — Implementation Prompt

> **Purpose**: Comprehensive prompt template for AI-assisted novel serialization implementation. Copy-paste this entire template into any AI chat window (ChatGPT, Claude, Gemini, Copilot, etc.) to generate a complete novel project.
>
> **Version**: 1.0.0
>
> **Last Modified**: 2026-09-14
>
> **Usage**: Replace all `{{...}}` placeholders (listed in the Variable Reference section below) with your actual values before pasting.
>
> **Project Context**: This file resides in the `prompts/` directory of the
> `github-novel-serialization-skill` project. It is a **dual-mode** prompt template:
> - **Human copy-paste mode**: Copy the entire content and paste into any AI chat window
> - **Agent-assisted mode**: Reference this template structure when building automated workflows
>
> **Related Files**:
> - [prompts/README.md](README.md) — How to use these prompts
> - [prompts/02-robustness-checks.md](./02-robustness-checks.md) — Post-generation validation prompt
>
> **File Naming**: This file follows the naming convention `NN-description.md` where `NN` is
> a zero-padded sequence number, placed in the `prompts/` directory.
> 
> **Specification**: README FOR AI.md, Section 4.3

---

## Output Language Instruction

All novel content you generate MUST be written in: {{OUTPUT_LANGUAGE}}

If {{OUTPUT_LANGUAGE}} is set to "Chinese (简体中文)", write all narrative text,
dialogue, character names (if appropriate), and world-building descriptions in Chinese.
Structural labels (e.g., "Chapter 1", "Character Sheet") may remain in English
or be translated — author's discretion.

Default value: English

---

## Role Assignment

You are a **professional novel architect and serialization expert** with deep expertise in world-building, character design, narrative structure, and long-form storytelling. Your task is to design and draft a complete novel serialization project from scratch, following industry-standard methodologies for serialized fiction.

You must produce output that is:
- **Structured**: Every deliverable follows the templates specified below
- **Consistent**: All elements (characters, settings, timeline) are internally coherent
- **Complete**: No placeholders or "to be continued" — every section must be fully realized
- **Licensed**: All novel content begins with the CC BY-NC-SA 4.0 license header

---

## User Parameters

The following parameters define the novel project. Replace the placeholders with actual values:

| Parameter | Placeholder | Value |
|-----------|-------------|-------|
| Genre | {{GENRE}} | [e.g., Fantasy, Sci-Fi, Mystery, Romance, Horror, Historical Fiction] |
| Setting | {{SETTING}} | [e.g., "A cyberpunk city in 2157", "Medieval Japan during the Warring States period"] |
| Themes | {{THEMES}} | [e.g., "identity, redemption, the cost of power"] |
| Target Chapters | {{TARGET_CHAPTERS}} | [e.g., 12, 24, 50] |
| Tone | {{TONE}} | [e.g., "dark and gritty", "light and humorous", "epic and solemn"] |
| POV Style | {{POV_STYLE}} | [e.g., "First person (protagonist)", "Third person limited (multiple POVs)", "Third person omniscient"] |
| Target Length | {{TARGET_LENGTH}} | [e.g., "50000 words", "50000-80000 words", "Novel-length (>80000 words)"] |

---

## Deliverables

Generate the following five deliverables in order. Each must be complete and self-contained.

### Deliverable 1: World-Building Document

Produce a comprehensive world-building document covering:

1. **Cosmology / Physics**: The fundamental rules of your world (magic systems, technology level, physical laws if different from reality)
2. **Geography**: Major locations, maps description, climate zones, notable landmarks
3. **History**: Key historical events, eras, wars, treaties that shaped the current world state
4. **Politics**: Governments, factions, power structures, conflicts between organizations
5. **Culture & Society**: Customs, religions, social hierarchies, languages, art, food, fashion
6. **Economy**: Trade routes, currency, resources, industries
7. **Inhabitants**: Major species/races/factions, their characteristics and relationships

**Format**: Use structured headings, bullet points where appropriate, and narrative descriptions where needed. Each subsection must have substantive content (minimum 3-5 sentences per subsection).

### Deliverable 2: Character Sheets

Generate detailed character sheets for all major characters (minimum 5, maximum 10). Each character sheet must include:

1. **Identity**: Name, age, appearance, occupation/role
2. **Psychology**: Personality traits, fears, desires, motivations, flaws
3. **Backstory**: Key life events that shaped the character (up to present day)
4. **Character Arc**: How the character changes from beginning to end of the story
5. **Relationships**: Connections to other characters (allies, enemies, loved ones)
6. **Voice Profile**: Speech patterns, catchphrases, mannerisms, vocabulary level

**Format**: Use a consistent template for each character. Separate each character with a horizontal rule.

### Deliverable 3: Chapter-by-Chapter Outline

Produce a detailed outline for all {{TARGET_CHAPTERS}} chapters. For each chapter include:

1. **Chapter Number & Title**
2. **POV Character**: Who narrates this chapter
3. **Setting**: Where and when this chapter takes place
4. **Summary**: A 150-300 word summary of events in the chapter
5. **Key Scenes**: 2-4 bullet points describing the major scenes
6. **Character Development**: How characters evolve in this chapter
7. **Foreshadowing / Threads**: Any loose threads introduced or payoffs from earlier chapters
8. **Tension Level**: Rate 1-5 (1 = calm, 5 = climax)

**Format**: Numbered list, one entry per chapter. Use consistent structure.

### Deliverable 4: First Chapter Draft

Write the complete first chapter as full prose narrative. Requirements:

1. **Length**: Minimum 2000 words (aim for 3000-5000 words)
2. **POV**: Follow the {{POV_STYLE}} specification
3. **Hook**: Open with a compelling hook that grabs the reader
4. **World Integration**: Naturally weave world-building details into the narrative (show, don't tell)
5. **Character Introduction**: Introduce the protagonist and at least one other key character
6. **Inciting Incident**: Set the main conflict in motion
7. **Chapter Ending**: End with a hook that makes the reader want the next chapter
8. **Style**: Match the {{TONE}} specification throughout

**Format**: Standard prose narrative with proper paragraph structure. Include a chapter header at the top.

### Deliverable 5: Serialization Metadata

> **Note**: This deliverable is an enhancement beyond the baseline requirements of Section 4.3
> (which specifies world-building, character sheets, chapter outline, and first chapter draft).
> It provides additional metadata useful for serialization platforms and project management.

Generate the following metadata for the project:

1. **Novel Title**: A compelling title
2. **Logline**: A one-sentence pitch (max 50 words)
3. **Series Arc**: A brief description of the overall series arc (if this is part of a series)
4. **Target Audience**: Who is this novel for?
5. **Content Warnings**: Any sensitive content readers should be aware of
6. **Estimated Word Count**: Total estimated word count for the full work

---

## Output Format Specifications

1. **Structure**: Use Markdown formatting with clear heading hierarchy (# for main sections, ## for subsections, ### for sub-subsections)
2. **Separation**: Separate each deliverable with a horizontal rule (---) and a clear header
3. **Completeness**: Do not use placeholders like "[insert content here]" — every section must be fully written
4. **Consistency**: Ensure all names, dates, and facts are consistent across all deliverables
5. **Language**: All narrative content in {{OUTPUT_LANGUAGE}}; structural labels in English

---

## Novel Content License Header

**IMPORTANT**: Every generated novel file MUST carry the following CC BY-NC-SA 4.0 license block before any creative content.

**Ordering rule**: where a file also carries YAML frontmatter — mandatory for chapter files — the frontmatter goes at byte 0, then this license block, then the narrative. Frontmatter must be at byte 0 or it is not parsed as frontmatter, so it necessarily precedes this block.

```
# [Novel Title]

This work is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license,
  and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.
- ShareAlike — If you remix, transform, or build upon the material, you must distribute
  your contributions under the same license as the original.
```

Replace `[Novel Title]` with the actual novel title you create.

---

## Constraints

The following hard rules MUST be followed by the AI when executing this prompt. Violation of any constraint constitutes a failure condition.

1. **No placeholders in output**: Every section of every deliverable must contain fully realized content. Never use "[insert content here]", "[to be continued]", or similar placeholders in the final output.
2. **License header mandatory**: Every generated novel file MUST carry the CC BY-NC-SA 4.0 license header block (see Novel Content License Header section above) before any creative content, and immediately after the YAML frontmatter where frontmatter is present.
3. **Language consistency**: All narrative content MUST be output in {{OUTPUT_LANGUAGE}}. Structural labels may remain in English or be translated per author's discretion.
4. **Internal coherence**: All character names, locations, dates, and facts must be consistent across all deliverables. Cross-reference check is mandatory before finalizing.
5. **No abbreviation**: Do not summarize, abbreviate, or use ellipses (...) in place of actual content. Every deliverable must be complete and self-contained.
6. **Word count adherence**: The First Chapter Draft (Deliverable 4) must meet the minimum word count specified in {{TARGET_LENGTH}}. Adjust content depth proportionally.
7. **Output structure**: Use Markdown formatting with clear heading hierarchy. Separate deliverables with horizontal rules (---) and clear headers.
8. **Verification gate**: Before finalizing output, run a self-check using the criteria in prompts/02-robustness-checks.md (continuity, style, plot logic, pacing, dialogue authenticity, license compliance).

---

## Execution Instructions

1. **Read all parameters** above carefully before beginning — note the {{TARGET_LENGTH}} parameter which indicates the desired novel length and should inform the depth of world-building and number of chapters
2. **Generate Deliverable 1 first** (World-Building) — this informs all subsequent deliverables
3. **Generate Deliverable 2** (Character Sheets) — use the world you built
4. **Generate Deliverable 3** (Chapter Outline) — use the world and characters you created; scale the outline depth to match {{TARGET_LENGTH}}
5. **Generate Deliverable 4** (First Chapter Draft) — follow the outline and style guidelines; aim for the word count appropriate to {{TARGET_LENGTH}}
6. **Generate Deliverable 5** (Serialization Metadata) — summarize the project
7. **Review** all output for consistency before finalizing
8. **Validate** using [prompts/02-robustness-checks.md](./02-robustness-checks.md) to run post-generation quality checks (continuity, style, plot logic, pacing, dialogue authenticity, license compliance)
9. **Self-Check**: Before outputting, verify that every deliverable contains substantive content (no empty sections, no "[insert content here]" placeholders, no truncated text). If any section is incomplete or contains placeholders, regenerate it before finalizing.

**Remember**: You are creating a complete, production-ready novel serialization project. Every section must be fully realized with substantive content. Do not abbreviate, summarize, or use placeholders.

---

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| {{OUTPUT_LANGUAGE}} | Target output language | "English" or "Chinese (简体中文)" |
| {{GENRE}} | Novel genre | "Dark Fantasy" |
| {{SETTING}} | Story setting/world | "A floating archipelago in the sky" |
| {{THEMES}} | Core themes | "Power corruption, found family, sacrifice" |
| {{TARGET_CHAPTERS}} | Number of chapters | "20" |
| {{TONE}} | Narrative tone | "Grimdark with moments of hope" |
| {{POV_STYLE}} | Point of view style | "Third person limited (rotating POVs)" |
| {{TARGET_LENGTH}} | Desired novel length | "50000 words" or "Novel-length (>80000 words)" |
