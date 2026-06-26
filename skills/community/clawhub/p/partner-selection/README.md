# 🤝 Partner Selection Skill

**为跨境电子发票合规平台寻找最佳本地通道合作伙伴**

> An AI-powered skill that systematically identifies, evaluates, and recommends local e-invoicing compliance channel partners for any target country — delivering a fully traceable, multi-round filtration report with POC acceptance scripts and negotiation frameworks.

[![Version](https://img.shields.io/badge/version-1.1-blue)]()
[![Tags](https://img.shields.io/badge/tags-E--Invoicing%20%7C%20Tax%20%7C%20Compliance%20%7C%20Partner--Selection-green)]()

---

## 🎯 What This Skill Does

When you're expanding an e-invoicing SaaS platform into a new country and need a **local compliance channel partner** (Access Point, Service Provider, T-VAN, PJAP, etc.), this skill runs a structured 9-step analysis:

```
Step 0  Check knowledge base     → Avoid repeating past decisions
Step 1  Confirm target country
Step 2  Decode regulatory system → Derive qualification thresholds
Step 3  Fetch official registry  → Objective candidate pool
Step 4  Player classification    → Identify structural conflicts
Step 5  Multi-round filtration   → Who's out / who stays / why
Step 6  Reverse falsification    → Stress-test "looks good" candidates
Step 7  Tiered recommendation    → Scored ranking with evidence
Step 8  Go-to-market actions     → BPO definition + POC design + negotiation
```

The output is a **`.docx` report** with full traceability — every elimination is named, every recommendation is scored, every URL is clickable.

---

## 🧩 Skill Structure

```
partner-selection/
├── SKILL.md                                    # Core instructions (417 lines)
├── README.md                                   # This file
└── reference/
    ├── country_regulatory_reference.md         # REF-A: Pre-loaded regulatory data (6 markets)
    ├── partner_scoring_matrix.md               # REF-B: 6-dimension weighted scoring (100-point)
    └── poc_acceptance_scripts.md               # REF-C: POC test scripts (3 markets)
```

---

## 💡 Key Design Principles

### Two Non-Negotiable Bottom Lines

Every analysis starts by declaring two immutable constraints:

1. **Frontend brand ownership stays with us** — Partners must accept a white-label/invisible-pipe role. If a candidate has a competing SaaS frontend, they're eliminated immediately.

2. **BPO fallback capability is mandatory** — Partners aren't just "API vendors" but "tech channel + local compliance safety net" composites. The specific BPO scope varies by market maturity, but the capability itself is non-optional.

### Evidence-Driven, Not Opinion-Driven

- Every candidate mention uses **full legal company names** (no anonymization like "a local SaaS platform")
- Every official registry must be cited with **complete, clickable URLs**
- Every multi-round filter must list **who was eliminated and why** — not just "N candidates remain"
- Scoring uses a **6-dimension weighted matrix** (100-point scale) to ensure reproducible ranking

### Portable Tool References

The skill uses **functional descriptions** (e.g., "use **web search**") instead of binding to specific tool function names, making it adaptable across different AI agent environments.

---

## 🗺️ Pre-Loaded Market Coverage

### REF-A: Regulatory Reference (6 markets)

| Country | Channel Type | Proxy Legal Status | BPO Maturity |
|---------|-------------|-------------------|-------------|
| 🇻🇳 Vietnam | T-VAN | ⚠️ Pending | Low — offline tax bureau visits |
| 🇲🇾 Malaysia | Peppol SP / MyInvois | ✅ Confirmed | Low — LHDN window visits |
| 🇸🇬 Singapore | Peppol AP (InvoiceNow) | ✅ Peppol-native | Medium — data mapping fixes |
| 🇮🇩 Indonesia | PJAP (mandatory) | ⚠️ PJAP-bound | High — DJP relationship network |
| 🇮🇹 Italy | SDI intermediary | ✅ Via Seeburger | High — SLA & API monitoring |
| 🇩🇪 Germany | ZUGFeRD / XRechnung | — | — (follow market) |

### REF-B: Scoring Matrix (6 dimensions)

| Dimension | Weight |
|-----------|--------|
| Official certification level | 25% |
| White-label track record | 20% |
| BPO local response capability | 20% |
| Technical concurrency & stability | 15% |
| Commercial flexibility | 10% |
| Regulatory update notification willingness | 10% |

### REF-C: POC Acceptance Scripts (3 markets)

Pre-built test scenarios for Vietnam, Malaysia, and Singapore, with test IDs (e.g., `T-VN-01`, `C-MY-03`, `B-SG-02`), specific acceptance criteria, and Pass/Fail BPO drills.

---

## 🚀 How to Use

### Trigger Phrases

**Chinese:**
```
帮我找马来西亚的电子发票通道合作伙伴
泰国那边谁做底层通道？
印尼 PJAP 通道选型
完成新加坡市场评估后，怎么接入？
```

**English:**
```
Find an e-invoice local partner for Indonesia
Who should we work with for e-invoicing in Vietnam?
POC design for Malaysia e-invoicing channel
Access point selection for Singapore InvoiceNow
```

### What You'll Get

A `.docx` report named `partner_selection_[country]_[YYYYMMDD].docx` containing:

1. **Regulatory decode** — Authority hierarchy, certification taxonomy, official registry URLs
2. **Full candidate pool** — Complete table with names, certifications, and URLs
3. **Player classification** — Structural conflict map by archetype
4. **Multi-round filtration** — 4 rounds with named eliminations and per-candidate analysis
5. **Reverse falsification** — "Three Sins" framework for borderline candidates
6. **Tiered recommendation** — First-tier / second-tier with weighted scores
7. **Go-to-market playbook** — Localized BPO definition, IaaS+BPO pricing framework, POC test plan, action items with owners and deadlines

---

## ⚙️ Requirements

- **Internet access**: The skill requires web search and URL fetching to verify official registries in real-time
- **File system access**: Reads reference files from the `reference/` directory
- **docx generation**: Uses the `docx` skill (or equivalent) to produce the final report

---

## 📋 Customization Guide

### Adding a New Country

1. **REF-A**: Add a new section to `reference/country_regulatory_reference.md` following the existing template (regulatory authority, channel type, proxy legality, BPO scope)
2. **REF-C**: Add POC acceptance scripts to `reference/poc_acceptance_scripts.md` using the three-tier format (Technical / Capability / BPO Drill)
3. **REF-B**: Review scoring dimensions — if the new market has unique factors, consider adding annotations

### Adjusting the Scoring Matrix

Edit `reference/partner_scoring_matrix.md`. Dimension weights must sum to 100%. The current calibration is optimized for Southeast Asian markets where BPO and white-label are equally critical.

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-04-06 | Added tool abstraction layer, REF-A/B/C indexing system, bilingual triggers, output format spec (`.docx`), Step 4 European market pre-check, output specificity constraints (full URLs, complete candidate tables, per-candidate analysis, real-name-only falsification) |
| 1.0 | 2026-04-06 | Initial release with 9-step workflow, 3 reference files, 6-market regulatory coverage |

---

## 👤 Author

**tangxf** — Built for cross-border e-invoicing platform international expansion.

---

## 📄 License

This skill is provided as-is for use with AI agent platforms. The reference data (regulatory frameworks, scoring matrices, POC scripts) reflects research as of 2026-04 and should be verified against current regulations before production use.
