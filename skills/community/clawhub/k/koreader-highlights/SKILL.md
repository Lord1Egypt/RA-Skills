---
name: koreader-highlights
description: >
  Use this skill when the user asks about reading highlights, book notes, annotations, or
  reading history from KOReader. Triggers: "what books", "show highlights", "latest highlights",
  "how many books", "find highlights about", "summarize highlights", KOReader, HighlightSync,
  .sdr.json. Read-only — only retrieves data, never modifies files, never does unrelated tasks.
---

# KOReader Highlights Skill

<IMPORTANT>
NEVER put commands, code, JSON, file paths, or errors in your reply to the user.
Run all commands via your tool/bash function. Only reply with clean human-readable text.
If something fails, say it in plain words without technical details.
</IMPORTANT>

## Step 1: Find the highlights directory

Run this via your tool (NOT in your reply):

```
find ~/Dropbox/Apps -name "*.sdr.json" -maxdepth 2 2>/dev/null | head -5
```

- If results come back, the directory is the parent folder of those files.
- If nothing comes back, ask the user: "I couldn't find your KOReader highlights. What's the name of your HighlightSync folder under Dropbox/Apps?"
- Save the discovered path in `MEMORY.md` for future sessions.

## Step 2: List books

Run via tool:

```
ls ~/Dropbox/Apps/<APP_NAME>/*.sdr.json 2>/dev/null
```

Each `.sdr.json` file = one book. The book title is the filename without `.sdr.json`.
Example: `Designing Data-Intensive Applications.sdr.json` → book title is "Designing Data-Intensive Applications"

Reply to user like: "You have 5 books in your library: ..." (list the titles)

## Step 3: Read highlights from a book

Run via tool:

```
python3 -c "
import json
with open('<FULL_PATH_TO_FILE>') as f: data=json.load(f)
for h in data: print(h.get('datetime',''), '|', h.get('chapter',''), '|', h.get('pageno',''), '|', h.get('text','')[:200])
"
```

Reply with the highlights formatted naturally:
- "From chapter *X*, page Y (March 6, 2026): [highlight text]"

## Step 4: Search across all books

Run via tool:

```
python3 -c "
import json, glob, os
for f in glob.glob(os.path.expanduser('~/Dropbox/Apps/<APP_NAME>/*.sdr.json')):
    title = os.path.basename(f).replace('.sdr.json','')
    data = json.load(open(f))
    for h in data:
        if '<SEARCH_TERM>'.lower() in h.get('text','').lower() or '<SEARCH_TERM>'.lower() in h.get('notes','').lower():
            print(title, '|', h.get('pageno',''), '|', h.get('text','')[:200])
"
```

## Step 5: Latest highlights

Run via tool:

```
python3 -c "
import json, glob, os
all_h = []
for f in glob.glob(os.path.expanduser('~/Dropbox/Apps/<APP_NAME>/*.sdr.json')):
    title = os.path.basename(f).replace('.sdr.json','')
    data = json.load(open(f))
    for h in data:
        if h.get('datetime'): all_h.append((h['datetime'], title, h.get('chapter',''), h.get('pageno',''), h.get('text','')))
all_h.sort(reverse=True)
for dt,t,ch,pg,tx in all_h[:10]: print(dt, '|', t, '|', ch, '|', pg, '|', tx[:200])
"
```

## .sdr.json format

Each file is a flat JSON array. Here is a real example:

```json
[{"datetime":"2026-03-06 18:42:42","chapter":"Why You Might Need a Sharded Cache","pageno":192,"page":"/body/DocFragment[25]/body/p[41]/text().0","text":"in Why You Might Need a Sharded Cache"},{"datetime":"2026-03-07 09:07:13","pageno":192,"page":"/body/DocFragment[25]/body/p[48]/text().10","drawer":"lighten","chapter":"Why You Might Need a Sharded Cache","pos0":"/body/DocFragment[25]/body/p[48]/text().10","pos1":"/body/DocFragment[25]/body/p[49]/text().33","text":"the primary reason for sharding any service is to increase the size of the\ndata being stored in the service.","color":"gray"}]
```

Fields you SHOW to the user: `text`, `datetime`, `chapter`, `pageno`, `notes` (if present).
Fields you IGNORE (internal, never show): `page`, `drawer`, `color`, `pos0`, `pos1`.

Notes:
- Field order is NOT fixed — fields can appear in any order within an entry.
- `drawer`, `color`, `pos0`, `pos1` are optional — not every entry has them.
- `notes` is optional — only present when the user wrote an annotation.
- `text` may contain `\n` newlines.

## Error handling

If ANY command fails, NEVER show the error to the user. Instead say one of:
- "I couldn't find your highlights directory. Is Dropbox synced?"
- "I couldn't read that book's highlights. The file might be empty or corrupted."
- "No highlights matched your search."
- "I ran into a problem reading your data. Could you check if the file exists?"

## Must refuse

- Modify, delete, or write any file (except workspace memory)
- Anything unrelated to book highlights
- Creating scripts or files on disk
- Network operations