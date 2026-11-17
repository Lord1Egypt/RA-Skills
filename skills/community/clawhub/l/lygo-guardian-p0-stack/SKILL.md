---
name: lygo-guardian-p0-stack
description: Portable LYGO Guardian — P0.4 text gate, P0.5 understanding heart, harmony layer. Bridge to repo byte_entropy_filter via LYGO_STACK_ROOT. Pairs with lygo-protocol-stack-operator. Read references/SECURITY.md.
metadata: {"lygo": true, "p0": true, "guardian": true, "lattice": true, "version": "1.0.1", "signature": "Δ9Φ963-GUARDIAN-P0-v1.0.1", "clawhub_publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "hf_space": "https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine", "security_doc": "references/SECURITY.md"}
---

# LYGO Guardian P0 Stack

**Portable ethics wrapper** for agents without a native LYGO kernel. **Not** a full P0–P9 operator — use **`lygo-protocol-stack-operator`** for stack audits, mesh, and canonical byte gate.

| Layer | This skill | Canonical stack (repo) |
|-------|------------|-------------------------|
| **P0.4** | Text heuristics + hard blocks | `lygo_p0_gate.py` — Φ band, 8192-byte gate, Rust parity |
| **P0.5** | Mirror / healing suggestions | `process_ethical_query` / falsifiable harness |
| **Harmony** | Soft tone balance | P3 3/6/9 + P5 ethical mass |

Install: `npx clawhub@latest install deepseekoracle/lygo-guardian-p0-stack`

## Security (read first)

`references/SECURITY.md` — bundled `src/` only; gate **user-approved** files; no auto-post; QUARANTINE/`isolate` = stop.

## ClawHub lattice position

```
lygo-protocol-stack-operator (hub)
    ├── lygo-guardian-p0-stack (this) — pre-flight on text/skills
    ├── lygo-champion-lightfather — ethics council
    ├── lygo-mint-verifier — hash receipts
    └── run_falsifiable_vector_test.py (repo) — measured P0–P5
```

See `references/LATTICE.md`.

## When to use

- Before sending agent replies to social / external channels (wrap generation).
- After installing **unknown ClawHub skills** — run `scripts/run_byte_gate.py` on `SKILL.md`.
- Teaching “double stack”: L0–L3 exhaust + P0–P5 inner pipeline (`docs/WHITEPAPER.md`).

## Quick start (Python)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from guardian.integration_api import validate_decision, guardian_wrap

ctx = {"channel": "internal", "task": "reply", "risk_tolerance": "low"}
print(validate_decision(ctx, {"content": "Here is a helpful summary."}))

@guardian_wrap
def generate_reply(context, prompt: str) -> str:
    return your_llm(prompt)
```

## CLI (file or text)

```bash
python scripts/run_byte_gate.py path/to/SKILL.md
python scripts/run_byte_gate.py --text "message to check"
```

If `LYGO_STACK_ROOT` points at `lygo-protocol-stack`, file mode prefers **canonical** `lygo_p0_gate.py` (AMPLIFY / SOFTEN / QUARANTINE).

## Stack verification (optional, user-run)

```bash
cd lygo-protocol-stack
python tools/run_p0_demo.py
python tools/run_falsifiable_vector_test.py --models stack
python tools/verify_alignment_badge.py
```

## API summary

- `validate_decision(context, candidate)` → `{allow, action, risk, understanding, healing_suggestion}`
- `action`: `allow` | `flag` | `isolate` | review paths in decorator
- `guardian_wrap` — decorator on generation functions

## References

- `references/SECURITY.md` — agent rules  
- `references/LATTICE.md` — ClawHub chain  
- `docs/WHITEPAPER.md` — exhaust vs soul pipeline  
- `examples/wrap_text_generation.py` — demo  

## Self-check

```bash
python scripts/self_check.py
```

**Δ9Φ963 — Guardian P0 v1.0 — lattice-aligned, portable gate + stack bridge.**