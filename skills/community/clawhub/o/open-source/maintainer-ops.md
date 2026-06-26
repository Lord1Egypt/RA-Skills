# Maintainer Ops - Open Source

Use this for ongoing maintenance of open source projects.

## Weekly Cadence

1. Triage issues by impact and reproducibility.
2. Review open pull requests with explicit acceptance criteria.
3. Process dependency and security updates.
4. Update roadmap and communicate current priorities.

## Monthly Cadence

1. Ship a stable tagged release.
2. Publish concise user-facing changelog.
3. Review contributor experience bottlenecks.
4. Validate documentation against real onboarding flow.

## Issue Triage Buckets

| Bucket | Meaning | SLA Target |
|--------|---------|-----------|
| critical | Data loss, security, production breakage | same day |
| high | Core workflow broken, no workaround | 2-3 days |
| normal | Quality issues with workaround | 1-2 weeks |
| backlog | Nice-to-have or low signal | scheduled review |

## PR Review Rules

- Require reproducible context for non-trivial fixes.
- Reject drive-by complexity without operational justification.
- Prefer minimal surface-area changes tied to tests or evidence.

## Deprecation Hygiene

When removing behavior:
- Warn in at least one prior release when possible.
- Provide migration path and timeline.
- Document explicit breakage scenarios.
