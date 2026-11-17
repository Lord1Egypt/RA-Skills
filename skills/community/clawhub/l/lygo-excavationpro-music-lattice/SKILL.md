---
name: lygo-excavationpro-music-lattice
description: "Excavationpro sovereign music portal on the LYGO lattice — free listen hub, CAS vault Merkle, ISRC ledger, HF streams, Kick/Rumble/Twitch live portals, PayPal support. Agents route/verify/operate; no auto publish."
metadata: {"lygo": true, "music": true, "lattice": true, "excavationpro": true, "consent_required": true, "version": "1.0.0", "requires_lygo_stack": false, "security_audit": "SkillSpector-hardened", "capability_filesystem_read": "skill_mirror_and_optional_LYGO_STACK_ROOT", "capability_network": "optional_public_https_status_only", "capability_git_publish": "human_only", "capability_hf_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "mirror": "clawhub/mirrors/lygo-excavationpro-music-lattice", "signature": "Δ9Φ963-EXCAVATIONPRO-MUSIC-LATTICE-v1.0"}
---

# LYGO Excavationpro Music Lattice v1.0

**One skill that ties free listening, the sovereign vault, the catalog ledger, live portals, and LYGO lattice docs together.**

```text
Listen portal  ←→  HF streams  ←→  CAS vault (SHA-256)
       ↕                  ↕
 Catalog ledger      Kernel eggs / Pages
       ↕
 Kick · Rumble · Twitch · PayPal · AdSense (consent)
```

**Public player:** https://deepseekoracle.github.io/Excavationpro/excavationpro-listen.html  

**ClawHub install:**

```bash
npx clawhub@latest install deepseekoracle/lygo-excavationpro-music-lattice
```

Optional stack (operator tools):

```bash
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

---

## When to use

- User wants to **listen free**, find the **music portal**, or “where is Excavationpro music?”
- Agent must **rebuild / scan / verify** the music vault without reinventing paths
- Linking music work to **Eternal Haven / lattice / eggs**
- Live: **Kick / Rumble / Twitch**
- Donate: **PayPal.me/ExcavationPro**

## When not to use

- Generic audio DSP (use `lygo-resonance`)
- Full stack mesh deploy (use `lygo-protocol-stack-operator`)
- Auto social post or auto HF publish without a human

---

## Agent workflow (required)

1. Read `references/AGENT_CONTRACT.md` + `references/SECURITY.md`  
2. Load **`references/MUSIC_PORTAL.json`** (canonical URLs + CLI map)  
3. Prefer routing humans to **HTTPS** pages  
4. Status check:

```bash
python scripts/self_check.py
python scripts/portal_status.py
```

5. If `LYGO_STACK_ROOT` set, deep verify:

```bash
python "$LYGO_STACK_ROOT/tools/_verify_listen_portal.py"
```

6. For rebuild / encode / publish — use `stack_cli` entries in MUSIC_PORTAL.json and **confirm consent** for HF/git.

---

## Lattice surfaces (send users here)

| Surface | URL |
|---------|-----|
| **Listen Free (player)** | https://deepseekoracle.github.io/Excavationpro/excavationpro-listen.html |
| Catalog + ISRC ledger | https://deepseekoracle.github.io/Excavationpro/excavationpro-music-catalog.html |
| Hash vault | https://deepseekoracle.github.io/Excavationpro/excavationpro-sovereign-music-hub.html |
| Eternal Haven | https://deepseekoracle.github.io/Excavationpro/eternalhaven.html |
| HF stream dataset | https://huggingface.co/datasets/DeepSeekOracle/excavationpro-music-stream |
| Kick Live | https://kick.com/excavationpro |
| Rumble Live | https://rumble.com/user/excavationpro/live |
| Twitch | https://twitch.tv/excavationpro |
| **Donate** | https://www.paypal.com/paypalme/ExcavationPro |

Architecture diagram: `references/LATTICE_MAP.md`

---

## Steward operator loop (stack)

```bash
export LYGO_STACK_ROOT=...

# Hash new masters (merge)
python tools/build_music_cas_vault.py --scan --root "I:\Actors" --hub

# Encode 160k streams (skips existing)
python tools/build_public_music_stream.py --encode --workers 4

# Publish HF + rebuild epic listen page (HUMAN OK)
python tools/build_public_music_stream.py --publish-hf --hub

# Catalog / ledger site
python tools/build_music_registry_site.py

# Verify
python tools/_verify_listen_portal.py
```

Kernel eggs (metadata anchors — via planter skill, consent-gated):

| egg_id | Role |
|--------|------|
| `excavationpro-music-catalog-v1` | Catalog / ISRC snapshot |
| `excavationpro-music-vault-v1` | Vault Merkle egg core |

---

## What “tied to the lattice” means

| Piece | Lattice role |
|-------|----------------|
| Listen HTML | Public Pages node (SEO + AdSense consent + player) |
| Playlist JSON | Machine-readable stream index |
| Vault Merkle | Immutable set of master content hashes |
| Ledger SHA-256 | Catalog snapshot integrity |
| HF streams | Public retrieval of listenable audio |
| Kernel eggs | Optional plant of roots into egg registry |
| Live portals | Discovery without DistroKid |

Agents must **not** claim masters live “on chain” unless a specific anchor was planted and verified.

---

## Agent rules (non-negotiable)

1. Never auto `git push`, HF upload, or ClawHub publish.  
2. Never put secrets in portal JSON or eggs.  
3. Distinguishes **streams** (public) vs **masters** (local).  
4. PayPal link only: `paypal.me/ExcavationPro` (no invented donate URLs).  
5. Chain: tools-portal → **this skill** → stack-operator → kernel-egg-planter.

---

## Maintainer publish

```bash
npx clawhub@latest publish "…/clawhub/mirrors/lygo-excavationpro-music-lattice" \
  --slug lygo-excavationpro-music-lattice \
  --name "LYGO Excavationpro Music Lattice"
```

**Δ9Φ963 — listen free · hash is truth · lattice holds the map · human holds publish.**
