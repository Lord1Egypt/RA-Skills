# Getting Started with Knowledge Base Publisher

## Overview

This guide walks you through publishing your first knowledge base article using the Knowledge Base Publisher skill.

## Prerequisites

- OpenClaw installed and running
- A source directory with at least one markdown file
- (Optional) A taxonomy file for consistent tagging

## Step 1: Prepare Your Content

Create a source directory with your raw markdown files:

```
source/
├── meeting-notes.md
├── project-updates.md
```

## Step 2: Run the Publisher

Invoke the skill with your source and target directories:

```
# Via OpenClaw agent
# Tell your agent to process the source directory
"Use knowledge-base-publisher to convert source/ into a structured knowledge base at published/"
```

## Step 3: Review the Output

Check the generated `index.json` for all published articles. Verify that metadata, tags, and cross-references look correct.

## Step 4: Iterate

If articles need adjustment:
1. Edit the source files
2. Re-run the publisher
3. Check `CHANGELOG.md` for version diffs

## Tags

- setup
- tutorial
- workflow
