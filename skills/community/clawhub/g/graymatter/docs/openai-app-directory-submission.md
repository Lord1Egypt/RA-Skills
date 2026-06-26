# OpenAI Apps SDK Submission Notes

## Current OpenAI path

Legacy ChatGPT plugin submission is not the public distribution path. GrayMatter should be submitted as a ChatGPT app through the OpenAI Apps SDK review flow, using the hosted MCP endpoint and the dashboard submission form.

Official references checked on 2026-05-12:

- https://developers.openai.com/apps-sdk
- https://developers.openai.com/apps-sdk/deploy/submission
- https://developers.openai.com/apps-sdk/app-submission-guidelines
- https://developers.openai.com/apps-sdk/reference
- https://developers.openai.com/apps-sdk/guides/security-privacy

OpenAI's current submission flow requires these repository-owned artifacts before account-side submission:

- A deployed HTTPS MCP endpoint, using `/mcp` for ChatGPT connector setup.
- Apps SDK-compatible MCP tool descriptors with accurate names, descriptions, security schemes, annotations, and optional UI resource metadata.
- A content security policy for the app UI resource.
- Public app metadata: app name, logo, description, company URL, privacy policy URL, screenshots, test prompts and responses, and localization details.
- Test credentials for a fully featured demo account with sample data and no inaccessible MFA or signup step.

OpenAI's dashboard-side prerequisites still require human/account action:

- Complete individual or business identity verification for the verified name GrayMatter will publish under.
- Use a project with global data residency.
- Ensure the submitter has `api.apps.write` permission to create drafts and submit for review, plus `api.apps.read` to view draft/review status.
- Provide the real MCP URL, OAuth settings if selected, review credentials, screenshots, test prompts, and confirmation checkboxes in the OpenAI Platform Dashboard.

## GrayMatter readiness

GrayMatter now has the repo pieces needed for an Apps SDK review package:

- `mcp-server/index.js` exposes `POST /mcp`, `resources/list`, `resources/read`, Apps SDK tool metadata, and an overview widget resource.
- `openai-app/submission-manifest.json` records the public, non-secret app metadata for dashboard entry.
- `docs/privacy-policy.md` is the GrayMatter-specific privacy policy URL source.
- `docs/reviewer-test-credentials.md` defines the review demo-account runbook without committing secrets.
- `.codex-plugin/plugin.json`, `assets/logo.svg`, `assets/composer-icon.svg`, and `assets/screenshot.svg` provide local plugin and review asset metadata.

## Submission copy

Title:
GrayMatter

Tagline:
Durable memory and live schema context for business-native agents.

Description:
GrayMatter gives agents durable memory, shared graph context, and authenticated awareness of the live ValkyrAI api-0 schema. It helps Codex and OpenClaw workflows persist decisions, query reusable context, inspect business objects, and coordinate agent state inside an RBAC-scoped business data environment.

Company URL:
https://valkyrlabs.com/

Repository:
https://github.com/ValkyrLabs/GrayMatter

Privacy policy:
https://github.com/ValkyrLabs/GrayMatter/blob/main/docs/privacy-policy.md

MCP endpoint path:
`/mcp`

Test credentials:
Use the secure handoff described in `docs/reviewer-test-credentials.md`. Do not commit credentials to this repository.

The test credentials must unlock a fully featured demo account with sample data and no inaccessible MFA step.

Setup:
Deploy `mcp-server` on a public HTTPS host, set `VALKYR_API_BASE=https://api-0.valkyrlabs.com/v1`, configure the review account token or OAuth bridge, and submit the public `/mcp` URL in the OpenAI Platform Dashboard.
