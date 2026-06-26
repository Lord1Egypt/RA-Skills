---
name: openclaw-vertex-credit-safe-setup
description: Safely configure Google Vertex AI for a fresh OpenClaw setup using a Google Cloud project, service-account JSON auth, minimal-cost verification, and explicit billing checks to avoid accidental Gemini API or extra spend.
version: 1.0.0
---

# OpenClaw Vertex Credit-Safe Setup

Use this skill when a user wants to configure Google Vertex AI for OpenClaw from scratch and wants to minimize billing mistakes.

## Goal

Set up Vertex AI in a way that:

- uses a Google Cloud project
- uses Vertex AI, not Gemini API direct access
- prefers service-account JSON for first-time setup
- keeps model routing on `google-vertex/...`
- validates with one tiny request before wider use
- explicitly checks billing / credits after the test

## Use this skill when

- the machine is a fresh or mostly fresh OpenClaw setup
- the user wants to use Google free credits or trial credits safely
- the user is unsure whether to use ADC, API keys, or service accounts
- the user wants a repeatable first-time setup process
- the user wants to avoid accidental extra spend from the wrong provider path

## Required inputs

- target Google Cloud project ID
- confirmation that billing / credits are attached to that project
- a local path where a service-account JSON file may be stored
- permission to inspect current OpenClaw config files

## Workflow

1. Audit the current machine state.
2. Confirm the target Google Cloud project and billing intent.
3. Prefer a new service-account JSON path for first setup.
4. Configure OpenClaw to use only `google-vertex/...` models for this setup.
5. Run one minimal test request.
6. Tell the user exactly what to check in Google Cloud Billing.
7. Only after billing looks correct should broader rollout happen.

## Guardrails

- Do not present Gemini API direct setup as equivalent to Vertex AI setup.
- Do not say setup is complete before the minimal test.
- Do not say billing is correct unless the user checks the billing console.
- Do not reuse ambiguous old auth state without stating it.
- Do not broaden rollout across many agents until the tiny test is confirmed.

## Preferred first-time auth path

For first-time setup, prefer:

- Google Cloud project
- Vertex AI API enabled
- dedicated service account
- dedicated service-account JSON file

Do not default to:

- Gemini API key
- mixed `google/...` and `google-vertex/...` models
- unclear old ADC state
- “it worked once on this machine” assumptions

## Model routing rules

When configuring models, keep them on the Vertex provider path only:

- `google-vertex/gemini-3.1-pro-preview`
- `google-vertex/gemini-3-pro-preview`
- `google-vertex/gemini-2.5-pro`
- `google-vertex/gemini-2.5-flash`

Do not silently substitute:

- `google/...`
- Gemini API direct routes
- partner-model assumptions when the user explicitly wants the safest likely credit-covered path

## Required report format

Return:

- current machine state
- current Google path in use
- target project
- auth method
- JSON path
- configured `google-vertex/...` models
- minimal test result
- billing checks to perform next

## Reference

For a compact checklist, read [references/vertex-first-setup-checklist.md](references/vertex-first-setup-checklist.md).
