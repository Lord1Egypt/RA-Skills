# Agent contract — Excavationpro Music Lattice

**Signature:** Δ9Φ963-EXCAVATIONPRO-MUSIC-AGENT-v1

## Purpose

Give agents one skill to **route, verify, and operate** the Excavationpro music system on the LYGO lattice:

listen portal · catalog ledger · CAS vault · HF streams · live portals · donate · kernel eggs.

## Always do first

1. Read `MUSIC_PORTAL.json` for canonical URLs.  
2. Prefer **sending users** to HTTPS pages over rebuilding tools.  
3. Prefer `portal_status.py` / stack `_verify_listen_portal.py` before claiming health.

## Routing table

| User intent | Agent action |
|-------------|--------------|
| Listen / play free | Open `public.listen` |
| Full ISRC catalog | Open `public.catalog` |
| Hash / merkle / retrieve | Open `public.sovereign_vault` + explain CAS |
| Live stream | Kick / Rumble live / Twitch from `live_portals` |
| Donate | `public.donate_paypal` only |
| “Is the portal up?” | Run `scripts/portal_status.py` |
| Rebuild / rescan | Map to `stack_cli` + confirm stack root |
| Plant egg | Hand off to `lygo-kernel-egg-planter` with consent |

## Never

- Invent stream URLs not in playlist or `hf_stream_base`  
- Auto `git push` or HF publish  
- Confuse DistroKid ban recovery with “music deleted” if HF streams still resolve  

## Lattice language (accurate)

- **Ledger SHA-256** = catalog snapshot integrity  
- **Vault Merkle root** = set of master hashes  
- **HF stream** = public listen copy (not master WAV)  
- **Lattice** = public Pages + registry + eggs, not “on blockchain by default”

## Skill chain

`lygo-tools-portal` → **`lygo-excavationpro-music-lattice`** → `lygo-protocol-stack-operator` → `lygo-kernel-egg-planter` (eggs only)
