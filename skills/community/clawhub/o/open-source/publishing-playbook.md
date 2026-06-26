# Publishing Playbook - Open Source

Use this when launching a new project or releasing a major update.

## Pre-Release Contract

Before publishing, confirm:
- License selected and documented in repository
- README has install, quick start, and troubleshooting basics
- Versioning policy is clear (semantic versioning recommended)
- Security contact and disclosure path are visible
- Contribution and code of conduct files are present

## Release Checklist

| Area | Minimum requirement |
|------|----------------------|
| Build quality | Reproducible build or release artifact generation |
| Docs | Upgrade notes and compatibility constraints |
| Governance | Maintainer ownership and review expectations |
| Distribution | Tagged release, checksums when relevant |
| Communication | Release notes focused on user impact |

## Announcement Template

Ship announcements with:
1. What problem this solves
2. What changed in this release
3. Who is affected
4. How to adopt or upgrade
5. Known limitations and next milestone

## Post-Release Loop

Within 7 days:
- Collect user feedback and failure reports
- Patch critical regressions first
- Update docs for top onboarding confusion points
- Decide whether to fast-follow with a stabilization release
