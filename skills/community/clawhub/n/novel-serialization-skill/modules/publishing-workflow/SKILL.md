---
name: novel-publishing-workflow
description: >
  Manages Git-based publishing pipeline for serialized chapters including tagging, release notes, and automated verification.
license: GPL-3.0
novel_content_license: CC-BY-NC-SA-4.0
license_note: >
  Skill infrastructure is licensed under GNU General Public License v3.0 (GPL-3.0).
  Generated novel content is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
compatibility: Works with any LLM-backed coding agent (Claude Code, GitHub Copilot, Cursor, etc.)
metadata:
  author: community
  version: 1.4.0
  output_language_default: English
---

## Overview

Manages Git-based publishing pipeline for serialized chapters including tagging, release notes, and automated verification.

**Triggers:** "publish chapter", "create release", "tag version", "release novel", "publish release"

## Output Language

All generated novel content MUST be output in the language specified by the user via the `{{OUTPUT_LANGUAGE}}` variable.

- **Variable:** `{{OUTPUT_LANGUAGE}}`
- **Default:** `English`
- **Supported:** Any language the underlying LLM supports
- **Scope:** Applies to all generated narrative content, NOT to Skill infrastructure files
- **Infrastructure files** (SKILL.md, references/, module definitions) remain in English to ensure cross-tool compatibility

See [Section 0.3 of README FOR AI](../../README%20FOR%20AI.md#03-runtime-output-language-single-authority) for the authoritative declaration.

## Quick Start

1. Load the publishing-workflow sub-skill and review the reference templates in method-patterns-publishing.md
2. Run continuity-check module to verify all content is publication-ready
3. Update CHANGELOG.md with release entries following Keep a Changelog format
4. Create Git tag using semantic versioning format (v{major}.{minor}.{patch})
5. Generate release notes and push to repository

## Related Modules

This module is a peer of the following modules. It may hand off to them, but it does not own or invoke them (spec Section 5.1: each module is independently usable, with a single responsibility and no circular dependencies):

| Skill | Purpose | Path |
|-------|---------|------|
| novel-worldbuilding | Generates and maintains world-building documents for novel serialization projects. Covers magic systems, geography, politics, technology, history, and culture design. | [SKILL.md](../worldbuilding/SKILL.md) |
| novel-character-design | Generates and maintains character sheets including identity, psychology, arc, relationships, and voice profiles for novel characters. | [SKILL.md](../character-design/SKILL.md) |
| novel-chapter-writing | Drafts chapters following established world-building, character designs, and style guidelines while maintaining continuity with previous chapters. | [SKILL.md](../chapter-writing/SKILL.md) |
| novel-continuity-check | Verifies consistency across all chapters and state files, identifying plot holes, timeline errors, and character inconsistency. | [SKILL.md](../continuity-check/SKILL.md) |
| novel-continuity-tracker | Maintains persistent state files including timeline, character states, location states, and unresolved thread ledger for cross-session state management. | [SKILL.md](../continuity-tracker/SKILL.md) |

## References

### Primary Template

- [Method Patterns](../../references/method-patterns-publishing.md) - Master template file with structured patterns and guidelines

### Supporting Resources

- [Glossary](../../references/glossary.md) - Domain terminology and conventions
- [Prompts README](../../prompts/README.md) - How to use prompt templates
- [Implement Method Prompt](../../prompts/01-implement-method.md) - Core implementation prompt
- [Robustness Checks Prompt](../../prompts/02-robustness-checks.md) - Validation and quality-check prompt


## Examples

- [CHANGELOG.md](../../CHANGELOG.md) - Live example of Keep a Changelog format in this project. For release note, git tag, and chapter naming templates, see [method-patterns-publishing.md](../../references/method-patterns-publishing.md).

## Quick Reference: File Conventions

- **Naming:** Git tags follow format: v{major}.{minor}.{patch} or chapter-{number}. Release notes follow Keep a Changelog format.
- **Encoding:** UTF-8
- **Line endings:** LF (Unix-style)
- **Max file size:** 500 lines (split if exceeded)

## Verification Gates

Before considering this module's output complete, verify:

1. [ ] All chapter files follow naming convention (ch-{number}-{title}.md)
2. [ ] License headers present in all generated novel files
3. [ ] Continuity check passed before release
4. [ ] CHANGELOG.md updated with release entries
5. [ ] Git tag format is valid (semantic versioning)
6. [ ] Release notes include all notable changes
7. [ ] No broken internal links in published content

## Cross-References

| Resource | Description | Path |
|----------|-------------|------|
| novel-worldbuilding Method Patterns | World-building templates: magic systems, geography, politics, technology, history, culture | [method-patterns-worldbuilding.md](../../references/method-patterns-worldbuilding.md) |
| novel-character-design Method Patterns | Character design templates: identity, psychology, arc, relationships, voice profiles | [method-patterns-character.md](../../references/method-patterns-character.md) |
| novel-chapter-writing Method Patterns | Chapter writing templates: scene structure, POV rules, pacing, dialogue | [method-patterns-chapter.md](../../references/method-patterns-chapter.md) |
| novel-continuity-check Method Patterns | Continuity tracking templates: state files, timeline, thread ledger | [method-patterns-continuity.md](../../references/method-patterns-continuity.md) |
| novel-publishing-workflow Method Patterns | Publishing workflow templates: Git tags, release notes, verification | [method-patterns-publishing.md](../../references/method-patterns-publishing.md) |
| Glossary | Domain terminology and conventions used across all modules | [glossary.md](../../references/glossary.md) |
| Prompts README | How to use prompt templates in the prompts/ directory | [prompts/README.md](../../prompts/README.md) |
| Implement Method Prompt | Core implementation prompt for generating novel content | [01-implement-method.md](../../prompts/01-implement-method.md) |
| Robustness Checks Prompt | Validation and quality-check prompt for continuity and style | [02-robustness-checks.md](../../prompts/02-robustness-checks.md) |

## Constraints & Boundaries

### Hard Rules

- All generated content MUST be output in `{{OUTPUT_LANGUAGE}}` (default: English)
- Infrastructure and metadata remain in English
- SKILL.md is index + quick-reference ONLY - no code templates, no long-form methodology
- All code templates, structural patterns, and long-form methodology live in `references/`
- This module file MUST NOT exceed 500 lines
- Every generated novel file MUST carry the CC BY-NC-SA 4.0 license header block before any narrative content. Where a file also carries YAML frontmatter (mandatory for chapter files — see `references/method-patterns-publishing.md` Section 3), the ordering is: frontmatter at byte 0, then the CC license header, then the narrative.
- State must be persisted in structured files, NOT in conversation context
- Each module has a single responsibility; no circular dependencies between modules

### Scope Boundaries

Scope: Manages Git-based publishing pipeline for serialized chapters including tagging, release notes, and automated verification.

This module does NOT handle:
- novel-worldbuilding: Generates and maintains world-building documents for novel serialization projects. Covers magic systems, geography, politics, technology, history, and culture design.
- novel-character-design: Generates and maintains character sheets including identity, psychology, arc, relationships, and voice profiles for novel characters.
- novel-chapter-writing: Drafts chapters following established world-building, character designs, and style guidelines while maintaining continuity with previous chapters.
- novel-continuity-check: Verifies consistency across all chapters and state files, identifying plot holes, timeline errors, and character inconsistency.
- novel-continuity-tracker: Maintains persistent state files including timeline, character states, location states, and unresolved thread ledger for cross-session state management.
