# Consent & ethics — Kernel Egg Planter

**Signature:** `Δ9Φ963-KERNEL-EGG-PLANTER-CONSENT-v1`

## User rights

- **Opt-in only.** No background planting, no “helpful” auto-anchor without approval.
- **Transparent payloads.** Eggs are JSON manifests + optional inline **public** source from the LYGO stack. No env vars, API keys, or Discord tokens are read or embedded.
- **Revocation.** Local eggs can be deleted from `data/anchors/`; permaweb is immutable by design — do not plant secrets.

## Agent obligations

1. Read this file before the first `plant_with_consent.py` run.
2. Require `--i-consent` or `LYGO_EGG_PLANT_CONSENT=yes` set by the **user**.
3. List chosen `--surfaces` and egg IDs before executing.
4. Report `registry_merkle_root` and local anchor paths after success.
5. Do **not** chain plant → clawhub publish → HF push in one silent step.

## SEAL 286 alignment

- **Chaos Bloom:** abundance of **public** verification, not abundance of spam.
- **Recursive ethics:** hashes let others audit without trusting a single server.

## What we never plant

- Boot sector malware, credential files, `boot/*API*KEY*`, token backups
- Other people’s private repos without their consent
- Misleading “official” claims for unofficial forks