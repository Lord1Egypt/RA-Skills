# Venue Quality Data

This folder contains optional venue-quality metadata used after real Google Scholar retrieval.

The data is used only for ranking and filtering retrieved papers. It is not used as a discovery source.

## Files

- `journal_scores.json`: journal title to JCR quartile, impact factor, and optional CAS zone.
- `ccf_conferences.json`: conference or journal acronym/full name to CCF rank.
- `eiiRankingName.json`: EI source title map.
- `chinese_journal_tags.json`: Chinese/core journal tags such as CSSCI, 北大核心, 科技核心, and AMI核心.

## Expected Use

```bash
python3 scripts/score_papers.py candidates.json \
  --markdown papers.md \
  --json enriched.json
```

You can replace these files with your own venue-quality data as long as the filenames and JSON shapes stay compatible.
