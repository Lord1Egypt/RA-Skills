---
name: personal-wiki
description: Uses wikmd to manage a personal, local wiki of useful information. Wiki can be hosted on HTTP for manual browsing and review. Proactively consult the wiki when the user mentions projects, research topics, decisions, or any topic that might be documented. Regularly review and update the wiki with new insights, research findings, and contextual information.
homepage:
metadata:
  openclaw:
    emoji: 📚
    requires:
      env:
        - PERSONAL_WIKI_ROOT
---

# Personal Wiki

Manage a personal wiki using [Wikmd](https://github.com/Linbreux/wikmd), a file-based wiki that renders Markdown files with a clean web interface.

## When to Use

### Active Triggers — Use immediately when:
- "Create a page about..."
- "Add to my wiki"
- "Research X and create a page about it"
- "Update my wiki with..."

### Proactive Triggers — Consult the wiki when:
- User mentions projects, work, or ongoing tasks
- User discusses research, learning, or exploring new topics
- User references decisions, plans, or goals
- User mentions people, places, or organizations repeatedly
- User asks questions about topics that might be documented
- Before making recommendations — check if wiki has relevant context
- When synthesizing information — see if wiki has related pages

### Maintenance Triggers — Update the wiki when:
- After completing research or gathering new information
- When learning something worth remembering
- After making decisions worth documenting
- When encountering useful resources, tools, or references
- When patterns or insights emerge from conversations
- During heartbeat checks — review for outdated or incomplete pages

## Installation

### Prerequisites

1. **Python 3** and **pip** installed
2. **Git** for version control

### Install Wikmd

```bash
pip install wikmd
```

Or via pipx (recommended):
```bash
pipx install wikmd
```

### Setup Wiki Directory

1. Create your wiki root directory:
```bash
mkdir -p ~/personal-wiki/wiki
cd ~/personal-wiki
git init
```

2. Create a basic configuration file (`wiki_config.yaml`) in your wiki root:
```yaml
wiki_directory: "./wiki"
homepage: "homepage"
homepage_title: "My Wiki"
host: "127.0.0.1"
port: 5000
authentication: false
hide_folder_content: false

**note: if you set the host to 0.0.0.0 you can access the wiki on your network - but be cautious about this opening up your data**

```

3. Run the wiki:
```bash
wikmd --config wiki_config.yaml
```

Visit http://localhost:5000 to view your wiki.

## Configuration

### Environment Variable

This skill requires the `PERSONAL_WIKI_ROOT` environment variable to be set:

```bash
export PERSONAL_WIKI_ROOT="<PATH>/personal-wiki"
```

Set this via OpenClaw config:
```bash
openclaw config set skills.entries.personal-wiki.env.PERSONAL_WIKI_ROOT "<PATH>/personal-wiki"
```

### Wiki Directory Structure

This is an example of how you can structure the wiki:

```
PERSONAL_WIKI_ROOT/
├── wiki/                    # Markdown files go here
│   ├── homepage.md         # Main landing page
│   ├── projects/
│   │   └── my-project.md
│   ├── research/
│   │   └── topic-notes.md
│   ├── people/
│   │   └── contacts.md
│   ├── decisions/
│   │   └── architecture-choices.md
│   └── resources/
│       └── useful-links.md
├── wiki_config.yaml        # Wikmd configuration
└── .git/                   # Version control
```

## Working with the Wiki

### Reading from the Wiki

**Always check the wiki before:**
1. Making recommendations — the wiki may have preferences or constraints documented
2. Answering questions — the user may have already researched this
3. Planning — there may be existing projects or goals to align with
4. Researching — avoid duplicating effort by checking what's already known

**To read the wiki:**
```bash
# List all pages
ls -la $PERSONAL_WIKI_ROOT/wiki

# Read a specific page
cat $PERSONAL_WIKI_ROOT/wiki/homepage.md
cat $PERSONAL_WIKI_ROOT/wiki/projects/active-project.md

# Search for content
grep -r "topic" $PERSONAL_WIKI_ROOT/wiki --include="*.md"
```

### Creating Pages

1. Create a Markdown file in the `wiki` subdirectory:
   - Use folders for organization (e.g., `projects/`, `research/`, `decisions/`)
   - File names become page URLs (e.g., `projects/my-project.md` → `/projects/my-project`)

2. Add content using Markdown syntax

3. **Commit the changes** — the wiki uses git for version control:
   ```bash
   cd $PERSONAL_WIKI_ROOT
   git add .
   git commit -m "Add page about X"
   ```

### Updating Pages

When adding new information to existing pages:
1. Append to the relevant section or create new sections
2. Include dates for time-sensitive information
3. Cross-reference related pages with WikiLinks
4. Commit the changes

### Integrating with Memory

The wiki is an extension of your memory system:

- **After conversations**: Review if anything discussed should be captured
- **After research**: Document key findings and sources
- **When patterns emerge**: Create or update pages that connect related information
- **During heartbeats**: Check for pages needing updates or maintenance

## Wikmd Markdown Features

Wikmd supports standard Markdown plus these extensions:

- **WikiLinks**: Link to other pages with `[[Page Title]]` or `[[Another Page|custom text]]`
- **Table of Contents**: Add `[TOC]` to insert a table of contents
- **Code Blocks**: Syntax highlighting with triple backticks
- **LaTeX Math**: Inline `$...$` and block `$$...$$` math rendering
- **Images**: Store images in `wiki/images/` and reference with `![alt](images/pic.jpg)`
- **Mermaid Diagrams**: Create flowcharts, sequence diagrams, etc.

See [Wikmd Documentation](https://linbreux.github.io/wikmd/) for full syntax details.

## Privacy & Security

- **Scope**: This skill only creates/modifies Markdown files in `PERSONAL_WIKI_ROOT/wiki`, reads documentation from https://linbreux.github.io/wikmd/ and hosts the Wiki on a local http server
- **Data Handling**: All content is stored locally; no data is sent to external services
- **Version Control**: Use git to track changes and maintain history
