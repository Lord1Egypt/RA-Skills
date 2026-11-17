# Agent contract — Layer C v1.1

1. Only activate for **explicit** public verify / external sync / star map / manifest jobs.  
2. Require trusted `LYGO_STACK_ROOT` (never invent a random path).  
3. Prefer **zero-write verify** first: `verify_world_lattice.py` / `verify_public_anchors.py` with no extra flags.  
4. Use `--write-report` only when the user wants `tests/*_last_run.json` persisted.  
5. Do **not** pass `--refresh-local` or `--build-manifest` unless the user asked to rebuild local docs; always pair with `--i-trust-stack`.  
5. Never auto-publish (git / HF / ClawHub / social).  
6. Snapshot: only with user `--i-consent` this turn.  
7. On LOCAL_QUARANTINE — stop all external steps.  
8. On PUBLIC_DEGRADED — report URLs; do not rewrite local eggs from public.  
9. Cite verdict JSON path + local vs public note.  
10. Do not use shell wrappers; call skill scripts with Python only.  
