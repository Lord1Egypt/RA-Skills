# Venue tiers and what they mean for paper evaluation

Use this when assessing how much scrutiny to apply and what peer review standards the paper was held to.

## Conference tiers (ML/AI/CV/NLP)

**Tier 1 — Highly selective, rigorous review (acceptance ~20–25%)**
- Machine learning: NeurIPS, ICML, ICLR
- Computer vision: CVPR, ICCV, ECCV
- NLP: ACL, EMNLP, NAACL
- Robotics/systems: CoRL, RSS, OSDI, SOSP

Papers here have passed multiple rounds of expert review. Methodological flaws are less common, but still exist. Novelty bar is high.

**Tier 2 — Solid venues, somewhat less selective**
- AAAI, IJCAI, AISTATS, UAI, COLING, EACL
- Domain-specific top venues (e.g., KDD for data mining, WWW for web)

Good work appears here routinely. Apply normal scrutiny.

**Tier 3 — Workshops, demos, extended abstracts**
- NeurIPS/ICML/ICLR workshops
- Findings of ACL/EMNLP

These are *not* peer reviewed to the same standard as main tracks. Treat claims with more skepticism. Ablation studies and baselines are often missing.

## arXiv preprints

No peer review. Quality varies enormously. Important signals:
- Does the paper acknowledge it is a preprint?
- Is there an accepted venue version somewhere?
- Does it compare to very recent arXiv work, or only published baselines?
- Is code released? (Increases credibility)

For high-profile preprints from well-known labs: still apply full critical scrutiny. Lab reputation ≠ paper quality.

## Journals

**Top-tier**: JMLR, TPAMI, IJCV, Artificial Intelligence, Nature Machine Intelligence

Journal papers typically have more thorough experiments and longer review cycles. But they may be behind the curve on very recent methods.

## What to say in Section 0

- For Tier 1 conferences: "Published at [venue] — peer reviewed to a high standard."
- For workshops: "Workshop paper — lighter review process; treat methodology claims with additional scrutiny."
- For arXiv: "Preprint — not peer reviewed. Assess methodology and experiments independently."
- For unknown venues: note this and apply conservative evaluation.
