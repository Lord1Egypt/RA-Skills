# Migration notes

## Why this public track exists

The internal/live skill accumulated real runtime state and machine-specific assumptions while being used operationally.

That is acceptable for an internal operator tool, but not for a public ClawHub release.

## Split strategy

Keep the current internal track untouched for production use.

Create and evolve the public track independently.

## Porting rule

Port only these categories from the internal track into the public track:

- generalized scripts
- compatibility checks
- reusable docs
- safe templates
- redaction-safe packaging helpers

Do not port:

- live state
- account snapshots
- callback captures
- backup files
- host-specific unit files
- host-specific module import paths

## Migration progress

Already ported into the public track:

- environment discovery
- doctor checks
- portable runtime inspection
- local slot metadata management
- controlled switch experiment
- rollback helper primitives
- local token ledger / hourly-daily rollup
- release-safe packaging wrapper

## Suggested next implementation phases

1. hardening for switched-write flows (`switch_experiment.py`)
2. portability cleanup for token ledger / usage analytics
3. optional web UI only after dependency discovery is portable
4. optional OAuth web-login support only after absolute host imports are removed
