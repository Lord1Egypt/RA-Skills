# References Map

These docs are organized around the current runtime entry and the layers under `scripts/ima_runtime`:

- `gateway/` covers request entry, routing, and the workflow-confirmation seam.
- `shared/` covers logic reused across the CLI and capability code.
- `models/` covers catalog and create-parameter facts sourced from the backend product list.
- `operations/` covers API contracts and operator playbooks for the active CLI entry.
- `capabilities/video/` covers the only shipped capability in this repo.

Read from gateway to shared policy to capability detail.

Current operator paths:

- structured path: `scripts/ima_runtime_cli.py` -> `cli_flow.py` -> capability/shared runtime
- natural-language path: `scripts/route_and_execute.py` -> `scripts/parse_user_request.py` -> `scripts/validate_params.py` -> `cli_flow.py`

Important shared references:

- `shared/natural-language-routing.md` for wrapper responsibilities and clarification rules
- `shared/catalog-aware-selection.md` for live-catalog-first model selection
- `shared/model-selection-policy.md` for runtime preference order and alias handling

The structure is intentionally layered so `SKILL.md` stays small and active guidance lives next to the layer that owns it.
