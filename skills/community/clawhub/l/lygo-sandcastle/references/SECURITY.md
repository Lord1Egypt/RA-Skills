# SECURITY — LYGO Sandcastle

- Agents must **not** `git push` or ClawHub publish without explicit user consent.
- **Docker/Podman sandboxes** run arbitrary code — only enable with user-approved workflows.
- Do not enable `LYGO_SANDCASTLE_USE_UPSTREAM` on untrusted machines without reviewing upstream `sandcastle-ai`.
- Workflow YAML may contain **prompts with secrets** — never commit sensitive YAML to public repos.
- Kernel egg plant requires `--i-consent` on `workflow_orchestrator_planter.py`.
- Default mode is **dry-run** (no external agent calls).