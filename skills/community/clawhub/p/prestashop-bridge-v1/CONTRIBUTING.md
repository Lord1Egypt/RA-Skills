# Contributing

## Scope

Contributions must preserve the contract stability of PrestaShop Bridge V1.

## Mandatory rules

- Keep endpoints, headers, and security rules consistent across all files.
- Do not introduce optional JWT algorithms. RS256 is mandatory.
- Do not change the meaning of `202 Accepted`.
- Keep MySQL documented as the source of truth for job status.
- Keep JSON Schemas strict with `additionalProperties: false`.
- Keep examples executable and aligned with schemas.

## Before proposing changes

1. Update `SKILL.md`, `openapi.yaml`, schemas, and examples together.
2. Run the lightweight validator in `validators/validate_examples.py`.
3. Review `docs/publishing-checklist.md`.
4. Verify there are no contradictions between examples and schemas.

## Pull request expectations

Every pull request must include:
- a clear description
- impacted files
- updated examples when contract behavior changes
- updated schemas when payloads change
- updated documentation when operational meaning changes
