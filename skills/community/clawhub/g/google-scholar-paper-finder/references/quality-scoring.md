# Quality Scoring

Use relevance first and venue quality second. Quality scoring starts only after papers have been retrieved from Google Scholar MCP.

## Local Data Sources

Quality data is optional but recommended. Put these files in the skill's `data/` folder, set `SCHOLAR_QUALITY_DATA_DIR`, or pass `--data-dir` to `scripts/score_papers.py`.

- `journal_scores.json`: English journal name -> `name`, `quartile`, `if`, optional `csa_zone`.
- `ccf_conferences.json`: conference/journal acronym or full name -> `A`, `B`, `C`.
- `eiiRankingName.json`: EI source title -> `EI`.
- `chinese_journal_tags.json`: journal name -> tags such as `CSSCI`, `北大核心`, `科技核心`, `AMI核心`.

If these files are unavailable, keep the paper in the candidate table, leave quality fields empty, and mark the venue as `unknown venue`.

## Venue Matching

Normalize venue names before matching:

- lowercase;
- strip punctuation;
- decode `&amp;`;
- replace `and`/`&` consistently;
- collapse whitespace;
- compare exact normalized names first;
- for Chinese journal names only, allow conservative substring matching when both strings contain CJK characters and the quality-data key is long enough to avoid accidental matches.

Avoid broad fuzzy matching for English acronyms and journal names. It can create false positives, especially when a short acronym appears inside an unrelated venue title.

Do not delete papers only because a venue is unmatched. Mark `unknown venue`.

Do not create venue metrics from memory. If a venue cannot be matched to local JSON data, leave IF/rank fields empty or `unknown`.

## Default Output Size

For normal searches, return the top 50 deduped Google Scholar papers after ranking. If the candidate pool has more than 50 records, keep the full pool internally but show the best 50. If fewer than 50 records are available, report the actual count and why expansion stopped.

## Quality Signals

Strong signals:

- CCF A;
- JCR Q1;
- CAS zone 1;
- CSSCI;
- 北大核心;
- high-impact journal in `journal_scores`.

Good signals:

- CCF B;
- JCR Q2;
- CAS zone 2;
- EI;
- 科技核心;
- AMI核心.

Weak or unknown signals:

- no venue match;
- unclear proceedings;
- missing venue;
- source title does not map to known data.

## Recommendation Tiers

Use:

- `Core`: high relevance + strong source quality.
- `Priority`: relevant + good source quality.
- `Reference`: relevant but source quality unknown/modest.
- `Check`: promising but missing abstract/venue/access information.
- `Remove`: weak relevance or not useful for the user's question.

## Sorting Order

Sort within the final table by:

1. recommendation tier;
2. relevance score;
3. venue quality score;
4. Google Scholar citation count;
5. publication year.

This prevents famous but weakly related papers from outranking directly relevant papers, while still rewarding authoritative venues and highly cited work.

## Reason Templates

Use concise reasons:

- "Highly relevant to the topic; Q1 journal and CAS zone 1."
- "Relevant method paper; CCF A conference."
- "Useful background review; high citation count but venue unmatched."
- "Potentially relevant from title only; abstract needs manual check."
- "Venue quality is strong, but topic fit appears weak."
