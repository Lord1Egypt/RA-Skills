# Academic Engineering Literature Survey 📚

**Transparent, two-phase workflow with checkpoints** — dual mode, IEEE citations, structured briefs, reproducible method.

## Why This Skill Exists

Most "deep research" tools are black-box API wrappers. This skill is for **engineering researchers who already know their direction** and need to track field progress without a heavy multi-theme, multi-cycle process.

**This skill is different:**
- ✅ **Full methodology visible** — Two-phase workflow, strategy recorded for appendix
- ✅ **No external dependencies** — Runs on native tools (web_search, web_fetch, sessions_spawn)
- ✅ **User checkpoints** — Screening plan confirmation + draft confirmation before final report
- ✅ **Engineering focus** — IEEE Trans, Science Robotics; IEEE citations; engineering-value interpretation
- ✅ **Structured output** — Tables and charts encouraged; 4.0–4.4 brief structure; method appendix for reproducibility

## Comparison with Cloud-Based Research Tools

| Feature | This Skill | Cloud API Wrappers |
|---------|------------|-------------------|
| Methodology | Fully documented | Black box |
| Dependencies | None | External API + key |
| Research mode | Dual mode (initial survey / daily reading) | Unspecified |
| Quantity target | 50–80 or 30–50 papers by mode | Unspecified |
| User checkpoints | Screening plan + draft confirmation | Usually none |
| Citation format | IEEE | Varies/unspecified |
| Output | Structured brief with tables/charts | Varies |
| Reproducibility | Method appendix (keywords, DBs, criteria) | Unknown |

## Core Features

### Startup Protocol
At session start, the agent **must** ask for:
- **Research mode:** 1 = Initial survey (last 3 years, 50–80 papers), 2 = Daily reading (last 3 months, 30–50 papers)
- **Research topic:** e.g. embodied AI, robot long-range navigation, NeRF-based 3D reconstruction

### Phase 1: Broad Retrieval + Checkpoint 1
- Build 3–10 keyword groups; run retrieval on Google Scholar, Semantic Scholar, arXiv, IEEE Xplore.
- If paywall/login: pause and ask user to provide content or skip.
- Meet quantity target or propose changes and get confirmation.
- **Checkpoint 1:** Present preliminary count and screening plan; ask for extra conditions; wait for approval.

### Phase 2: In-Depth Analysis
- Shortlist by citation, venue, relevance (and user’s conditions).
- For each paper: title, authors, venue, core contribution, **engineering perspective** (algorithm, code, data, reproducibility), **IEEE citation**.
- Mark "analysis based on abstract only" when full text is unavailable.

### Structured Brief (Sections 4.0–4.4)
- **4.0** Title (by mode: initial survey vs date + daily brief)
- **4.1** Executive summary
- **4.2** Categorized selected papers (tables/charts encouraged)
- **4.3** Appendix: full initial list (title + URL)
- **4.4** Method appendix: keywords, time range, databases, screening criteria

### Draft Confirmation
Before publishing the final report, send a **draft** and ask if the user wants to change grouping, add/remove papers, or adjust interpretation. Publish final version only after feedback.

## Quick Start

Choose mode and topic. Example inputs:

```
1, robot long-range navigation
2, NeRF-based 3D reconstruction
```

Or: `/research` then when prompted, reply with mode and topic (e.g. `1, embodied AI`).

## Research Protocol

### Startup
Agent sends the fixed prompt: select mode (1 or 2) and enter research topic. **Waits for your reply.**

### Phase 1: Broad retrieval
- Keyword strategy → retrieval on academic platforms
- Paywall: agent pauses and asks you to provide content or skip
- **Checkpoint 1:** Agent reports count and screening plan, asks for extra conditions. **You confirm.**

### Phase 2: In-depth analysis
- Agent builds shortlist and extracts per-paper info (engineering perspective, IEEE citation).
- **Draft confirmation:** Agent sends draft brief and asks for changes. **You confirm or request edits.**

### Final report
Structured brief with 4.0–4.4 (title, executive summary, categorized papers, full list, method appendix). IEEE references; tables and figures used where helpful.

## File Structure

```
├── SKILL.md       # Full methodology (engineering literature survey)
├── README.md      # This file
├── quickref.md    # One-page quick reference
├── example.md     # Example workflow (English)
└── LICENSE        # Apache 2.0
```

This skill focuses on **engineering literature** and prioritizes **IEEE Trans** and **Science Robotics**.

## When to Use This

- You have a clear research direction and need a literature survey
- Tracking technical and industry progress (e.g. embodied AI, world models, robotics, 3D reconstruction)
- You want IEEE-style citations and an engineering-focused interpretation
- You want a reproducible method (keywords, databases, criteria) in the appendix

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

**Built for engineering researchers who care about methodology and reproducibility.**
