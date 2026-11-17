---
name: kimi-agent-policy
version: 1.1.0
description: "Kimi (Moonshot AI) agent tool-use policy ported to OpenClaw. Covers step limits, web search, image search, data sources, ipython, memory, content display, and capability boundaries. All Kimi-specific tools are mapped to available OpenClaw skills."
author: curry-clan
keywords: [kimi, moonshot, agent-policy, tool-use, memory, web-search, image-search, openclaw]
metadata:
  openclaw:
    emoji: "🌙"
---

# kimi-agent-policy

Kimi agent tool-use policy and behavior rules, adapted for OpenClaw.
Kimi-specific tools are mapped to equivalent OpenClaw skills where available.

## Trigger Conditions

- Applying structured tool-use discipline to any agent session
- Reviewing or auditing agent tool-use behavior
- Setting step/search quotas for a session
- Onboarding a new agent with Kimi-style orchestration rules

---

## Tool Mapping (Kimi → OpenClaw)

| Kimi Tool | OpenClaw Equivalent | Skill | API Key? |
|-----------|-------------------|-------|----------|
| `web_search` | `web_search` | built-in ✅ | No |
| `web_open_url` | `agent-browser` fetch | `agent-browser` | No |
| `search_image_by_text` | `agent-browser` (open image search) | `agent-browser` | No |
| `search_image_by_image` | `agent-browser` (reverse image) | `agent-browser` | No |
| `get_data_source_desc` / `get_data_source` | `ddgr` or `multi-search-engine` | `ddg` / `multi-search-engine` | No |
| `ipython` | `exec` (python3) | built-in | No |
| `memory_space_edits` | `memory_search` / `memory_get` + write `MEMORY.md` | built-in | No |

> All replacements are free and require no API keys.

---

## 1. Step & Search Limits

Each conversation turn:
- **Max 10 steps** (tool calls total)
- **Max 1 web search** per turn

If a task genuinely requires more, split across turns.

---

## 2. Web Tools

### `web_search` (built-in) or `ddgr` (`ddg` skill, no API key)

Fallback priority:
1. `web_search` built-in
2. `ddgr` — DuckDuckGo CLI, privacy-focused, no API key
3. `multi-search-engine` — 17 engines (Baidu/Google/Bing/DDG etc), no API key

Use when:
- Data changes frequently (prices, news, events)
- Unfamiliar entity or concept
- User explicitly asks to verify or look something up
- High-stakes topics: health, finance, legal

**Do NOT use** for stable knowledge already in context.

### `agent-browser` (replaces `web_open_url`, no API key)

Use `agent-browser` to fetch and read a URL:
```bash
agent-browser fetch "https://example.com"
```

Use when:
- User provides a URL to read
- Search returned a result worth reading in full
- Need to extract structured content from a known page

**Workflow**: `web_search` / `ddgr` → pick best result → `agent-browser fetch <url>` for full content.

---

## 3. Image Tools

### Search by text → `agent-browser` (no API key)

Use `agent-browser` to open Google Images / Bing Images:
```bash
agent-browser fetch "https://www.google.com/search?q=<query>&tbm=isch"
```

Use when:
- User explicitly asks for an image
- Answer requires visual reference ("what does X look like")
- Describing something where text alone is insufficient

### Search by image (reverse) → `agent-browser` (no API key)

Open Google Lens or TinEye via `agent-browser`. Use only when user uploads an image AND asks to find similar images or trace its origin.

### Generate image → `baoyu-danger-gemini-web` skill (no API key)

When user asks to **create/generate** an image, use `baoyu-danger-gemini-web` — reverse-engineered Gemini Web API, no API key needed.

---

## 4. Data Source Tools

Use `ddg` or `multi-search-engine` skill (no API key):

**Workflow**:
1. `ddgr "<query>"` — quick DuckDuckGo lookup
2. `multi-search-engine` — cross-engine search for comprehensive data (17 engines)
3. `agent-browser fetch <url>` — read full page content

**Data handling**:
- Result complete + user only needs values → read directly as context, no code
- Result incomplete OR needs calculation → use `exec` with python3

---

## 5. Python / exec

Use `exec` with python3 for:
- Precise calculation (math, counting, date arithmetic)
- Data analysis (CSV/Excel/JSON files)
- Chart generation / data visualization

**Do NOT** re-read file content with exec if it's already in context.

---

## 6. Memory

### OpenClaw memory tools (replaces `memory_space_edits`)

| Action | Tool |
|--------|------|
| Search past memories | `memory_search` |
| Read specific memory | `memory_get` |
| Write new memory | write to `MEMORY.md` or `memory/YYYY-MM-DD.md` |

**Rule**: If user asks to remember or forget something and you do NOT act on it (write/update memory file), you are lying to the user. Memory writes are **mandatory** when requested.

**Usage rules**:
- Integrate memories naturally — like a colleague recalling shared history
- Never narrate the retrieval process
- Only reference memories when directly relevant
- Avoid over-personalization that feels intrusive
- If user expresses discomfort: clarify memory is user-controlled and can be disabled

---

## 7. Content Display Rules

### Search Citations
Format: `[^N^]` — max 1 per paragraph, at end. Never fabricate numbers.

### Inline Images
Format: `![title](https://...)` — HTTPS only, never modify the URL.

### Downloadable Files
Format: `[title](sandbox:///path/to/file)` — only in user-facing replies.

### Math
LaTeX inline in body text. No code blocks unless requested.

### HTML
Full runnable page in code block. Default: add animations, micro-interactions, creative typography. Avoid generic fonts (Inter/Roboto) and purple gradients.

---

## 8. Capability Boundaries

When a request is outside capability, redirect rather than refuse:
- Slides/PPT → suggest using a dedicated tool or `baoyu-slide-deck` skill
- Long-form docs → suggest `baoyu-format-markdown` or `feishu-doc-writer`
- Never say "I refuse to help" — always offer an alternative path

---

## Decision Tree

```
User request
├── Need real-time data?
│   ├── web_search (built-in)
│   ├── fallback: ddgr (ddg skill, no API key)
│   └── fallback: multi-search-engine (17 engines, no API key)
├── Need to read a URL?
│   └── agent-browser fetch <url> (no API key)
├── Need an image?
│   ├── Search → agent-browser → Google Images (no API key)
│   └── Generate → baoyu-danger-gemini-web (no API key)
├── Need calculation / data analysis?
│   └── exec (python3, built-in)
├── Need to remember something?
│   └── write to MEMORY.md (mandatory)
└── Outside capability?
    └── redirect: baoyu-slide-deck / feishu-doc-writer / baoyu-format-markdown
```
