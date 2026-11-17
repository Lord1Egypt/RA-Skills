# Multilingual Quality Evaluation

For recorded judgments of meaning, voice, readability, concision, factual support,
and restraint, use the new [independent editorial comparison workflow](editorial-evaluation.md).
`evaluate` below remains deterministic triage; `evaluate-editorial` never generates ratings.

`evaluate` runs a labeled, local JSON case file. The bundled cases under
`tests/fixtures/quality/multilingual-benchmark.json` are **developer-written seed
tests**. They prevent regressions but do not establish real-world accuracy or
native-speaker quality.

```powershell
human-writing-skills evaluate --cases tests/fixtures/quality/multilingual-benchmark.json
```

## Case Schema

Each case needs a unique `id`, `kind`, `language`, `genre`, `review_status`, and
`expected`. The supported kinds are:

- `serious-detection`: add `text`; `expected` is `true` or `false`. Optional
  `document_type` tests an explicit override instead of automatic routing.
- `fidelity`: add `source` and `candidate`; `expected` is `pass-exact`,
  `needs-review`, or `fail-literal`. This measures triage, not an automatic
  determination that a revision preserved meaning.

Use `review_status: seed` for examples made by project contributors. Use
`native-reviewed` only after an independent fluent reviewer checks the language,
genre, intended meaning, and expected result. Such cases must include `reviewer`,
`annotation_date`, and `source_provenance`; use reviewer IDs rather than personal
contact details. Keep licensed or private full texts out of public fixtures.

## Annotation Protocol

1. Sample naturally occurring material by language and genre, including
   fiction, news, formal documents, research, and negative controls that happen
   to contain an academic word, number, dash, or citation. Respect permissions.
2. Ask at least two fluent reviewers to label independently, without showing
   tool predictions. Record disagreements and a separate adjudication decision.
3. For rewrite pairs, mark changed actor, polarity, certainty, scope, attribution,
   chronology, source support, omission, and harmless rewording. Include passages
   where every number and citation remains identical but the meaning changes.
4. Report precision, recall, false positives, and false negatives separately by
   language and genre, with sample counts and confidence intervals where useful.
   Do not pool tiny groups into a global accuracy claim.
5. Rerun after rule changes, including negative controls for deliberate literary
   repetition, formal prose, dialect, code-switching, and intentional ambiguity.

`evaluate` reports the two review-status groups separately and gives per-language,
per-genre counts. A `21/21` result on the bundled seed cases is a smoke-test
result, not a claim of multilingual editorial accuracy.
