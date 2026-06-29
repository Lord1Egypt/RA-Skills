# Innovation and Deduplication Assessment Guide

This file guides how to assess novelty and avoid duplicate topics at the topic-selection stage. Load it when performing dedup searches, judging evidence increments, or deciding whether to proceed.

## 1. Why dedup search is required

The cost of a duplicate meta-analysis:
- Wastes research resources
- Increases publication bias (multiple syntheses of the same question can amplify false signals)
- Damages the author's reputation (editors and reviewers dislike "no-increment duplication")
- Most high-quality journals (Lancet, BMJ, JAMA sub-journals, etc.) explicitly reject meta-analyses that heavily duplicate recent publications

## 2. Three-layer deduplication search flow

### Layer 1: PROSPERO search (registered projects)

URL: https://www.crd.york.ac.uk/prospero/

Search strategy:
- Keywords: core intervention name + disease name (no need to add "meta-analysis"; PROSPERO is all systematic reviews by default)
- Search fields: title + abstract
- Time range: all

Decision rules:
| PROSPERO hit | Action |
|---|---|
| No hit | ✅ Strong novelty; proceed |
| Hit but status "Stopped" or "Cancelled" | ✅ Proceed; explain in the background |
| Hit and "Ongoing", registered <6 months | ⚠️ High risk; consider abandoning or focusing on a different subgroup/outcome |
| Hit and "Ongoing", registered 6–24 months | ⚠️ Medium risk; must clearly state the evidence increment |
| Hit and "Completed" but unpublished | ⚠️ Medium risk; contact the registrant to ask about publication status |
| Hit and "Completed" and published | ❌ Usually abandon; convert to an update |

### Layer 2: Cochrane Library search

URL: https://www.cochranelibrary.com/

Search strategy:
- Search both CDSR (Cochrane Database of Systematic Reviews) and CENTRAL
- Search fields: Title/Abstract/Keyword

Decision rules:
| Cochrane hit | Action |
|---|---|
| No hit | ✅ Proceed |
| Hit but Cochrane review published ≥5 years ago | 🟡 Update is reasonable; contact the original Cochrane group for the protocol |
| Hit and published <5 years ago | ❌ Usually abandon; Cochrane reviews carry high authority |

### Layer 3: PubMed published meta-analysis search

Search strategy:
```
(core intervention term[Title/Abstract]) AND (disease term[Title/Abstract]) AND (
  "systematic review"[Publication Type] OR
  "meta-analysis"[Publication Type] OR
  "meta-analysis"[Title/Abstract] OR
  "systematic review"[Title/Abstract]
)
```

Time range: search the full last 5 years.

Decision rules:
| PubMed hit | Action |
|---|---|
| No hit | ✅ Strong novelty |
| 1 hit, published ≥3 years ago | 🟡 Update is reasonable |
| 1 hit, published <3 years ago | ⚠️ Must clearly state the evidence increment (see below) |
| ≥2 hits, all ≥3 years old | 🟡 Integrative update is reasonable; highlight methodological innovation |
| ≥2 hits, including 1 <3 years | ❌ Usually abandon |

## 3. Evidence-increment assessment

When a prior same-topic meta-analysis exists, you must clearly state "what increment my study provides". Increment types, by priority:

### 1. New-study increment (highest priority)
- Since the most recent prior meta-analysis, ≥1 large RCT has been added (sample size ≥500)
- Since the most recent prior meta-analysis, ≥3 small-to-medium RCTs have been added
- Must list the added studies with sample sizes

### 2. New-subgroup increment
- A key subgroup not done by predecessors (e.g., stratified by biomarker, by region, by prior therapy)
- Must specify the subgroup definition and the expected heterogeneity source

### 3. New-outcome increment
- A new outcome not synthesized by predecessors (e.g., a newly reported secondary outcome, long-term follow-up outcome, rare adverse event)
- Must confirm the new outcome has sufficient reporting rate in original studies

