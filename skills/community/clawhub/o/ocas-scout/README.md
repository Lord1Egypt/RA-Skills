# ⚙️ Scout

  <img src="./assets/readme/hero.jpg" width="100%" alt="Scout">

Structured OSINT research on people, companies, and organizations. Use for provenance-backed briefs, entity resolution across public sources, background research with cited sources, or free-first research workflows that escalate to paid sources only with explicit permission. Do not use for topic research without a person/org focus (use Sift) or illegal data collection.

**Skill name:** `ocas-scout`
**Version:** 4.0.0
**Type:** 
**Layer:** research
**Author:** <agent-name>

---

## 📖 Overview

Structured OSINT research on people, companies, and organizations. Use for provenance-backed briefs, entity resolution across public sources, background research with cited sources, or free-first research workflows that escalate to paid sources only with explicit permission. Do not use for topic research without a person/org focus (use Sift) or illegal data collection.

---

## 🔧 Capabilities

- `"user"` — the signal is relevant to the user's personal knowledge graph
- `"agent_only"` — agent-initiated research with no demonstrated user connection
- `scout.research.start` — begin a new research request with subject and goal
- `scout.research.expand --tier <1|2|3>` — escalate to a higher source tier
- `scout.brief.render` — generate the final markdown brief with findings and sources
- `scout.brief.render_pdf` — optional PDF brief generation
- `scout.status` — return current research state
- `scout.journal` — write journal for the current run; called at end of every run
- `scout.update` — pull latest from GitHub source; preserves journals and data
- `scout.sources.discover` — discover new MCP servers relevant to current research
- `scout.sources.refresh` — refresh curated source lists from GitHub
- `scout.sources.status` — show state of dynamic source discovery
- **`gh api` base64 content is unreliable for counting** — `gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d` can silently return truncated or empty results. For fetching raw GitHub README content, use `curl -s "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md"` instead. This returns clean text that `wc -l` and `grep` can process directly.

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

- [2.10.0] - 2026-04-12
- Added
- Removed
- [2026-04-05] Hunter.io parallel OSINT integration
- Added
- Changed
- Validation
- [2026-04-04] Spec Compliance Update

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
