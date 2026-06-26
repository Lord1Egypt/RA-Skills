# Eval input files (skill-creator compliant)

Place **input files for evals** here. Paths in `evals/evals.json` are relative to the skill root, e.g.:

```json
"files": ["evals/files/sample.csv"]
```

- If an eval has no input files, `files` is `[]` and this folder stays empty.
- When adding a file, update the corresponding eval entry in `evals/evals.json` with the path under `evals/files/`.
