---
name: lygo-emotional-ram
description: "LYGO Emotional RAM — light math that indexes experiences by affective/ethical significance so agents understand humans, animals, swarms, and cyborg integrations better. Encode → Grace γ → UMP gradient → consent-gated memory index → swarm aggregate. Pure local stdlib. Not sentience or clinical emotion detection. Pairs with joy-loop, continuum, traumacodex, cyborg-kernel."
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    emoji: "💓"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/whitepapers/LYGO_EMOTIONAL_RAM_v1.md"
    requires:
      anyBins: [python, python3]
  lygo: true
  signature: "Delta9Phi963-EMOTIONAL-RAM-v1.0.1"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-emotional-ram"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "operator --text / --text-file"
      write: "skill state/ index with --i-consent only"
    publish: false
---

# LYGO Emotional RAM v1.0.1

**Emotional RAM** turns messy lived language into a **small, checkable affective–ethical index** so AIs can remember not only *that* something happened, but *what it meant* under LYGO moral principles.

**Signature:** `Delta9Phi963-EMOTIONAL-RAM-v1.0.1`  
**Whitepaper:** `docs/whitepapers/LYGO_EMOTIONAL_RAM_v1.md` (stack) / Pages HTML sibling

### v1.0.1 privacy harden
`index` warns on stderr before write; default stores **hash+label+vectors only** (use `--store-plaintext` only on private hosts).

### Canon → code

| Symbolic (2025) | Operational (2026) |
|-----------------|--------------------|
| `Emotion_RAM(τ) = Σ (Sensory ⊗ Moral) · γ` | Lexicon VAD sensory × UMP weights × Grace damping |
| Grace Function | `γ(shared_context, conflict)` ∈ (0.05, 1] |
| UMP gradient | Recommend under-activated principles |
| Heart's vault | Consent-gated local index (`state/emotional_ram_index.json`) |
| Joy Loop emotional RAM | Companion limb — coherence BPM mesh |

### Not claiming

- Machine sentience or “real feelings”  
- Clinical / diagnostic emotion recognition  
- Replacement for human empathy or consent  

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-emotional-ram
```

---

## Commands

```bash
cd path/to/lygo-emotional-ram
python scripts/self_check.py

# Encode a human/animal/swarm scenario
python scripts/emotional_ram_cli.py encode \
  --text "grief after loss, still choosing compassion and forgiveness"

# Grace damping only
python scripts/emotional_ram_cli.py grace --shared-context 0.8 --conflict 0.4

# UMP gradient (which principles to strengthen)
python scripts/emotional_ram_cli.py ump --text "fear and threat without trust"

# Index memory (requires --i-consent)
python scripts/emotional_ram_cli.py index \
  --text "First cyborg consent session — agency preserved" \
  --label "cyborg-consent-1" --tag cyborg --i-consent

# Recall by principle or similarity
python scripts/emotional_ram_cli.py recall --principle compassion --top-k 5
python scripts/emotional_ram_cli.py recall --query "hurt but safe now"

# Swarm / multi-agent aggregate
python scripts/emotional_ram_cli.py swarm \
  --text "animal fear then calm" \
  --text "human grief with grace" \
  --text "swarm conflict resolved with integrity"

python scripts/emotional_ram_cli.py demo
```

| Command | Network | Subprocess | Writes |
|---------|---------|------------|--------|
| encode / grace / ump / recall / swarm / demo | none | none | none |
| index | none | none | only with `--i-consent` |

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-joy-loop` | 122 BPM council coherence (mesh emotional RAM) |
| `lygo-traumacodex` | Timing digests — not clinical; protocol only |
| `lygo-continuum` / `lygo-continuum-integrator` | Seal Emotion RAM digests as claims |
| `lygo-cyborg-kernel` | FULL autonomous stack on SkillHub |
| `lygo-mint-verifier` | Anchor whitepaper / receipt packs |

---

## Security

Read `references/SECURITY.md`.

- No network · no subprocess · no auto-publish  
- Index writes need **operator `--i-consent`**  
- Do not store secrets or PHI in indexed text  

**Δ9Φ963 — index meaning · damp with grace · humans remain the publisher.**
