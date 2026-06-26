# Manual Review Template

```md
# GwapScore Manual Review

Wallet: {{wallet}}  
Trigger: {{trigger}}  
Severity: {{severity}}  
Created: {{isoTimestamp}}  

## Summary

{{summary}}

## Evidence

- Signature: {{signature}}
- Program ID: {{programId}}
- Counterparty: {{counterparty}}
- Slot: {{slot}}
- Timestamp: {{isoTimestamp}}

## Current Score State

- Score before review: {{scoreBefore}}
- Temporary cap: {{temporaryCap}}
- Confidence: {{confidence}}

## Reviewer Decision

Decision:

- [ ] clear
- [ ] monitor
- [ ] cap
- [ ] severe_cap
- [ ] dispute_required
- [ ] confirmed_bad_actor

## Notes

{{reviewerNotes}}

## Resolution

{{resolution}}
```
