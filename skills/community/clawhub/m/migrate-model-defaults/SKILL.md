---
name: migrate-model-defaults
description: Find, classify, and update hardcoded default-like model references in a repo. Use when the user wants to replace model strings, audit model defaults, centralize model constants or workflow variables, or migrate CI/workflow/runtime defaults without bulk-replacing tests, docs examples, catalogs, or compatibility references.
---

# Migrate Model Defaults

## Workflow

Be terse. Minimal prose. Ask only necessary questions.

Ask first:

- Existing model string to replace?
- New model string to use?

Then search for the old string and likely variants:

- If old is `provider/model`, also search bare `model`.
- If old is bare, ask whether to include provider-qualified forms.
- Pay special attention to `.github/workflows/**`; this repo often has workflow defaults in `env`, action `with.model`, and shell args such as `--model`, `--alt-model`, and `--candidate-label`.

Ignore expected noise up front unless it controls default behavior:

- changelog text
- tests and fixtures
- QA mock fixtures and mock catalogs
- provider catalogs and model availability lists
- model capability, compatibility, or alias handling
- generated schema examples
- plain docs examples

Keep only default-like references:

- configured defaults or fallback defaults
- workflow/action defaults
- CI, QA, release, E2E, or smoke default models
- i18n/docs generation defaults
- hardcoded runtime feature defaults

Group candidates semantically, then present a concise checklist with repo-root-relative file refs and one short reason each. Do not edit until the user selects items.

When editing:

- Update only selected items.
- Preserve whether each site expects a bare model id or provider-qualified ref.
- If centralizing repeated workflow defaults, prefer repository variables such as `OPENCLAW_CI_OPENAI_MODEL`, `OPENCLAW_CI_OPENAI_MODEL_BARE`, and an explicit alt-model variable when needed.
- If centralizing source defaults, prefer an existing shared defaults module before adding a new one.
- Ask if string shape or ownership is unclear.

Validation:

- Run the repo-required first pass before searching when applicable.
- For workflow edits, run `actionlint` if available or via `go run github.com/rhysd/actionlint/cmd/actionlint@latest <files>`.
- Run the repo’s changed gate with the correct base. If the default base points at a stale fork, rerun against the real upstream base and report that.
- Scan the touched surface for remaining old-model literals.
