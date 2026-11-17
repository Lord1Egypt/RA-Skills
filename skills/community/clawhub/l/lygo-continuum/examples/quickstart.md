# Continuum quickstart (local CLI)

This skill’s **CLI is pure local** — no network, no subprocess.  
An optional **separate** browser portal exists for humans; Continuum never opens it.

```bash
python scripts/self_check.py
python scripts/continuum.py demo
```

## Seal a real task

`claims.json` (paths must be **relative** to `--base`):

```json
[
  {"id": "c1", "kind": "file_exists", "path": "README.md"},
  {"id": "c2", "kind": "file_sha256", "path": "README.md"},
  {"id": "c3", "kind": "file_contains", "path": "README.md", "needle": "Continuum"}
]
```

```bash
python scripts/continuum.py seal --claims claims.json --task "Document continuum" --base . --out capsule.json
python scripts/continuum.py verify --capsule capsule.json --base .
python scripts/continuum.py handoff --capsule capsule.json --verify --base .
```

`--out` must land under `--base` (default cwd), or under skill `state/` with `--i-consent`.  
Operator override: `--i-allow-any-out` (explicit).

## Optional human portal (not the CLI)

If you want a browser witness card (client-side SHA-256, no skill upload):

- https://chatagent.ca/lygo-continuum.html  

Only paste capsules / drop files you are comfortable showing that site.  
**Do not treat the portal as part of the “no network” CLI surface.**
