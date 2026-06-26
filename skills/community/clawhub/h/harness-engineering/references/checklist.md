# Harness Template Checklist

Use this list when evolving an existing repository toward Harness Engineering.

## Core map

- `AGENTS.md` exists and stays short
- `AGENTS.md` points to deeper docs instead of duplicating them
- All referenced docs actually exist

## Source of truth

- Product intent lives in `docs/product-specs/`
- Active implementation work lives in `docs/exec-plans/`
- Tech debt lives in `docs/exec-plans/tech-debt-tracker.md`
- Library-specific notes live in `docs/references/`

## Architecture

- Layer order is explicit
- Boundary rules are written down
- Examples match the declared layer rules

## Enforcement

- Template has a `bun` script for governance checks
- CI runs a real command, not an `echo` placeholder
- Docs do not claim automation that does not exist

## Incremental adoption

- Existing product structure is preserved unless it blocks legibility
- Placeholder artifacts make absence explicit
- New docs explain the current repo, not an imaginary greenfield version

## Verification

- Local validation command runs successfully
- Any residual warnings are documented
