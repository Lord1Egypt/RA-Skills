# Ledger Auto-Extraction

`extract-ledger` lowers the cost of starting a long-form continuity workflow. It
does not claim to infer canon locally and it does not call a model. Instead, it
compiles a bounded, evidence-first prompt that an attached writing agent can use
to produce a **candidate** ledger for human confirmation.

```powershell
human-writing-skills extract-ledger `
  --draft chapters-01-10.md `
  --context novel-ledger.md `
  --output ledger-extraction-prompt.md
```

Run the resulting prompt with the model used for editorial work. Review its
proposed changes before copying them into the canonical ledger.

## What It Extracts

- character state, carried objects, clothing, injuries, abilities, and resource use;
- promises, debts, open questions, information boundaries, and unresolved pressure;
- occupancy, relative positions, barriers, reach, and explicit movement transitions;
- conflicts and unknowns that must not become canon by omission.

Every extracted entry must carry evidence and one status: `observed`, `inferred`,
`conflicted`, or `unknown`. Existing ledger facts remain authoritative unless the
new manuscript explicitly changes them.

This makes the ledger easier to maintain, but it does not replace editorial
judgment. Confirm evidence, resolve conflicts, then use the approved ledger with
`audit --context`, `pipeline --context`, or `chunk-audit --outline`.
