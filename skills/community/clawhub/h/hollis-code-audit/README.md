# Code Audit Skill

Cross-agent code audit workflow for repo, PR, security, regression, and intent-alignment reviews.

Use `SKILL.md` as the primary instructions. Helper scripts are optional and use only the Python standard library.

## Portable Usage

Replace `<skill-dir>` with the directory containing `SKILL.md`.

```bash
python <skill-dir>/scripts/audit_snapshot.py --root . --json
python <skill-dir>/scripts/detect_review_models.py --current-model "<model-if-known>"
python <skill-dir>/scripts/detect_review_models.py --config <skill-dir>/review_routes.example.json
python <skill-dir>/scripts/build_audit_packet.py --root . --mode standard --scope diff
python <skill-dir>/scripts/build_audit_packet.py --root . --mode standard --scope diff --producer-agent "other-agent" --prior-review review.md
python <skill-dir>/scripts/run_tests.py
python <skill-dir>/scripts/run_evals.py
```

Use `python3` instead of `python` when required by the environment.

If Python or git is unavailable, follow the manual flow in `SKILL.md`: read project intent docs, inspect the requested scope, disclose independent-review availability, and report evidence-backed findings.

When auditing another agent's code, treat prior agent plans/reports as evidence, keep outputs separate, and resolve disagreements by local code, tests, docs, and user goals.

## Modes

- `quick`: current diff/status only.
- `standard`: intent docs, requested scope, adjacent contracts/tests.
- `security`: auth, permissions, paths, secrets, LLM/network, logs.
- `deep`: broader repo risk map and test strategy.
- `intent`: alignment with README/AGENTS/product purpose.

## Optional Files

- `.auditignore`: repo-local ignore patterns for noisy/generated/confidential files.
- `.codex/skills/code-audit/config.json`: local preferences copied from `config.example.json`.
- `<skill-dir>/review_routes.json`: local custom reviewer routes copied from `review_routes.example.json`.
