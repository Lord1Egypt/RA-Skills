# Hermes Agent compatibility

The read-only adapter was verified against NousResearch/hermes-agent commit
`d7b836ab1c0cddaafc109ed24c9a83b6191cdc88`.
Source: https://github.com/NousResearch/hermes-agent/tree/d7b836ab1c0cddaafc109ed24c9a83b6191cdc88

Maintainer integration: `python3 tools/test_hermes_compat.py --source /path/to/pinned/checkout`.
This creates an isolated temporary profile using the actual upstream cron.jobs parse/save
functions, audits the resulting files, and verifies every profile file remains unchanged.
No scheduler, job script, provider authentication or paid inference is run.

Inputs: explicit profile config.yaml and cron/jobs.json, or JSON/YAML config plus JSON jobs export.
Missing selected files fail instead of reporting an empty successful audit. The adapter does
not import Hermes, search profiles, read .env or resolve profile overlays. Ambient HERMES_MODEL
is ignored; pass its known non-secret value with --hermes-model-env if needed.

Model order follows upstream cron scheduler: job.model, cron.model, model_snapshot,
explicit environment, global model.default (or model string). Provider evidence follows
job.provider, cron.model_provider, provider_snapshot, global model.provider. Actual auth,
aliases, runtime overrides and fallbacks remain unverified.

The skill format uses SKILL.md. Preserve its scripts and references when installing.
OpenClaw native commands are never invoked for a Hermes audit. JSON needs standard-library
Python 3.10+; YAML additionally needs PyYAML, loaded with safe_load. Nothing is auto-installed.

No native catalog/auth/usage ingestion, automatic configuration changes or guaranteed savings.
Reports omit raw prompt/script/config content; selected identifiers can still be sensitive.
