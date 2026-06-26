# Gougoubi Create Condition

Use this skill when a Gougoubi proposal already exists and the user wants to add one condition from minimal input.

Best for:

- proposal id plus condition title only
- deterministic deadline and trade-deadline defaults
- normalized condition creation payloads

Not for:

- creating a brand-new proposal
- activation, settlement, or reward flows

Typical input:

```json
{
  "proposalId": "0x...",
  "conditionName": "Will Team A win the match?"
}
```
