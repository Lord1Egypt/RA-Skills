# Architecture — Sovereign Kernel Seeder

## Layers

```
┌─────────────────────────────────────────────┐
│ Agents (OpenClaw / Hermes / Army / LYRA)    │
│  resolve egg_id → verify → load hooks       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Seeder CLI (stdlib Python)                  │
│  seed_kernel · verify_seed · list_seeds     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Local CAS registry                          │
│  registry.json  +  eggs/*.egg.json           │
│  registry_merkle_root = Merkle(leaves)      │
└─────────────────────────────────────────────┘
```

## Merkle

- Each egg contributes `leaf_hash` (hash of id+version+kind+content_sha256).  
- Leaves sorted, pairwise SHA-256 until root.  
- Odd node duplicated (Bitcoin-style).  

## Atomicity

1. Snapshot registry  
2. Write egg JSON via temp + `os.replace`  
3. Write registry via temp + `os.replace`  
4. Re-verify; on fail restore snapshot + delete new egg  

## Bridge to stack

If `LYGO_STACK_ROOT` set → default root `{stack}/data/sovereign_seeds`  
Classic kernel eggs remain under `data/kernel_eggs/` (planter skill).  
Both may be checked by lattice alignment tooling when wired.  
