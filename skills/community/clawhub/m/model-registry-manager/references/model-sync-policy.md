# Model Sync Policy

Use `references/model-sync-policy.json` for sync-time filtering policy.

## Fields
- `allowlist`: when non-empty, only these remote model ids are eligible
- `denylist`: these remote model ids are always ignored

## Rules
- keep provider-native ids
- duplicate remote ids are deduplicated by id
- unusable models are excluded after probe
- allowlist/denylist affects eligibility before registration
- this skill does not choose primary/fallbacks
