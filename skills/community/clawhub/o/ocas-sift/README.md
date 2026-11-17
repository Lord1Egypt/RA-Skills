# ⚙️ Sift

  <img src="./assets/readme/hero.jpg" width="100%" alt="Sift">

>-

**Skill name:** `ocas-sift`
**Version:** 2.9.3
**Type:** 
**Layer:** Execution
**Author:** Indigo Karasu

---

## 📖 Overview

>-

---

## 🔧 Capabilities

- `"user"` — the signal is relevant to the user's personal knowledge graph
- `"agent_only"` — the signal is agent-initiated research with no demonstrated user connection
- `sift.search` — execute a search query with automatic tier selection and query rewriting
- `sift.research` — run a multi-source research session producing a structured research journal
- `sift.verify` — fact-check a specific claim across multiple sources with consensus scoring
- `sift.summarize` — summarize a document or URL with structured entity extraction
- `sift.extract` — extract entities, claims, statistics, and relationships from content
- `sift.thread.list` — list active research threads with entity overlap detection
- `sift.status` — return current state: active threads, quota usage, source reputation summary
- `sift.journal` — write journal for the current run; called at end of every run
- `sift.update` — pull latest from GitHub source; preserves journals and data
- `sift.fetch [url]` — extract clean Markdown content from a URL. Runs Scrapling first (fast HTTP for static sites, headless browser mode for JS-heavy sites); falls back to Jina Reader (`r.jina.ai/<url>`) if Scrapling output is below content threshold. Returns Markdown with structure preserved. Use for summarizing a specific page or document the user provides.
- `sift.webwright` — execute an interactive web task using browser automation (Playwright driving the system Chrome). **Requires the `playwright` package** (`pip install playwright`); it uses the already-installed Chrome via `channel="chrome"`, so no browser download is needed. Write the plan, exploration screenshots, instrumented final_script.py, execution log, and self-verification into `{agent_root}/commons/data/ocas-sift/webwright/`. For form filling, multi-step flows, JS-heavy sites, interactive filtering, or any task where the browser is the workspace. Read `references/webwright-integration.md` before first use.

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [2.8.5] - 2026-04-12
- Fixed
- [2026-04-05] N2 MCP + URL content fetcher
- Added
- Changed
- Validation
- [2026-04-04] Spec Compliance Update
- Changes

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
