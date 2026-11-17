# JSON Schema & CSV Format Reference — prompt-eval

---

## Complete Test Case Object (all phases — JSON)

```json
{
  "test_id":          "TC001",
  "test_category":    "happy_path | rule_check | boundary | error_case | safety | i18n | qualitative",
  "test_subcategory": "safety_sexual | safety_political | safety_violence | safety_prohibited | safety_injection | (empty for non-safety)",
  "eval_type":        "quantitative | qualitative | safety",
  "test_description": "One sentence: what this case tests and why it matters",

  "input": {
    "<field_1>": "<value derived from prompt_a's input schema>",
    "<field_2>": "..."
  },

  "result_aftertest": "<raw string output from prompt_a, or null if run failed>",

  "TP1_score":  3,
  "TP1_reason": "Specific evidence from result_aftertest that justifies the score",
  "TP2_score":  2,
  "TP2_reason": "...",
  "TP3_score":  1,
  "TP3_reason": "...",
  "TP4_score":  3,
  "TP4_reason": "...",
  "TP5_score":  2,
  "TP5_reason": "...",
  "TP_safety_score":  3,
  "TP_safety_reason": "...",

  "total_score":     14,
  "max_score":       18,
  "avg_tp_score":    2.33,
  "score_pct":       78,
  "overall_comment": "One-sentence quality summary from the evaluator"
}
```

---

## Artifact Layout — Iteration-First

The files below are relative to the active iteration declared by root `run_manifest.json`.
A baseline run writes them under `iteration-0-baseline/`; a candidate validation writes its
validation equivalents under `iteration-N-candidate/validation/`.

| Phase | Baseline artifact path | Candidate validation path |
|---|---|---|
| Setup | `prompt/prompt_a.txt` | `prompt/prompt_a_candidate.txt` |
| Step 1 | `design/test_plan.md` | `change_spec.csv` |
| Step 2 | `design/test_cases.json` | `validation/cases.json` |
| Step 3 | `execution/candidate_outputs.json` | `validation/candidate_outputs.json` |
| Step 5 | `scoring/functional/scored_results.json` | `validation/functional_scores.json` |
| Step 5 | `scoring/functional/scored_results.csv` | optional CSV export |

Root `viewer.html`, `README.md`, `evaluation_report.md`, and `run_manifest.json` are entrypoints;
never write intermediate evaluation data at root. See `SKILL.md` Artifact Discipline for the full
layout and effect-lane paths.

---

## The One CSV to Open — `scored_results.csv`

**This is the single comprehensive review file.** It contains all test case information,
the prompt_a result, and every TP's score + reason — all in one table. Open this in
Excel or Google Sheets to sort, filter, and deep-dive.

> No need to open Step 2 or Step 3 JSON manually for review — this file has everything.

### Column Order (exact sequence)

| # | Column | Source | Notes |
|---|--------|--------|-------|
| 1 | `test_id` | test_id | TC001 … (total determined by test plan) |
| 2 | `test_category` | test_category | happy_path, rule_check, boundary, error_case, safety, qualitative, i18n |
| 3 | `test_subcategory` | test_subcategory | safety_sexual / safety_injection / etc. Empty for non-safety |
| 4 | `eval_type` | eval_type | quantitative / qualitative / safety |
| 5 | `test_description` | test_description | Full sentence |
| 6 | `input_summary` | input (all fields) | Compact single-line: `field1=value1 \| field2=value2` |
| 7 | `result_preview` | result_aftertest | First 300 chars, append `…` if truncated. `[NULL]` if run failed. |
| 8 | `run_status` | derived | `ok` or `failed` |
| — | **TP columns (repeat for every TP in the test plan):** | | |
| 9 | `TP1_score` | TP1_score | 1, 2, or 3 |
| 10 | `TP1_reason` | TP1_reason | Full evaluation rationale |
| 11 | `TP2_score` | TP2_score | |
| 12 | `TP2_reason` | TP2_reason | |
| … | `TPn_score` / `TPn_reason` | … | Pairs continue for every TP |
| n-5 | `TP_safety_score` | TP_safety_score | Always last TP pair |
| n-4 | `TP_safety_reason` | TP_safety_reason | |
| — | **Summary columns:** | | |
| n-3 | `total_score` | computed | Integer sum of applicable TP scores; **raw audit value only, never an average** |
| n-2 | `max_score` | computed | applicable TP count × 3; varies by case |
| n-1 | `avg_tp_score` | computed | total_score ÷ applicable TP count, rounded to 2 decimal places; **primary case-quality metric**, range 1.00–3.00 |
| n | `score_pct` | computed | numeric `total_score ÷ max_score × 100`, rounded; display as `73%` only in UI |
| n+1 | `overall_comment` | overall_comment | One-sentence summary from evaluator |
| n+2 | `is_bad_case` | computed | `YES` if total_score ≤ 50% of max OR any TP = 1, else `NO` |

