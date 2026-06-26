# Engineering Literature Survey — Example Workflow (English)

## User Input

User invokes the skill (e.g. `/research`) and, when prompted, replies with mode and topic:

```
1, robot long-range navigation
```

---

## Startup Protocol

The agent **must** respond first with:

> Please select your research mode and enter your research topic:
>
> **Research mode**  
> 1. 【Initial survey】 — Systematically understand a new area (time range: last 3 years; goal: build knowledge framework, identify high-impact literature)  
> 2. 【Daily reading】 — Follow latest progress in an existing direction (time range: last 3 months; goal: capture frontier breakthroughs and open-source results)
>
> **Research topic [User_Topic]:** e.g. embodied AI, world models, robot long-range navigation, NeRF-based 3D reconstruction
>
> Example input: "1, robot long-range navigation" or "2, NeRF-based 3D reconstruction"
>
> I will run the two-phase workflow according to your choice and confirm with you at key checkpoints.

User has already replied: `1, robot long-range navigation`. So mode = **Initial survey**, topic = **robot long-range navigation**. Agent proceeds to Phase 1.

---

## Phase 1: Broad Retrieval and Preliminary Screening

### 2.1 Retrieval Strategy

Agent generates 3–10 keyword groups (examples for "robot long-range navigation"):

| # | Keyword group (and synonyms) |
|---|------------------------------|
| 1 | long-range navigation, long-horizon navigation |
| 2 | robot navigation, mobile robot navigation |
| 3 | semantic navigation, visual navigation |
| 4 | SLAM long-term, lifelong navigation |
| 5 | outdoor navigation, large-scale navigation |

Time range: **last 3 years**. Full strategy is recorded for Section 4.4 (Method Appendix).

### 2.2 Execute Retrieval

Agent uses `web_search` / `web_fetch` (and optionally `sessions_spawn`) to query:

- Google Scholar  
- Semantic Scholar  
- arXiv  
- IEEE Xplore  
- Science

**Paywall example:** A hit points to a paper on IEEE Xplore that requires login. Agent pauses and sends:

> Retrieval found the paper «Long-range semantic navigation in large indoor environments» which requires access via IEEE Xplore. If you have institutional access, please log in and provide the full HTML or PDF content so I can continue the analysis. If you cannot obtain it, please say whether to skip it.

User either provides content or says "skip". Agent then continues.

### 2.3 Quantity Target

For **Initial survey**, target is **50–80** papers. Example outcome: **67** papers in the initial set. Target met.

### 2.4 Checkpoint 1: Screening Plan Confirmation

Agent sends:

> Initial retrieval found **67** papers from the last three years on "robot long-range navigation". I will apply an evidence hierarchy (top venues, high citation, review papers) to select **18** representative papers for in-depth analysis. Do you have any extra screening conditions? (e.g. exclude certain authors, focus on a specific team.)

**User response (example):** "No, use the default."

Agent then fixes the shortlist (e.g. 18 papers) and moves to Phase 2.

---

## Phase 2: In-Depth Analysis and Interpretation

### 3.1 Shortlist

Using default criteria (citation count, venue tier, relevance) and no extra user conditions, the agent keeps 18 papers for detailed extraction.

### 3.2 Core Information Extraction (Example Entries)

Two example papers, in the format required for Section 4.2:

**Paper A**  
- **Title:** [Example] Learning to navigate in complex environments with topological maps  
- **Authors:** Smith, A.; Jones, B.; et al.  
- **Year/Venue:** 2023, IEEE Trans. Robotics  
- **Core contribution:** Combines learned topological graphs with model-based planning for long-horizon navigation; reduces planning failures in unseen layouts.  
- **Engineering perspective:** Open-source code and benchmark released; dataset available; runtimes reported; suitable for reproducibility studies.  
- **Code/data:** https://example.org/code  
- **IEEE citation:** [1] A. Smith, B. Jones, et al., "Learning to navigate in complex environments with topological maps," IEEE Trans. Robot., vol. 39, no. 2, pp. 512–528, 2023.

