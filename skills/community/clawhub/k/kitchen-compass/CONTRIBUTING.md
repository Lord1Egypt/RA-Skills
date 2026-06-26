# Contributing to Kitchen Compass

Thanks for opening a contribution. This project is small and opinionated; the rules below exist because prior changes have bitten us.

## Ground rules

1. **The recipe schema is frozen.** Do not add, remove, or rename fields in `scripts/contract.py` or `references/recipe-schema.md`. If a change seems to require a schema change, open an issue before sending a patch.
2. **`scripts/contract.py` and `references/recipe-schema.md` must stay aligned.** Any change to one requires a matching change to the other in the same commit. `tests/test_contract_alignment.py` enforces this.
3. **Planner scoring is not to be changed casually.** Presets, weights, hard constraints, and history/inventory math in `scripts/build_weekly_plan.py` (and the `scripts/planner/` package) are intentional. Restructuring is fine; changing behavior is not. Capture a scoring decision in a commit message *before* adjusting it.
4. **Preserve the authored-vs-generated boundary.** Nothing under `generated/` is an input. Every file there must be rebuildable from authored sources.
5. **Do not ship real household data inside the skill.** Sample content under `assets/sample-household/` uses placeholder values only.

## Dev setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Pre-PR check

```bash
make test   # pytest
make smoke  # full CLI smoke test
```

Both must pass before opening a PR.

## Commit style

- One task per commit.
- Commit message explains *why*, not what.
- Co-authored commits from tooling are fine; keep the trailer format.
