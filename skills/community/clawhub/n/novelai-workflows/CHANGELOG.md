# Changelog

## Unreleased

- Fixed strict YAML parsing of all three Skill frontmatter descriptions by quoting values containing colon-space sequences.
- Synchronized the main Skill and strict Free variant with the Opus Free same-session billing-profile reuse and bounded transient retry policy.
- Added versioned updates for the main Skill (`0.1.2`) and strict Free variant (`0.1.1`).
- Added up to three sequential retries for transient Opus Free image-operation failures while preserving exact parameters and billing safeguards.
- Improved the Opus Free variant to reuse a verified zero-Anlas billing profile throughout the same session while parameters remain unchanged.
- Added the local `openclaw-novelai-free` zero-Anlas policy variant under `variants/`.
- Added the local `openclaw-novelai-opus-free` Opus enhancement variant with the latest live-tested zero-Anlas boundaries.
- Updated cost documentation to distinguish official rules, empirical account tests, and conservative policy blocks.

## 0.1.1 - 2026-09-06

- Added Chinese and English cost/quota guides for NovelAI Anlas, Opus free images, and V5 usage limits.
- Linked the cost/quota guides from both README files and both user manuals.
- Clarified that the V5 daily image figure is a dynamic refill rate, not a fixed daily grant.

## 0.1.0 - 2026-09-05

- Initial public OpenClaw Skill for NovelAI story and image workflows.
- GitHub repository: `techotaku39/openclaw-novelai`; ClawHub slug: `novelai-workflows`.
- Added bounded story context and secret-safe generation records.
- Added current API smoke-test harness for text and image capabilities.
- Added Chinese user documentation and an English project README.
- Pinned the reference NovelAI Image MCP deployment to `0.4.0`.