**Paper B**  
- **Title:** [Example] Long-range visual navigation without GPS  
- **Authors:** Lee, C.; Wang, D.  
- **Year/Venue:** 2022, IEEE ICRA  
- **Core contribution:** End-to-end policy for multi-kilometer outdoor navigation using only onboard vision; no prior map.  
- **Engineering perspective:** Analysis based on abstract only (full text behind paywall). Abstract source: https://ieeexplore.ieee.org/abstract/...  
- **Code/data:** Not mentioned in abstract.  
- **IEEE citation:** [2] C. Lee and D. Wang, "Long-range visual navigation without GPS," in Proc. IEEE ICRA, 2022, pp. 1–7.

### 3.3 Access Limitations

For Paper B, the agent has only the abstract. The brief states: **"Analysis based on abstract only"** and gives the abstract URL.

---

## Draft Confirmation

Before publishing the final report, the agent sends:

> The draft brief is ready. Before finalizing, do you want to change the grouping, add or remove papers, or adjust the focus of any interpretation?

**User response (example):** "Keep the grouping; add one sentence on real-world deployment for Paper A."

Agent updates the draft and then publishes the **final** brief.

---

## Final Output (Outline)

### 4.0 Title

**Robot long-range navigation — Initial survey**

### 4.1 Executive Summary

This run covered the last three years of literature on robot long-range navigation. Retrieval used five keyword groups across Google Scholar, Semantic Scholar, arXiv, and IEEE Xplore, yielding 67 papers. After evidence-based screening, 18 papers were analyzed in depth. Main findings: (1) trend toward learned topological representations and hybrid planning; (2) growing use of simulation-to-real benchmarks; (3) several open-source codebases and datasets available for reproducibility.

### 4.2 Categorized Selected Papers

*(Tables and short summaries per group; each paper: title+link, core interpretation, code/data links, IEEE citation.)*

**Group: Topological and semantic navigation**  
| Title | Core interpretation | Code/Data | IEEE ref |
|-------|---------------------|-----------|----------|
| Learning to navigate... | Combines topological graphs with planning; code and benchmark released. | [link] | [1] |
| ... | ... | ... | ... |

**Group: Outdoor and long-horizon**  
| Title | Core interpretation | Code/Data | IEEE ref |
|-------|---------------------|-----------|----------|
| Long-range visual navigation... | Abstract only: end-to-end vision-only policy, no GPS. | — | [2] |
| ... | ... | ... | ... |

*(Additional groups as needed.)*

### 4.3 Appendix: Full Initial List

All 67 papers from Phase 1, each with **title** and **URL**, for the user to explore further.

### 4.4 Method Appendix (Reproducibility)

- **Keyword groups:** (list the 3–10 groups used)  
- **Time range:** 2022–2025 (last 3 years)  
- **Databases and dates:** Google Scholar (2025-03-14), Semantic Scholar (2025-03-14), arXiv (2025-03-14), IEEE Xplore (2025-03-14)  
- **Screening criteria:** Top venues (e.g. IEEE Trans., Science Robotics, ICRA/IROS); high citation; include at least one review/survey; target 15–20 papers for deep analysis.

---

## Comparison with Generic Deep Research

| Aspect | Generic deep research | This workflow (engineering literature survey) |
|--------|------------------------|-----------------------------------------------|
| Phases | Clarify → Plan themes → Execute (2 cycles per theme) → Report | Startup (mode+topic) → Phase 1 retrieval → Checkpoint 1 → Phase 2 analysis → Draft confirm → Final brief |
| Checkpoints | 3 (clarification, plan approval, final report) | 2 (screening plan, draft confirmation) |
| Citation | APA 7th | IEEE |
| Output | Long narrative, no bullet/list tables | Structured brief (4.0–4.4), tables and figures encouraged |
| Quantity | Not fixed | 50–80 (initial) or 30–50 (daily) by mode |
| Focus | Any topic, multi-theme | Engineering literature; IEEE Trans, Science Robotics |
