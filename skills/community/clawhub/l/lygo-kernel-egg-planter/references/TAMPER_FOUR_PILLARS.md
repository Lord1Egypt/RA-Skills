# Four pillars (tamper-proof)

1. **SHA-256** — one byte change → new hash  
2. **Merkle registry root** — any egg change → root break  
3. **Anchors** — local CA + optional permaweb; envelope must match blob  
4. **Lattice verify** — `verify_kernel_eggs.py` + lattice gate + badge field `kernel_egg_registry_merkle_root`

**Skill enforcement:** `scripts/verify_eggs.py` after every plant.  
**Retrieve:** stack `retrieve_kernel_egg.py` exit `3` = refuse tampered egg.

Full spec: https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/KERNEL_EGG_TAMPER_LOGIC.md