---
name: perplexity-downloader
description: Download and save Perplexity.ai conversations as individual Markdown files. One thread = one .md file. Processes threads sequentially. Supports single thread, URL lists, or full history export. Triggers on "download perplexity thread", "export perplexity history", "save all perplexity threads", or any request to capture Perplexity conversations.
---

# Perplexity Thread Downloader

Downloads Perplexity.ai conversation threads and saves each as an individual Markdown file. Processes sequentially, one thread per file.

## Overview

This skill handles three export modes:
1. **Single Thread** — Download one thread by URL → one `.md` file
2. **Bulk from URL List** — Download multiple threads from a list → one `.md` file per thread, processed sequentially
3. **Full History Export** — Extract all threads from your Perplexity history → one `.md` file per thread, processed one-by-one

Each thread becomes its own Markdown file. All files saved to `~/perplexity-downloader/outputs/`.

---

## Mode Detection

When the user invokes the skill, detect their intent:

| User says | Mode |
|-----------|------|
| "Download this thread: [URL]" | Single Thread |
| "Export all my Perplexity threads" | Full History Export |
| "Download these threads: [list of URLs]" | Bulk from URL List |
| "Archive my Perplexity history" | Full History Export |

Ask clarifying questions if intent is ambiguous.

---

## Single Thread Download

### Workflow

1. **Get URL** → Ask user for Perplexity thread URL (e.g., `https://perplexity.ai/search/...`)
2. **Fetch** → Use `web_fetch(url, html_extraction_method="markdown")`
3. **Parse** → Extract question, answer, follow-ups, sources
4. **Build Markdown** → Structure as shown below
5. **Save** → One `.md` file per thread
6. **Present** → Show download link

### Markdown Format (per thread)

```markdown
# [Thread Title / First Question]

> Saved from Perplexity.ai  
> URL: [original URL]  
> Date: [today's date]

---

## Turn 1

### Question
[user's question text]

### Answer
[AI answer text]

#### Sources
1. [Source title](URL)
2. [Source title](URL)

---

## Turn 2

### Question
[follow-up question]

### Answer
[AI answer]

#### Sources
...
```

### Formatting Rules

- Use `##` for each conversation turn
- Preserve all source links exactly as found
- Keep inline citations like `[1]` if present in answer text
- Remove Perplexity UI text ("Ask follow-up", "Share", "Copy", etc.)
- Sanitize filename: lowercase, spaces → hyphens, remove special chars

### Output Filename

```
~/perplexity-downloader/outputs/[YYMMDD]-[sanitized-title].md
```

Example:
```
260423-what-is-the-best-way-to-learn-japanese.md
```

---

## Bulk Download from URL List

Use when user provides multiple thread URLs.

### Workflow

1. **Collect URLs** → Ask user to paste newline- or comma-separated list of URLs
2. **Loop sequentially** → For each URL:
   - Fetch the thread
   - Parse and clean
   - Build Markdown
   - Save to individual `.md` file
   - Show progress: *"Downloaded 3/10 threads..."*
3. **Create index** → Build `index.md` listing all downloaded threads
4. **Present** → Show all files for download

### Example URL Format

```
https://www.perplexity.ai/search/how-to-learn-python
https://www.perplexity.ai/search/best-practices-for-rest-apis
https://www.perplexity.ai/search/docker-vs-kubernetes
```

### Index File (index.md)

```markdown
# Perplexity Thread Archive

**Export Date:** 2026-04-23  
**Total Threads:** 3

## Threads

1. [How to learn Python](./260423-how-to-learn-python.md)
2. [Best practices for REST APIs](./260423-best-practices-for-rest-apis.md)
3. [Docker vs Kubernetes](./260423-docker-vs-kubernetes.md)
```

### Output Files

```
~/perplexity-downloader/outputs/
├── index.md
├── 260423-how-to-learn-python.md
├── 260423-best-practices-for-rest-apis.md
└── 260423-docker-vs-kubernetes.md
```

---

## Full History Export

Use to download ALL threads from user's Perplexity account.

### Prerequisites

User must be logged into Perplexity.ai in their browser.

### Workflow

1. **Get History Page** → Ask user to do one of:
   - Visit `https://www.perplexity.ai/` (logged in), scroll history sidebar to load all threads, copy/paste the page
   - Or provide the URL to their Perplexity home page
2. **Extract Thread URLs** → Parse the content for all thread URLs (pattern: `https://perplexity.ai/search/...`)
   - Deduplicate
   - Report count: *"Found 42 threads in your history"*
3. **Download Each Thread Sequentially** → Loop through each URL:
   - Fetch thread page
   - Parse and clean
   - Build Markdown
   - Save to individual `.md` file
   - Show progress: *"Downloaded 15/42 threads..."*
4. **Create Archive Structure** → Build folder with index + all thread files
5. **Present** → Offer as folder download or batch of files

### Output Structure

```
~/perplexity-downloader/outputs/perplexity-archive-2026-04-23/
├── index.md
├── perplexity-thread-001.md
├── perplexity-thread-002.md
├── perplexity-thread-003.md
└── [... more threads ...]
```

### Archive Index (index.md)

```markdown
# Perplexity Complete Archive

**Export Date:** 2026-04-23  
**Total Threads:** 42  
**Date Range:** 2025-01-15 to 2026-04-23

## All Threads

1. [What is the best way to learn Japanese?](./perplexity-thread-001.md) — 2026-04-20
2. [How to optimize Docker builds?](./perplexity-thread-002.md) — 2026-04-19
3. [Best practices for REST API design](./perplexity-thread-003.md) — 2026-04-15
...
[full list with dates]
```

### Processing Speed

For sequential processing:
- **Single thread:** ~2-5 seconds (fetch + parse)
- **10 threads:** ~30-60 seconds (with rate limiting)
- **50 threads:** ~5-10 minutes
- **100+ threads:** 15-30 minutes (may want to offer date-range filtering)

Show progress continuously so user knows it's working.

---

## Handling Edge Cases

| Situation | What to do |
|-----------|------------|
| Page returns empty or access denied | Thread may be private/login-gated. Ask user to paste the page text manually. |
| Thread has only one turn | Use same format, just one `## Turn 1` section. |
| Very long thread (10+ turns) | Process all turns; note turn count in file header. |
| Sources section missing | Omit `#### Sources` block for that turn. |
| Non-English thread | Preserve original language; do not translate. |
| Rate limited during bulk download | Pause 5 seconds between requests. Inform user of slowdown. |
| Some URLs fail during bulk export | Skip failed URLs, log them, report at end: *"Downloaded 40/42 threads; 2 failed (access denied)"* |
| History page doesn't yield URLs | Ask user to manually provide thread URLs or copy-paste page content for manual parsing. |

---

## Manual Fallback (if web_fetch fails)

If `web_fetch` cannot retrieve a page (login wall, access denied, etc.):

> "I wasn't able to fetch this thread automatically — it may require a login. You can copy the full page text and paste it here, and I'll format it into Markdown."

When user pastes raw text, apply the same parsing and formatting logic to create the `.md` file.
