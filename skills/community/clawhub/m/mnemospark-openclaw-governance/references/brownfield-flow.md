# Brownfield discover flow

Use on existing governance repos with hand-authored `registry.yaml` and runbooks.

## Flow

```
discover (read-only summary)
    │
    ├─ inventory only ──► discover --inventory
    │                      └── workflows/discovered-inventory.json (schema v2)
    │
    └─ review + promote ──► discover --staged
                              ├── discovered-inventory.json
                              └── discovery-candidates.json
                                    │
                                    ▼
                            review candidates (human or agent)
                                    │
                                    ▼
                            discover --promote [--allowlist]
                              └── registry.yaml (only on semantic diff)
```

## Rules (v0.5.3+)

- `discover --promote` does **not** overwrite curated `agents` or `raci_domains`
- Protected rows (`active`, `required`) keep hand-edited fields
- `--allowlist` limits promotion to listed workflow ids
- Plain `discover --write` is legacy immediate merge — prefer staged + promote on brownfield

## Allowlist format

JSON array or `{"workflow_ids": ["id1", "id2"]}`.

```bash
openclaw-gov discover --promote --allowlist allowlist.json --root "$GOV_ROOT"
openclaw-gov regen --write --root "$GOV_ROOT"
openclaw-gov check --root "$GOV_ROOT"
```

## CI safety

After `discover --staged`, registry must be unchanged:

```bash
git diff --exit-code workflows/registry.yaml
```

## Fan-out crons

Jobs with same agent/name/schedule but different payloads are **related instances**, not duplicates. Check `cron_instance_groups` in JSON for `kind: fan_out`.