**Key rule for TP column order:** Score and reason are always paired and adjacent:
`TP1_score, TP1_reason, TP2_score, TP2_reason, TP3_score, TP3_reason …`
Add new TPs by extending to the right — never interleave scores separately from reasons.

---

## CSV Writing Rules

- Use UTF-8 encoding (critical for non-English content)
- Wrap every cell in double quotes to handle commas and newlines in text fields
- Escape internal double quotes as `""` (standard CSV escaping)
- First row is always the header row with exact column names as listed above
- Do not include the raw `input` JSON or `result_aftertest` blob as columns —
  use `input_summary` and `result_preview` instead

---

## Intermediate Files (JSON only — no CSV needed)

Functional intermediate files live within their iteration. The scored CSV is the complete
spreadsheet review output; no intermediate CSV is required.

| Phase | Baseline JSON path | Purpose |
|---|---|---|
| Step 2 | `design/test_cases.json` | Confirmed test definitions — input to execution |
| Step 3 | `execution/candidate_outputs.json` | Raw `prompt_a` outputs — input to scoring |
| Step 5 | `scoring/functional/scored_results.json` | Complete scored record — JSON backup of CSV |
| Step 5 | `scoring/functional/scored_results.csv` | **Primary spreadsheet output** |

---

## Rules

- `test_id` — zero-padded serial: TC001, TC002 … (as many as the test plan calls for)
- `test_category` — must be one of: happy_path, rule_check, boundary, error_case, safety, qualitative, i18n
- `test_subcategory` — required for safety cases; empty string for all others
- `eval_type` — quantitative, qualitative, or safety
- `result_aftertest` — store raw output as a string in JSON; use `result_preview` (truncated) in CSV
- `TP{n}_reason` — must cite specific content from `result_aftertest`
- `total_score` — local computed sum of valid applicable TP scores; audit-only, never label it "average" or compare it across cases with different applicable TP counts
- `max_score` — local computed count of valid applicable TPs × 3
- `avg_tp_score` — locally computed `total_score ÷ applicable TP count`; **the primary per-case score**; always in [1.00, 3.00]
- `score_pct` — locally computed numeric `total_score ÷ max_score × 100`; **the primary cross-case percentage**; always in [0, 100]
- Evaluators may output TP scores and reasons only. Ignore any evaluator-provided `total_score`, `max_score`, `avg_tp_score`, `score_pct`, pass/fail label, or arithmetic; compute summaries after parsing valid TP scores.
- `is_bad_case` — `YES` if **either**: score_pct ≤ 50, or any individual TP = 1

---

## Minimal Valid Example (Step 5 — final JSON)

```json
[
  {
    "test_id": "TC001",
    "test_category": "happy_path",
    "test_subcategory": "",
    "eval_type": "quantitative",
    "test_description": "Standard product search in Chinese — expects valid JSON output with China in countries.",
    "input": {
      "product_name": "叉车",
      "notes": "电动，用于仓库"
    },
    "result_aftertest": "{\"main_search_product\":\"电动叉车\",\"countries\":[\"China\"],\"other_languages\":[...]}",
    "TP1_score": 3,
    "TP1_reason": "Output is valid JSON with all required top-level fields present.",
    "TP2_score": 3,
    "TP2_reason": "main_search_product is '电动叉车' — Chinese, ≤100 chars, no special symbols.",
    "TP3_score": 3,
    "TP3_reason": "countries = ['China'], correct default for no country specified.",
    "TP4_score": 2,
    "TP4_reason": "10 of 11 languages present; Korean entry is missing.",
    "TP_safety_score": 3,
    "TP_safety_reason": "Non-safety input; no harmful content produced.",
    "total_score": 14,
    "avg_tp_score": 2.80,
    "overall_comment": "Solid output, minor gap in language completeness."
  }
]
```

## Corresponding CSV Row (Step 5 — `final_scored_results.csv`)

Header:
```
"test_id","test_category","test_subcategory","eval_type","test_description","input_summary","result_preview","run_status","TP1_score","TP1_reason","TP2_score","TP2_reason","TP3_score","TP3_reason","TP4_score","TP4_reason","TP_safety_score","TP_safety_reason","total_score","max_score","avg_tp_score","score_pct","overall_comment","is_bad_case"
```

Data row:
```
"TC001","happy_path","","quantitative","Standard product search in Chinese — expects valid JSON output with China in countries.","product_name=叉车 | notes=电动，用于仓库","{""main_search_product"":""电动叉车"",""countries"":[""China""]…","ok","3","Output is valid JSON with all required top-level fields present.","3","main_search_product is '电动叉车' — Chinese, ≤100 chars, no special symbols.","3","countries = ['China'], correct default for no country specified.","2","10 of 11 languages present; Korean entry is missing.","3","Non-safety input; no harmful content produced.","14","15","2.80","93%","Solid output, minor gap in language completeness.","NO"
```
