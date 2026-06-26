# Gougoubi Submit Real Results

Use this skill when the user wants to submit Gougoubi condition outcomes from public evidence.

Best for:

- resolved-only settlement first
- full proposal result submission
- forced fallback for pending conditions when explicitly requested

Typical input:

```json
{
  "proposalAddress": "0x...",
  "mode": "resolved-only"
}
```

Script entry:

- `scripts/pbft-submit-results-from-skills-once.mjs`
- `scripts/pbft-submit-all-condition-results.mjs`
- `node scripts/pbft-submit-results-from-skills-once.mjs --help`
- `node scripts/pbft-submit-results-from-skills-once.mjs <proposalAddress>`
- `node scripts/pbft-submit-all-condition-results.mjs <proposalAddress> --result yes --dry-run`