### 4. New-methodology increment
- Predecessors did traditional pairwise; you do NMA
- Predecessors did aggregate data; you do IPD meta
- Predecessors did not do dose-response; you do dose-response meta
- Predecessors did not do network ranking; you do SUCRA ranking

### 5. New-data-scope increment
- Predecessors included only English; you include multiple languages
- Predecessors included only RCTs; you include RCTs + high-quality real-world studies
- Predecessors' time range ended in 2020; yours ends at the latest

### 6. New-question redefinition
- Predecessors asked "is A better than B"; you ask "in which subgroup is A better than B"
- Predecessors asked "is it effective"; you ask "what is the optimal dose"

## 4. Increment sufficiency matrix

| Increment type | Sufficient alone? | Note |
|---|---|---|
| New-study (≥1 large RCT or ≥3 small-medium RCTs) | ✅ Sufficient | Strongest increment |
| New-study (1–2 small-medium RCTs) | ⚠️ Borderline | Recommend stacking other increments |
| New-subgroup | ⚠️ Borderline | Subgroup sample size must be sufficient |
| New-outcome | ⚠️ Borderline | New-outcome reporting rate must be sufficient |
| New-methodology | ✅ Usually sufficient | Methodological rationale required |
| New-data-scope | ❌ Not sufficient alone | Must stack other increments |
| New-question redefinition | ✅ Sufficient | Must justify the importance of the new question |

Decision rules:
- Any ✅ increment → proceed
- Only ⚠️ increments, but ≥2 stacked → proceed
- Only 1 ⚠️ increment, or only ❌ → usually abandon

## 5. Dedup report template

After the dedup search, you must output a structured report:

```markdown
## Dedup search report

### 1. PROSPERO search
- Query: [full query]
- Search date: [YYYY-MM-DD]
- Hits: [N]
- Key hits (top 3):
  1. [registration ID] [title] — status: [Ongoing/Completed] — registration date: [YYYY-MM-DD]
  2. ...

### 2. Cochrane Library search
- Query: [full query]
- Search date: [YYYY-MM-DD]
- Hits: [N]
- Key hits:
  1. [title] — publication year: [YYYY]

### 3. PubMed published meta-analysis search
- Query: [full query]
- Search date: [YYYY-MM-DD]
- Hits: [N]
- Key hits (top 5 by relevance):
  1. [PMID] [title] — year: [YYYY] — journal: [Journal]
  2. ...

### 4. Innovation judgment
- Relationship with existing work: [no duplicate / update / integrative update / methodology-innovative]
- Evidence-increment type: [new study / new subgroup / new outcome / new methodology / new scope / new question]
- Increment sufficiency: [sufficient / borderline / insufficient]
- Recommendation: [proceed / hold / abandon]
```

## 6. Common dedup pitfalls

1. **Query too narrow**: only disease + intervention English full name, missing abbreviations and trade names → do keyword synonym expansion
2. **Missing conference abstracts and preprints**: medRxiv, SSRN, Research Square preprints also count as "published"
3. **Non-English databases not searched**: non-English meta-analyses on CNKI, Wanfang, VIP can also constitute duplication
4. **Judging increment by study count only**: ignoring quality difference (1 NEJM RCT increment ≥ several small RCTs)
5. **Overconfidence in "methodological innovation"**: many "new methods" have already been applied by predecessors; verify carefully
6. **Ignoring unpublished PROSPERO registrations**: may be published concurrently at submission, causing conflict

## 7. Non-English database extension search

When the topic meets any of the following conditions, you **must** extend the search to non-English databases:
- Population mainly in non-English-speaking regions or East Asia
- Intervention drug is marketed/approved in non-English-speaking regions
- Researcher plans to publish in a non-English journal or bilingually
- A non-English meta-analysis on the same question is likely to exist (e.g., traditional medicine, region-prevalent diseases)

### Non-English database checklist (Chinese DB example)

