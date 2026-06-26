---
name: journal-selector
description: "Suggest optimal academic venues for paper submission based on paper content, novelty level, and author's goals. Activated when Chopin asks 'which journal should I submit to', 'help me find the right venue', or shares a draft seeking publication advice. Input: paper draft, abstract, or key contributions. Output: ranked list of 5-8 suitable venues with fit score, rejection risk, review speed, and reasoning. Use when Chopin is deciding where to submit a paper or comparing venues."
---

# Journal Selector

Match papers to the right venue — maximizing acceptance odds and impact.

## Input Needed

Provide one or more of:
- Full paper draft
- Abstract
- Key contributions list
- Current submission status (new / revision / rejected)
- Author preference: speed vs. prestige, theory vs. application, impact factor priority

## Output: Venue Recommendations

For each suggested venue, provide:

| Field | Description |
|-------|-------------|
| **Venue** | Full name + abbreviation |
| **Fit Score** | 1-10, how well paper matches |
| **Match Reasoning** | Why this paper fits this venue |
| **Risk** | Reach / Safe / Safety |
| **Review Speed** | Fast (3-6mo) / Medium (6-9mo) / Slow (9-18mo) |
| **Impact Factor** | If known |
| **Key Concerns** | What might cause rejection here |
| **Strategy Tip** | How to position the paper for this venue |

### Risk Classification
- **Reach:** Top-tier, low acceptance rate, high impact if accepted
- **Safe:** Lower-tier, higher acceptance, less prestige
- **Safety:** Almost certain acceptance, but limited impact

### Review Speed Classification
- **Fast:** Conferences (ICRA, CDC, ACC), some letters journals
- **Medium:** IEEE TIE, TCST, Neurocomputing
- **Slow:** IEEE TAC, Automatica, Springer journals

## Venue Categories for Control/AI Research

### Tier 1 — High Prestige, Low Acceptance
- IEEE Transactions on Automatic Control (TAC)
- Automatica
- International Journal of Robotics Research (IJRR)

### Tier 2 — Strong, Balanced
- IEEE Transactions on Industrial Electronics (TIE)
- IEEE Transactions on Control Systems Technology (TCST)
- IEEE Transactions on Robotics (TRO)
- Systems & Control Letters
- International Journal of Adaptive Control and Signal Processing

### Tier 3 — Applied / Specialized
- IEEE Transactions on Aerospace and Electronic Systems
- Journal of the Franklin Institute
- Asian Journal of Control
- IET Control Theory & Applications

### Tier 4 — Fast Conference Track
- CDC (IEEE Conf. on Decision and Control)
- ACC (American Control Conference)
- ICRA (IEEE Intl. Conf. on Robotics and Automation)
- IROS (IEEE/RSJ Intl. Conf. on Intelligent Robots and Systems)
- ECC (European Control Conference)

### AI / Learning + Control
- IEEE Transactions on Neural Networks and Learning Systems (TNNLS)
- IEEE Transactions on Artificial Intelligence
- Pattern Recognition and Machine Intelligence (PRAMI)

See `references/venue-database.md` for full venue profiles including IF, review speed, scope, and tips.

## Decision Factors

1. **Paper's theory-to-application ratio** — Pure theory → TAC/Automatica; Applied → TIE/TCST
2. **Novelty level** — Incremental → Mid-tier; Breakthrough → Top-tier
3. **Author timeline** — Need publication fast → Conference first; Can wait → Journal
4. **Target audience** — Robotics community → ICRA/IROS; Control theory → CDC/ACC/TAC
5. **Revision history** — Rejected from top? Suggest next-tier before re-review

## Workflow

1. Analyze paper: extract topic, method, contribution strength, application domain
2. Map to venue categories (tier + type)
3. Score fit for 8-12 candidate venues
4. Select top 5-8 with varied risk levels
5. Sort by fit score descending
6. Include reach/safe/safety spread for author choice

## Warning Signs

- Paper is too theoretical for applied journal → expect desk rejection
- Paper lacks experiments for IEEE Transactions → risky
- Novelty is incremental but targeting top-tier → high rejection risk
- Mixing control + learning communities without clear contribution to either → positioning problem

See `references/venue-database.md` for detailed venue profiles.
