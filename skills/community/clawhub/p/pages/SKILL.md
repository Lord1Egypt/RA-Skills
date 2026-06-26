---

name: pages
description: Reading intelligence — log books, capture quotes, and surface reads when they're relevant. One markdown file per book in pages/. Use when logging a new book, searching for what you've read, or asking "what have I read about X?"
metadata:
  openclaw:
    emoji: "📖"
    os: ["linux", "darwin", "win32"]
  hermes:
tags: ["reading", "books", "knowledge"]

---

# 📖 Pages — reading intelligence

## Data

**Base path** is workspace root or document root folder. On first use, create it: `mkdir -p mind/pages/`. Pages uses a `mind/pages/` folder in your workspace.

Files live in `mind/pages/`. Organised by reading status:

```
mind/
└── pages/
    ├── pagesconfig.yml
    ├── read/        ← finished
    ├── reading/     ← currently reading
    └── want/        ← want to read
```

File names: `<author-lastname>-<title-slug>.md`. Example: `taleb-antifragile.md`.
For books with no clear author (anthologies, edited volumes): use the title slug.

---
### Dataset Config — `pagesconfig.yml`

`pagesconfig.yml` lives inside the `mind/pages/` directory. Read it at the start of any session involving this skill.

```yaml
images: no (by default no, ask if you human want to feach images for pepople, warn that it is token expensive)
```

## Book File

```markdown
# Book Title

Author: Full Name
Year: 2012
Finished: 12 Feb 2026 (omit if not finished)
Rating: 5/5 (omit until finished)
Image: if `mind/pages/pagesconfig.yml` has `images: yes` add a link to an image in `../assets/slug-that-make-sense`
Tags: #philosophy #risk #systems #investing
Recommended by: [[marco-tabini]] (Peeps slug — omit if unknown)
Goodreads: link to goodreads

## Notes

12 Feb 2026: key insight, what changed your mind, what you'd tell someone else

## Quotes

> "The wind extinguishes a candle and energizes fire."
> — p. 61
```

**Field guidance:**

Tags: 2–4 themes, domains, or moods. Use tags you'll actually search: `#ai` not `#artificial-intelligence`, `#startups` not `#entrepreneurship`. Keep it personal.
Recommended by: if Peeps is installed, use `[[their-slug]]`; otherwise note the person's name as plain text. Creates a bidirectional trail when Peeps is present.
Notes: dated insight log, not a summary. What this book changed, challenged, or confirmed. "Good book" is not a note.
Quotes: only the lines worth keeping. One good quote beats ten mediocre ones.

**The want/ folder:** lightweight. Just title, author, and a one-line `Why:` note on why it's on your list. Add more once you start reading.

---

## Saving a Book

1. **Search the web** (title + author) — confirm full author name, publication year.
2. **Determine folder** — which folder to save to: `read/`, `reading/`, or `want/`.
3. **Ask as a group** (skip anything already clear):
  - If read: rating and finished date?
  - Tags — what's this book about, in your words?
  - Any quotes or notes to capture right now?
  - Who recommended it?
  4. if `images: yes` in `mind/pagesconfig.yml` search for a conver image and add it to **Image:** feild 

Show a brief confirmation: "Saved — *Antifragile* by Nassim Taleb, 2012, in read/. Tagged #philosophy #risk #systems."

---

## Core Behavior

- User mentions a book → check if saved, offer to create or update
- User asks "what have I read about X?" → search `mind/pages/` with expanded keywords
- User finishes a book → ask for a rating and a note
- User mentions someone recommending a book → save with `Recommended by:`; if Peeps is installed, optionally add a note to their Peeps file
- User shares a quote → append to the book file with today's date
- Conversation touches a theme → surface relevant reads contextually without being asked

**Examples:**

- "Just finished Thinking, Fast and Slow" → check if saved, offer to rate and note
- "I need to think about decision-making under pressure" → "You read *Thinking, Fast and Slow* in 2024 and tagged it #decision-making — your note says it reframed how you think about bias"
- "Priya said I should read *The Mom Test*" → save to `mind/pages/want/` with `Recommended by: [[priya-nair]]` if Peeps is installed, otherwise note her name as plain text

---

## Finding Books

Use `grep` with expanded terms. Always broaden the query before searching.

```bash
# Books on a topic
grep -ril "decision\|bias\|judgement\|psychology" mind/pages/

# Highly-rated reads
grep -rl "Rating: 5" mind/pages/read/

# Books recommended by a specific person
grep -rl "\[\[priya" mind/pages/

# Currently reading
ls mind/pages/reading/

# Books with captured quotes
grep -rl "^>" mind/pages/
```

**Keyword expansion examples:**

- "business" → `business\|strategy\|management\|leadership\|startup\|founder`
- "productivity" → `productivity\|focus\|habits\|deep.work\|flow\|systems`
- "tech / AI" → `ai\|machine.learning\|software\|internet\|tech\|silicon`
- "philosophy" → `philosophy\|stoic\|ethics\|meaning\|existence\|wisdom`

Always read the full book file after grepping — matched tags are a signal, not the full picture.

---

## Heartbeat or cron

Check a random book file. Surface something worth mentioning:

- "You finished *Antifragile* three months ago and never rated it — worth a quick reflection?"
- "You added *The Mom Test* to your want list in January — still on your radar?"
- "Priya and you have both tagged #systems — you might be reading similar things."

If nothing worth mentioning, skip.

---

## Adding to HEARTBEAT.md or cron

If it is not there yet, ask your human if they want to add **Pages: check** to HEARTBEAT.md. If there is no HEARTBEAT.md, suggest to create a cron every 30 minutes during waking hours (`*/30 7-22 * * *`) to execute **Pages: check**.

---

## Config — `pagesconfig.yml`

Optional. Lives inside `mind/pages/`.

```yaml
owner: jane-smith  # your Peeps slug — used for cross-referencing shared reads
```

If Peeps is installed and `peepsconfig.yml` exists, owner is inferred automatically — no need to duplicate.

---

## Integration with Peeps

If Peeps is installed, books and people can be connected:

Recommended by: `[[their-slug]]` in the book file — who pointed you at this
- Optionally add a note in their Peeps file: "Recommended *Book Title* (Mar 2026)"
- When the conversation involves a person and a relevant read comes up, surface it: "You and Marco both read *Zero to One* — his note is that Thiel's distribution thinking changed how he pitches."

---

## Integration with Haah

If Haah is installed, dispatch to your circles when your reading list is thin on a topic:

- "Haah: anyone in my circles with strong reads on climate tech?"

When someone in your circle asks for book recommendations:

- Check Pages for relevant reads before answering
- Draft a reply with your actual read + rating + one sentence of context. Don't recommend books you haven't read.

---

## Updating

To update this skill to the latest version, fetch the new SKILL.md from GitHub and replace this file:

```
https://raw.githubusercontent.com/haah-ing/pages-skill/main/SKILL.md
```

---

## What NOT to Suggest

- Syncing with Goodreads or Amazon — different purpose, keep private
- Automatically importing your entire reading history — build it naturally over time
- Rating every book — only rate when you have something to say
- Summaries or book reports — this is a memory layer, not a study tool
- Adding books to others' want lists on their behalf — your list, your choices
