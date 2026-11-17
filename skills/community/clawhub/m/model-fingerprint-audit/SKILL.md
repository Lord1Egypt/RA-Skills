---
name: model-fingerprint-audit
description: Audit OpenAI-compatible or Anthropic-compatible model endpoints using repeated behavioral probes, stability metrics, and reference fingerprints. Use when checking whether a proxy model is stable or plausibly matches its claimed identity.
---

# Model Fingerprint Audit

Use repeated, synthetic probes to assess endpoint stability and compare behavior with a trusted reference fingerprint.

## Workflow

1. Ask for the endpoint, API format, model IDs, and a local API key source. Never place real keys in this skill, reports, or published files.
2. Run a low-cost pilot first (4 repetitions) to verify authentication and response validity.
3. For an authorized full audit, run 16 repetitions per model with bounded concurrency. Record total requests, failures, latency, returned model IDs, usage fields, empty responses, and probe distributions.
4. Compare against a trusted reference fingerprint for the same model/version. A model name returned by the proxy is evidence only, not identity proof.
5. Apply these labels:
   - **符合**: at least 95% requests succeed, sufficient shared probes with a trusted reference, and nearest fingerprint is the claimed model or same family.
   - **可疑**: failure rate above 5%, major cross-run drift, or nearest fingerprint consistently belongs to another family.
   - **无法判断**: stable endpoint but no trusted reference or insufficient shared probes.
6. Report evidence and limits. Do not call a model fake solely because the reference library lacks it.

## Privacy and cost

Keep keys in environment variables or local ignored files. Do not print them. Use synthetic prompts only. Because each probe consumes quota, obtain authorization before full runs and avoid uncontrolled concurrency.

Read [references/baseline-sources.md](references/baseline-sources.md) when a reference fingerprint is missing or must be collected.\n\n## Plan and endpoint separation

Treat subscription or coding-plan quota as a separate resource from standard PaaS API balance. A key that works in Claude Code, OpenCode, or another coding tool may still receive `1113` (insufficient balance or no resource package) at the standard PaaS chat-completions endpoint. Do not use that key or its plan dashboard as a trusted model fingerprint baseline. Record the resource type and endpoint in every report.

## Baseline caching

Collect a trusted provider fingerprint once, then store the sanitized fingerprint artifact locally and reuse it for later proxy audits. Routine audits must not call the official model again. Never store the API key or raw private responses in the artifact.

Refresh the baseline only when the provider changes the model version, tokenizer, system behavior, API format, sampling settings, or when a scheduled drift check is due. Label every comparison with the baseline model version, provider, collection date, and probe-set version. If the baseline provenance is missing or stale, downgrade the result to `无法判断` instead of silently treating a new sample as truth.
## Community contributions

Contributors may add provider adapters, probe normalizers, reference fingerprints, and anonymized result fixtures. Never commit real API keys, private prompts, cookies, or raw user conversations. Every reference fingerprint must record its provider endpoint, model ID, collection date, request format, sampling parameters, and provenance. Run secret scanning and validation before submitting a release.
## Suggested implementation

The open-source `llm-fingerprint` project can be used as the probe engine:
https://github.com/dreamor/llm-fingerprint

For broader compatibility checks, use:
https://github.com/RuizhangZhou/CompatBench
