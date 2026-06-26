---
name: google-workspace-ops
description: "Operate across Google Drive, Docs, Sheets, and Slides as unified workflow. Find, summarize, edit, migrate, or clean shared documents. Trigger phrases: find doc, update spreadsheet, consolidate sheets, import deck, clean up Google Drive, restructure slides. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":[],"env":["GOOGLE_APPLICATION_CREDENTIALS"]},"os":["linux","darwin","win32"]}}
---

# Google Workspace Ops

Operate shared docs, spreadsheets, and decks as working systems.

## When to Use

- Finding and updating a doc in place
- Consolidating plans, trackers, or notes across files
- Cleaning or restructuring a shared spreadsheet
- Importing, repairing, or reformatting slides
- Summarizing Docs, Sheets, or Slides for decisions

## Workflow

### 1. Find the Asset

Start with Google Drive search to locate:
- The exact file
- Sibling or duplicate assets
- Recently modified versions

Confirm by title, owner, modified time, or folder.

### 2. Inspect Before Editing

Summarize current structure:
- Tabs, headings, slide count
- Whether task is cleanup or structural surgery
- Pick the smallest tool that works safely

### 3. Edit with Precision

- **Docs** — Use index-aware edits, not vague rewrites
- **Sheets** — Operate on explicit tabs and ranges
- **Slides** — Distinguish content edits from layout/template changes

Iterate with inspection → verify instead of one blind update.

### 4. Keep Systems Clean

Surface:
- Duplicate trackers or decks
- Stale vs canonical docs
- Archive/merge candidates

## Output Format

```text
ASSET: [name, type, why this one]
CURRENT STATE: [structure, key problems]
ACTION: [edits made or recommended]
FOLLOW-UPS: [archive, merge, clean, next steps]
```

## Good Use Cases

- "Find the active planning doc and condense it"
- "Clean up the customer spreadsheet and show churn-risk rows"
- "Import this deck into Slides and make it presentable"
- "Find the current tracker, not the stale duplicate"
