# Skill Maintenance

Use this reference when updating mpesa-daraja or preparing a ClawHub release.

## Source Update Check

Before changing examples, production guidance, endpoint assumptions, or publishing a new version, check current official sources:

- Safaricom Daraja developer portal: https://developer.safaricom.co.ke/
- The specific Daraja API page for the flow being updated: STK Push, C2B, B2C, Transaction Status, Reversal, or Account Balance.
- Safaricom developer announcements or release notes when available.

Prefer official Safaricom sources over blogs, snippets, or copied SDK examples. If official pages are unavailable, say that clearly in the release notes and avoid making strong claims about changed behavior.

## Versioning

Use semantic versioning:

- Patch: typo fixes, safer wording, small test fixture updates. Example: 1.0.1.
- Minor: new references, scripts, flow coverage, or reusable examples. Example: 1.1.0.
- Major: breaking changes in skill behavior, trigger scope, file structure, or safety policy. Example: 2.0.0.

Always update the version field in SKILL.md before publishing to ClawHub.

## Pre-Publish Validation

Run:

    python3 scripts/scan_skill_safety.py .
    python3 scripts/validate_daraja_fixture.py stk-request path/to/request.json
    python3 scripts/validate_daraja_fixture.py stk-callback path/to/callback.json

Only run fixture validation when fixture files exist. The safety scan should run every time.

## Release Notes Template

    mpesa-daraja vX.Y.Z

    Changed:
    - ...

    Sources checked:
    - Safaricom Daraja portal
    - ...

    Validation:
    - scan_skill_safety.py
    - fixture validation, if applicable

    Notes:
    - No production account values or live payment calls used.

## Publishing Rule

Do not publish externally unless Nevil explicitly asks for a ClawHub push in that turn or the current task clearly includes publishing. If publishing is requested, check sources, bump version, run validation, then publish.
