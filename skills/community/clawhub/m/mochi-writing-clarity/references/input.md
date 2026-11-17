# Action contract

lint: file (UTF-8 text); reports generic phrase indicators, long sentences, duplicate paragraphs and fact tokens. compare: before, after (text paths); compares counts of numeric/URL tokens. Does not rewrite automatically or infer semantic correctness. Exact URLs include punctuation as provided; review false positives.

## Request example

```json
{
  "action": "lint",
  "file": "samples/draft.txt"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Do not label writing as AI-generated or promise to evade detectors. Use findings as editorial hints. Verify names, quotations and meaning separately; unchanged numeric tokens are not a semantic accuracy guarantee.
