# Vertex First-Setup Checklist

## Phase 1: Confirm scope

- target project ID is known
- billing / credits are attached to that project
- user wants Vertex AI, not Gemini API direct access
- user wants to avoid accidental extra spend

## Phase 2: Audit current machine

Check for:

- `gcloud` availability
- old `google` / `gemini` / `google-vertex` entries in OpenClaw config
- old Gemini API keys
- old ADC state
- old service-account JSON paths

## Phase 3: Safe auth path

Prefer:

- dedicated service account
- dedicated JSON file
- explicit local JSON path

Avoid claiming success based only on:

- historical browser login
- vague ADC state
- an old working shell session

## Phase 4: OpenClaw model setup

Bias toward:

- `google-vertex/gemini-3.1-pro-preview`
- `google-vertex/gemini-3-pro-preview`
- `google-vertex/gemini-2.5-pro`
- `google-vertex/gemini-2.5-flash`

Avoid:

- `google/...`
- Gemini API direct routes
- mixing provider styles in one “fresh setup” pass

## Phase 5: Verification

Run one tiny request only.

Report:

- provider
- model
- auth method
- target project
- success / failure

## Phase 6: Billing check

Tell the user to verify:

- the line item is under `Vertex AI`
- the correct project is charged
- credits / trial balance applied as expected
