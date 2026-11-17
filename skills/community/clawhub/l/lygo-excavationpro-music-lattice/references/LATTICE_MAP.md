# Excavationpro music × LYGO lattice map

```text
                    ┌─────────────────────────────┐
                    │   Eternal Haven / LYGO      │
                    │   Pages · Stack · Eggs      │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌──────────────┐      ┌────────────────┐      ┌─────────────────┐
   │ Listen Free  │      │ Catalog Ledger │      │ Sovereign Vault │
   │ (player+SEO) │      │ ISRC + albums  │      │ SHA-256 Merkle  │
   └──────┬───────┘      └───────┬────────┘      └────────┬────────┘
          │                      │                        │
          └──────────┬───────────┴──────────┬─────────────┘
                     ▼                      ▼
            HF public streams        Local masters (CAS)
            160kbps MP3              MUSIC_VAULT / J: / I:\Actors
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Kick / Rumble / Twitch    PayPal support
   live discovery            ca-pub AdSense (consent)
```

## Identity layers

| Layer | Artifact | Public? |
|-------|----------|---------|
| Commercial title / ISRC | DistroKid restore + ledger | yes (metadata) |
| Content hash | `sha256` per master | yes (hex) |
| Stream | `stream/{sha256}.mp3` on HF | yes (audio) |
| Catalog root | `ledger.content_sha256` | yes |
| Vault root | `merkle_root` | yes |
| Kernel egg | `excavationpro-music-*-v1` | metadata only |

## Operator loop (steward machine)

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack

# 1 Hash / merge new folders (e.g. I:\Actors)
python tools/build_music_cas_vault.py --scan --root "I:\Actors" --hub

# 2 Encode streams (skips existing)
python tools/build_public_music_stream.py --encode --workers 4

# 3 Publish + rebuild player (consent)
python tools/build_public_music_stream.py --publish-hf --hub

# 4 Catalog ledger site
python tools/build_music_registry_site.py

# 5 Verify
python tools/_verify_listen_portal.py
```

## Agent one-liner for humans

> Listen free: https://deepseekoracle.github.io/Excavationpro/excavationpro-listen.html  
> Live: Kick / Rumble / Twitch · Support: paypal.me/ExcavationPro  
> Lattice: Eternal Haven + sovereign vault + ISRC ledger.
