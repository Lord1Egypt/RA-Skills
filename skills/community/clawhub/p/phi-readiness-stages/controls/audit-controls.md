# Audit Controls

Last reviewed: March 17, 2026.

Primary authority pointers:

- HIPAA Security Rule audit controls standard
- HHS Security Rule overview

## Why this domain matters

Logging alone is not enough. PRS requires evidence that logging is enabled where needed and, at higher stages, that logs support monitoring and response.

## Review questions

- Are security-relevant events logged at the workload boundary?
- Are logs retained and protected?
- Are alerts configured for meaningful failures or suspicious activity?
- Is there a review path for production signals?

## Minimum expectations by stage

- PRS-1: audit logging is materially implemented
- PRS-2: logging scope and retention expectations are documented
- PRS-3: monitoring and escalation paths are enabled before cutover
- PRS-4: alert handling and review evidence is current

## Strong evidence

- logging configuration
- SIEM or monitoring integrations
- retention settings
- alert policies
- incident or alert review records

## Common blockers

- logs are emitted but never reviewed
- alerts are disabled in production
- retention is undefined
- integrity of logs is weak or unclear

## Recommended next actions

- document required security event coverage
- define alert ownership and escalation
- retain production alert-review artifacts
