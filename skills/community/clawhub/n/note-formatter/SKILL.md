---
name: note-formatter
description: "Markdown note formatting and cleanup utility. Use when cleaning up raw notes, standardizing markdown structure, fixing heading hierarchies, or converting messy pasted text into clean, well-structured markdown documents."
metadata:
  openclaw:
    emoji: "📝"
---

# Note Formatter

A skill for cleaning up and formatting raw markdown notes into well-structured documents.

## What It Does

- Fixes heading hierarchy (ensures H1 → H2 → H3 order)
- Standardizes bullet list indentation
- Removes excessive blank lines (max 2 consecutive)
- Ensures consistent spacing around headings (blank line before/after)
- Formats code blocks with language hints when missing
- Wraps long lines at sensible widths

## When to Use

- You have raw notes from a meeting, call, or scribbled draft
- You need to standardize a collection of markdown files
- You're preparing notes for publication or sharing
- You want consistent formatting across a document set

## Prerequisites

- Read access to the markdown file(s)
- Write access to save formatted output

## Basic Steps

1. Read the source markdown file
2. Detect and fix heading hierarchy issues
3. Normalize list formatting and indentation
4. Clean up whitespace (excessive blank lines, trailing spaces)
5. Ensure code blocks have language identifiers
6. Write the cleaned content back to the file (or save as new file)
7. Report what was changed

## Example Prompt

"Format the notes in `meeting-notes.md` — fix the heading levels, clean up extra blank lines, and make sure all lists use consistent indentation."