| Database | URL | Search fields | Note |
|---|---|---|---|
| CNKI | https://www.cnki.net/ | Topic + keyword + abstract | Journals, theses, conferences |
| Wanfang | https://www.wanfangdata.com.cn/ | Topic + keyword | Journals, theses |
| VIP | http://www.cqvip.com/ | Topic + keyword | Mostly journals |
| SinoMed (CBM) | http://www.sinomed.ac.cn/ | Subject heading + keyword | Chinese biomedical literature; most standardized |

### Query construction (Chinese example)

Template:
```
(core intervention Chinese term OR synonyms OR trade name) AND (disease Chinese term OR synonyms) AND ("Meta 分析" OR "系统评价" OR "系统综述")
```

Example (PD-1 + lenvatinib for HCC):
```
(PD-1 OR 程序性死亡受体1 OR 帕博利珠单抗 OR 信迪利单抗 OR 替雷利珠单抗)
AND (仑伐替尼 OR 乐伐替尼)
AND (肝细胞癌 OR 肝癌 OR HCC)
AND ("Meta 分析" OR "系统评价" OR "系统综述")
```

### Non-English hit decision rules

| Non-English DB hit | Relation to English DB hit | Action |
|---|---|---|
| No hit | English DB also no hit | ✅ Strong novelty |
| No hit | English DB has hit | 🟡 Usually proceed; note "non-English population not synthesized separately" |
| 1 hit, ≥3 years old | — | 🟡 Update is reasonable |
| 1 hit, <3 years old | — | ⚠️ Must clearly state the evidence increment |
| ≥2 hits | — | ❌ Usually abandon, unless there is major methodological innovation |

## 8. Near-duplicate judgment matrix

Exact duplicate (all four PICO elements identical) → handle per the Layer 1–3 matrices above. When only some PICO elements change, it is a "near duplicate", with different rules.

### Near-duplicate definition

Only 1–2 of the four PICO elements change; the rest are essentially identical.

### Near-duplicate judgment matrix

| Near type | Changed element | Counts as duplicate? | Proceed condition |
|---|---|---|---|
| Switch within-class intervention | I (e.g., PD-1 → PD-L1, or between PD-1 agents) | Usually no | Justify the within-class substitution clinically + report a new subgroup (stratified by PD-1 type) |
| Switch dose/duration | I (dose or interval change) | Usually no | Justify the clinical meaning of the dose difference + dose-response subgroup |
| Switch primary outcome | O (e.g., OS → PFS, or add QoL) | Usually no | Justify the clinical value of the new outcome + the new outcome has sufficient reporting rate |
| Switch subgroup population | P (e.g., restrict to Asian, or prior therapy history) | Usually no | Justify the independent clinical meaning of the subgroup + estimate sufficient subgroup sample size |
| Switch comparator | C (e.g., switch SOC) | Usually no | Justify the clinical relevance of the comparator + may trigger NMA |
| Only switch database scope | Database (e.g., add CNKI) | ❌ Yes | Must stack other increments (new study / new subgroup / new methodology) |
| Only switch time window | Time (1–2 years later) | Borderline | Must stack a new-study increment (≥1 large RCT or ≥3 small-medium RCTs) |
| Only switch synthesis model | Methodology (e.g., DL → REML) | ❌ Yes | Not a sufficient increment |

### Near-duplicate handling flow

1. List all near-duplicate works
2. Apply the matrix to each near-duplicate to decide if it counts as a duplicate
3. If all "no" → innovation = "methodology/subgroup innovative"; proceed
4. If some count as duplicate → apply the "increment sufficiency matrix" to decide if the stack is sufficient
5. In the report Section 5, list each near-duplicate work + the judgment

### Common near-duplicate pitfalls

1. **Insufficient within-class justification**: switching PD-1 type without justifying "PD-1 class drugs have similar mechanisms and comparable efficacy" → weak increment
2. **Subgroup sample size not estimated**: restricting to Asian without estimating the number of Asian RCTs → data-availability dimension may be inflated
3. **New-outcome reporting rate not verified**: adding QoL without verifying original studies reported QoL → data-availability dimension may be inflated
4. **Methodological innovation duplicated**: claiming NMA but predecessors already did NMA → increment does not hold
