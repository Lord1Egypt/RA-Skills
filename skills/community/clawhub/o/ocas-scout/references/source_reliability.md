# Scout Source Reliability

Benchmarking tools against labeled data so tier assignments and tiered-verification sampling rest on measured accuracy.

## The problem

Scout's tier system assumes some tools are more reliable than others. "Sherlock is good" is a claim; until it is tested against labeled data it is an assumption. `source_reliability.py` turns a labeled corpus into precision, recall, F1, and false-positive rate per tool and per (tool, site) pair.

## Input: a labeled corpus

A JSON list where each item is one labeled observation:

```json
[
  {"tool": "sherlock", "site": "github", "handle": "known_real_user",
   "predicted": true, "actual": true},
  {"tool": "sherlock", "site": "github", "handle": "known_fake_user",
   "predicted": true, "actual": false}
]
```

`actual: true` = the handle belongs to the subject and was correctly found. `actual: false` = the handle does NOT belong to the subject and was a false positive. Build the corpus by scanning handles you know are real (from the subject's own confirmation) and handles you know are fake (random strings, other people's known handles).

## Output

Per-tool and per-(tool, site) metrics: `precision`, `recall`, `f1`, `fpr`, `n` (sample size), `reliable` (n ≥ 20 by default). Tools ranked by F1. Metrics below the minimum labeled count are flagged `LOW N` — they are provisional and must not be cited as measured accuracy.

```bash
python3 source_reliability.py --corpus labeled_corpus.json
python3 source_reliability.py --corpus labeled_corpus.json --tool sherlock --format concise
```

## Using it

1. **Tier assignments.** A tool with F1 < 0.6 on its main sites shouldn't carry Tier 1 status on those sites — move it to Tier 2 with heavier verification.
2. **Tiered-verification sampling (invariant 8).** Low-precision tools need more of their hits verified before feeding synthesis. The `reliable` flag and sample size tell you when a metric can be trusted.
3. **Periodic re-measurement.** Re-run against a frozen corpus when the tool is updated, or quarterly, to detect drift.

## The "no numbers shipped" rule

This script reports nothing until you give it real labels. A reliability figure that was not measured is worse than no figure — it looks like evidence and isn't. Build the corpus first.
