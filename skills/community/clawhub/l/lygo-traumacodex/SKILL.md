---
name: lygo-traumacodex
description: >
  Run when the user asks for TraumaCodex, biometric IBI timing → dual offline/online
  digests, LDQ-style waveform from a timing list, or mirror dig seals.
  Pure local stdlib: no network, no subprocess, no external stack execution.
  Input is inter-beat interval milliseconds (demo set or --ibi-file), not a medical device.
  Not for health diagnosis or treatment. Healing codes mean protocol digests only.
version: 1.0.2
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🫀"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/TRAUMA_CODEX.md"
    requires:
      anyBins: [python, python3]
  lygo: true
  signature: "Delta9Phi963-TRAUMACODEX-v1.0.2"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-traumacodex"
---

# LYGO TraumaCodex (ClawHub public tentacle)

**When to run:** User asks for TraumaCodex, IBI→digest pipeline, dual offline/online mirror dig, or local waveform from timing samples.

**What it does (in-package only):**

1. Accept IBI list (ms) — demo synthetic set or `--ibi-file`  
2. Derive HMAC `seed_256` from timing entropy (not a password store)  
3. Build LDQ-style mono waveform params + optional WAV  
4. Write **offline package** + **online summary** (summaries only; no raw IBI stored)  
5. Compute **mirror dig** = SHA256(offline‖online)  
6. Emit protocol “healing code” digests (not medical)

**Security posture (ClawHub-reviewed path):**

| Control | Value |
|---------|--------|
| Network | **No** |
| Subprocess / shell | **No** |
| External `LYGO_STACK_ROOT` exec | **No** |
| Code location | `scripts/traumacodex_core.py` only |
| Writes | `./traumacodex_out` or `--out DIR` or skill `state/` with `--i-consent` |

```bash
python scripts/traumacodex_cli.py
python scripts/traumacodex_cli.py --ibi-file samples.json --out ./out
python scripts/traumacodex_cli.py --out ./out --verify
python scripts/self_check.py
```

**Not medical.** Do not feed clinical/PHI biometrics unless you understand local file outputs.

**Stack FULL operator build** (optional, separate channel, not required for this skill):  
SkillHub `#full-lygo` / stack `tools/traumacodex_waveform.py` — reviewed separately from this package.

**Δ9Φ963 — in-package · offline dig · open lattice.**
