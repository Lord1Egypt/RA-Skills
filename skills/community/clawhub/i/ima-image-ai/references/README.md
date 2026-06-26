# References Map

These docs are organized around the active runtime entry and the layers under `scripts/ima_runtime`:

- `gateway/` covers request entry, routing, and clarification seams.
- `shared/` covers reusable policy and cross-cutting runtime rules.
- `operations/` covers API lifecycle, smoke checks, and troubleshooting playbooks.
- `capabilities/image/` covers image-specific behavior, model rules, parameter tuning, and scenarios.

Read from gateway to shared policy to image capability detail. That follows the intended runtime path from `scripts/ima_runtime_cli.py` into `cli_flow.py`, then through shared services, and finally into `capabilities/image/*`.

Useful operator-facing docs:

- `operations/api-contract-and-errors.md` for request lifecycle and timeout contracts
- `operations/e2e-smoke-playbook.md` for local and live smoke checks
- `operations/troubleshooting.md` for common failures and copy-paste recovery commands
- `shared/catalog-aware-selection.md` for the formal dynamic model-selection contract
- `../capabilities/image/references/parameter-tuning.md` for practical control combinations
- `../capabilities/image/references/scenarios.md` for concrete prompt-only and reference-image examples
