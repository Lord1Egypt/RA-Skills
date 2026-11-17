# Independent Editorial Evaluation

Use `critique` for diagnosis without replacement prose, or `compare-blind` to
randomize two versions. Supply the reader's purpose and authoritative material in
`--brief`. Give reviewers only `comparison.md`, with no revision history or version
key. Record independent ballots before unblinding; allow ties and insufficient evidence.
Neither draft is a factual authority when sources are absent.

`evaluate-editorial --cases ballots.json` aggregates recorded judgments and exposes
disagreements. It never calls a model or invents annotations. Each case needs
`id`, `language`, `genre`, `review_status` (seed/native-reviewed), `version_key`
mapping A/B to original/candidate, and `ballots`. Each ballot needs `reviewer`,
`annotation_date`, `verdict` (A/B/tie/insufficient-evidence), and `scores` for A and B.
Score all six dimensions 0–4, higher being better:

| Dimension | Assessment |
| --- | --- |
| meaning | Original meaning, uncertainty, and scope against authoritative material |
| voice | Evidenced author/speaker habits and intent |
| readability | Comprehension and target-language register |
| concision | Avoidance of padding without harmful omission |
| factual_support | Support for claims and details |
| restraint | Avoidance of forced texture, melodrama, or rhetorical recipes |

Use 0 for severe defects, 2 for mixed quality, and 4 for no material defect found.
Use insufficient-evidence when material cannot support a judgment; numbers do not
override this verdict. Do not judge voice without samples or factual support without
sources. Empty ballots are pending. Native-reviewed cases require two distinct fluent
reviewers and source_provenance; this is an attestation, not identity verification.
Keep results separate by language, genre, and review status, and resolve disagreements.

```json
[
  {
    "id": "zh-essay-pending", "language": "zh", "genre": "essay",
    "review_status": "seed",
    "version_key": {"A": "original", "B": "candidate"},
    "ballots": []
  }
]
```

A recorded ballot has this shape (numbers are schema examples, not real results):

```json
{
  "reviewer": "reviewer-01", "annotation_date": "2026-10-13", "verdict": "tie",
  "scores": {
    "A": {"meaning": 2, "voice": 2, "readability": 2, "concision": 2, "factual_support": 2, "restraint": 2},
    "B": {"meaning": 2, "voice": 2, "readability": 2, "concision": 2, "factual_support": 2, "restraint": 2}
  }
}
```

Start with Chinese, English, Japanese, and Spanish across factual articles and fiction.
Include formal prose, dialect, intentional repetition, ambiguity, and direct emotional
labels as negative controls. Compare ordinary rewriting and project-guided rewriting
against the same original in separate blinded cases. Keep private keys and drafts out
of public reports unless publication is authorized. No native-reviewed editorial
results are bundled yet; collect them before making real-world improvement claims.
