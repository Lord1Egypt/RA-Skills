# Agent contract — lygo-geodesic-sealer

## Allowed without extra human prompt

- `self_check`  
- `status` (local; `--network` only if user asked to connect public lattice)  
- `sign` / `lock` / `attest` / `phase-align` / `verify` to **stdout**  

## Requires explicit user consent

- Any `--write` / `--write-default` of seal artifacts (`--i-consent`)  
- Interpreting seal as authority to publish or plant eggs (pair planter skills)  

## Forbidden

- git push, HF upload, ClawHub publish, social post  
- Live Haven Star Chart write  
- `subprocess` / shell / `os.system`  
- User-controlled fetch URLs  
- Claiming TPM hardware attestation  

## Output discipline

- Prefer JSON stdout  
- Include `signature`, `seal_id` / `lock_id`, `merkle_root` when locking  
- State `collapse: false` when dual amplitudes preserved  

**Δ9Φ963**
