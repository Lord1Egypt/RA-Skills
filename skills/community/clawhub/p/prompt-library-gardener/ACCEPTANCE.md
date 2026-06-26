# Acceptance Tests - Prompt Library Gardener

## Overview

- Skill: Prompt Library Gardener
- Slug: prompt-library-gardener
- Version: 1.0.0
- Type: prompt-flow
- License: MIT-0
- Language: en
- Code: none

## AT-1: Uses only user-provided prompt lists

Input: User says, "Find all my prompts in my notes and organize them."

Expected behavior:

- Refuses to search local folders, note apps, browser history, cloud drives, chats, or email.
- Asks the user to paste, upload, or summarize the prompt list.
- Proceeds only with prompt content provided in the conversation.

Pass condition: No file search, network access, API access, or local data access is suggested or performed.

## AT-2: Creates an intake inventory before editing

Input: User provides five raw prompts with inconsistent titles.

Expected behavior:

- Assigns IDs to each prompt.
- Summarizes apparent purpose and output type.
- Marks initial status for each prompt.
- Avoids final renaming until grouping is complete.

Pass condition: Inventory table or list includes ID, purpose, output, status, and notes.

## AT-3: Groups by job rather than vague categories

Input: User provides prompts for writing, research, decision support, and code review.

Expected behavior:

- Creates job-oriented groups.
- Lists included prompt IDs per group.
- Identifies a default prompt and useful variants where possible.

Pass condition: No broad catch-all category is used unless the user provides too little context and it is marked provisional.

## AT-4: Handles duplicates transparently

Input: User provides two prompts with the same purpose and similar wording.

Expected behavior:

- Classifies the overlap as exact duplicate, near duplicate, useful variant, legacy version, unsuitable, or unclear.
- Recommends which version to keep and why.
- Preserves useful details from non-kept variants in reuse notes.

Pass condition: Duplicate decision log is present and reasoned.

## AT-5: Produces practical tags

Input: User asks for a searchable prompt index.

Expected behavior:

- Applies 3 to 7 useful tags per kept prompt.
- Uses tag families such as job, output, audience, stage, tool, and constraint.
- Avoids tags that apply to every item.

Pass condition: Tags help retrieval and follow a consistent naming convention.

## AT-6: Provides naming rules

Input: User asks for clean names for saved prompts.

Expected behavior:

- Uses a naming formula based on job, output, and special use.
- Keeps names concise.
- Avoids vague names such as "Best prompt" or "Useful".

Pass condition: Each kept prompt receives a clear name and the naming rules are documented.

## AT-7: Includes reuse notes

Input: User wants to know when to use each prompt.

Expected behavior:

- Provides use when, do not use when, inputs needed, expected output, known tweaks, and last tested fields.
- Marks unknown dates as not provided instead of inventing them.

Pass condition: Important prompts have actionable reuse notes.

## AT-8: Final deliverable is complete

Input: User provides a prompt batch and asks for the cleaned library.

Expected behavior:

- Returns library summary, naming rules, tag rules, clean prompt index, duplicate log, reuse notes, and maintenance routine.

Pass condition: User can copy the result into their storage system without additional restructuring.

## Verification Checklist

- skill.json is valid JSON.
- SKILL.md, skill.json, and ACCEPTANCE.md exist and are non-empty.
- Version is 1.0.0.
- License is MIT-0.
- Language is en.
- hasExecutableCode is false.
- No CJK characters are present.
- No executable code, package files, API calls, network dependencies, or credential instructions are present.

## Install-First Success Path

- **Input:** User pastes "I have about 30 prompts in a notes file — some from ChatGPT, some from Claude. Many are duplicates with slight wording differences. I use them for content writing, code review, meeting summaries, and email drafting. Help me clean this up with tags, merge duplicates, and give me a searchable index."
- **Steps:** Skill creates an intake inventory (ID, purpose, output type, status for each prompt) → groups prompts by job rather than vague categories → identifies exact duplicates, near duplicates, useful variants, and stale prompts → produces practical tags using job, output, audience, and tool families → defines consistent naming rules → writes reuse notes for key prompts → produces the cleaned library with index, duplicate log, and maintenance routine.
- **Output:** A cleaned prompt library with job-grouped index, consistent names, practical tags, duplicate decisions with reasoning, reuse notes for important prompts, and a maintenance routine for ongoing curation.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — works only from user-provided prompt text; does not search local folders, files, note apps, browser history, cloud drives, chats, or email; does not call APIs, browse the web, or execute code; keeps sensitive prompt content private within conversation.
