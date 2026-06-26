# Release notes 0.1.0

## Summary

First public release candidate of `openai-auth-switcher-public`.

This version focuses on **safe publication, portability, and operator clarity**, not on bundling every internal feature from the live/private skill.

## Included in 0.1.0

- environment discovery (`env_detect.py`)
- compatibility doctor (`doctor.py`)
- portable runtime inspection (`inspect_runtime.py`)
- slot metadata management (`profile_slot.py`)
- controlled switch experiment (`switch_experiment.py`)
- rollback helper (`rollback_experiment.py`)
- local token ledger rebuild (`token_ledger.py`)
- hourly / daily usage rollup payload (`hourly_usage.py`)
- release-safe packaging wrapper (`package_public_skill.py`)
- public static web assets for release presentation

## Deliberately excluded from 0.1.0 core promise

- machine-bound OAuth web login flows
- machine-bound live web service runtime behavior
- absolute host-path imports tied to one operator machine

## Compatibility wording for publication

Recommended listing wording:

- Tested on OpenClaw `2026.3.11`
- Tested on Python `3.11`
- Tested on Node.js `22.x`
- Linux-first public release

## Safety statement

This skill is intended for administrators who understand that OpenAI OAuth switching is a credential-adjacent operation.

The public release must be packaged without live tokens, callbacks, backups, or machine-specific runtime state.
