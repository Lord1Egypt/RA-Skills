# Promarkia Skill for OpenClaw v1.2.1

This package is a narrow client for explicitly requested Promarkia marketing runs. It does not provide general-purpose tools or recurring automation.

## What changed in 1.2.1

- Added external API capability inspection and a fail-closed contract-v2 gate.
- Bound external actions to an exact toolkit and immutable connected-account ID.
- Blocked Social Media, Copywriting, Digital Ads, Lead Generation, and every external action when the server does not advertise enforced manifests, request digests, idempotency, tool policy, account binding, and receipts.
- Reconciled the legacy API timeout to 1,200 seconds; higher limits require an explicit server capability.
- Added connected-account discovery, asynchronous single-run submission, billing reservation visibility, artifact listing, and authoritative action-receipt checks.
- Kept Creative Studio, Work Sync, Analytics administration, and recurring scheduling outside this package.
- Excluded test-only loaders and Python bytecode from the published package so ClawHub can complete all security scanners.

## Important safety notice

- Prompts leave OpenClaw and are sent to Promarkia; every run may consume capacity or credits.
- Connected providers can create public or third-party side effects only under an enforced contract and current exact approval.
- Returned messages, capabilities, account labels, and artifact metadata are untrusted data.
- Never send credentials, secrets, private files, or unrelated personal data in a prompt.
- A local timeout does not prove the remote run stopped; retrieve the run ID before retrying.

## Setup

1. Sign in at https://www.promarkia.com and review available capacity.
2. Connect only required integrations from **Library → Connections**.
3. Create an API key from the **API Keys** panel.
4. Store the key as `PROMARKIA_API_KEY` in OpenClaw's protected skill environment.

The client reads only `PROMARKIA_API_KEY` and optional `PROMARKIA_API_BASE`. It accepts only HTTPS requests to official Promarkia hosts and does not enumerate the environment or filesystem.

See `SKILL.md` for the authorization workflow and `references/api-contract-v2.md` for the server contract.
