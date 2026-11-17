# Governance

This document describes how the k12-teacher project is maintained and how decisions are made.

## Roles

| Role | Responsibilities |
|---|---|
| Maintainer | Repository ownership, release management, final review of merged changes, security response |
| Reviewer | Reviews pull requests for quality-gate and constraint compliance (G-01 to G-10, C-01 to C-10) |
| Contributor | Files issues and submits pull requests following CONTRIBUTING.md |

Current maintainer: @JohnSmithfan

## Decision Making

- Routine decisions (bug fixes, documentation updates, test additions) are made through the standard pull request review process. At least one maintainer approval is required before merge.
- Significant decisions (changes to the five-tier capability model, the five-phase workflow, file contracts, or breaking changes) require a dedicated issue with a comment period of at least 5 business days before the change is merged.
- Disagreements that cannot be resolved in review are decided by the maintainer. The rationale is recorded in the related issue.

## Releases

- Versioning follows Semantic Versioning. BREAKING changes increment the major version, backward-compatible features increment the minor version, and fixes increment the patch version.
- The maintainer cuts releases by tagging. Release notes are compiled from CHANGELOG.md.

## Security Response

Vulnerability reports are handled per SECURITY.md. The maintainer is the security contact of record.

## Changes to This Document

Governance changes are proposed by pull request against this file and require maintainer approval.
