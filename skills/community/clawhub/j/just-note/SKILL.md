---
name: notes
description: Manage personal markdown notes — search, read, create, and append to notes. Use when the user asks to jot down an idea, find a note, list notes, or add something to an existing note.
user-invocable: true
---

# Notes Skill

Personal notes manager. Notes live in `/home/node/.openclaw/workspace/notes/` as markdown files with optional YAML frontmatter.

**On the host (VPS)** this maps to `/root/.openclaw/workspace/notes/` — data persists across container restarts.

## Setup

On first use, create the notes directory if it doesn't exist:

```bash
mkdir -p /home/node/.openclaw/workspace/notes/ideas
mkdir -p /home/node/.openclaw/workspace/notes/projects
mkdir -p /home/node/.openclaw/workspace/notes/daily
mkdir -p /home/node/.openclaw/workspace/notes/misc
```

## Note format

```markdown
---
tags: [idea, article]
created: 2026-03-06
---

# Title

Content here.
```

Frontmatter is optional. If absent, treat the file as plain markdown.

## Paths

All paths below use the variable `NOTES` for brevity:

```bash
NOTES=/home/node/.openclaw/workspace/notes
```

## Commands

### List notes

```bash
find $NOTES -name '*.md' -type f | sed "s|$NOTES/||" | sort
```

### Search by content

```bash
grep -rn --include='*.md' -i 'SEARCH_TERM' $NOTES/
```

### Search by tag

```bash
grep -rl --include='*.md' 'tags:.*TAGNAME' $NOTES/
```

### Read a note

```bash
cat $NOTES/PATH_TO_NOTE.md
```

### Create a new note

1. Generate a slug from the title (lowercase, hyphens, no special chars).
2. Add YAML frontmatter with `tags` and `created` (today's date).
3. Write to the appropriate subdirectory.

```bash
cat > $NOTES/SUBDIR/SLUG.md << 'EOF'
---
tags: [tag1, tag2]
created: YYYY-MM-DD
---

# Title

Content
EOF
```

### Append to an existing note

```bash
echo -e "\n## New section\n\nContent to add" >> $NOTES/PATH_TO_NOTE.md
```

### Daily quick note

For quick thoughts without a full note, append to today's daily file:

```bash
mkdir -p $NOTES/daily
FILE=$NOTES/daily/$(date +%Y-%m-%d).md
[ -f "$FILE" ] || echo "# $(date +%Y-%m-%d)" > "$FILE"
echo "- $(date +%H:%M) — Quick thought here" >> "$FILE"
```

## Behavior guidelines

- When creating notes, confirm the title and tags with the user unless the request is unambiguous.
- When searching, show matching filenames and a brief context snippet.
- Keep file names short and descriptive: `gpu-price-tracking.md`, not `note-about-tracking-gpu-prices-over-time.md`.
- Never delete notes without explicit confirmation.
- When listing, show relative paths from the notes root for readability.
