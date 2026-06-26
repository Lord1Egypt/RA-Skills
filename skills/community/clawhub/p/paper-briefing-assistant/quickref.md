# Engineering Literature Survey — Quick Reference

## Invocation
- `/research` or e.g. "literature survey" / "文献调研"
- **Startup:** Agent **must** first send mode + topic prompt; do not begin retrieval until user replies.

## Research Modes

| Mode | Time range | Goal | Paper target |
|------|------------|------|---------------|
| **1. Initial survey** | Last 3 years | Knowledge framework, high-impact papers | 50–80 |
| **2. Daily reading** | Last 3 months | Frontier breakthroughs, open-source | 30–50 |

## Two Phases + Checkpoints

| Step | User action | Agent action | Output |
|------|-------------|--------------|--------|
| Startup | Choose mode (1/2) + topic | Send fixed prompt, **WAIT** | Mode + topic |
| Phase 1 | — | Keywords → retrieve (Scholar, Semantic Scholar, arXiv, IEEE Xplore) | Raw list |
| **Checkpoint 1** | Confirm screening plan / add conditions | Report count + screening plan, **WAIT** | Shortlist approved |
| Phase 2 | — | Per-paper extraction (engineering view, IEEE refs) | Draft brief |
| **Draft confirm** | Confirm or request edits | Send draft, **WAIT** | Final brief |
| Final | — | Publish final brief (4.0–4.4) | Structured report |

## Retrieval and Barriers
- **Keywords:** 3–10 groups (with synonyms); record for Method Appendix.
- **Platforms:** Google Scholar, Semantic Scholar, arXiv, IEEE Xplore (and similar).
- **Paywall / login:** Pause and tell user: e.g. "Paper X needs IEEE Xplore. Provide HTML/PDF or say skip." Resume only after user reply.

## Output Structure (Final Brief)
- **4.0** Title — `[Topic] — Initial survey` or `[Topic] — YYYY-MM-DD daily brief`
- **4.1** Executive summary — scope, strategy, main findings
- **4.2** Categorized selected papers — groups; per paper: title+link, core interpretation, code/data links, IEEE citation; **use tables/charts**
- **4.3** Appendix: full initial list — all Phase 1 papers (title + URL)
- **4.4** Method appendix — keyword groups, time range, databases + dates, screening criteria

## Citation: IEEE
- **In-text:** [1], [2], [1]–[3]
- **References:** Numbered by order of appearance; full IEEE style (authors, title, venue, vol/issue/pages, year, URL/DOI when available).

## Writing and Content
- **Tables and figures:** Allowed and **encouraged** in the brief.
- **Engineering perspective:** For each shortlisted paper, stress: algorithm efficiency, open-source code, datasets, reproducibility.
- **Abstract-only:** If no full text, state "Analysis based on abstract only" and give abstract URL.

## Exception Handling
- **Too few results:** Propose broader keywords or time range; get user confirmation before continuing.
- **Draft before final:** Always ask whether to change grouping, add/remove papers, or adjust focus; then publish final version.
