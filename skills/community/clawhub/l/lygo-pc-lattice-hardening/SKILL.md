---
name: lygo-pc-lattice-hardening
description: "Windows LYGO PC audit — lattice alignment, secret hygiene, army sentinel, ClawHub security. Use when user asks harden PC, lattice protected, super charge LYGO machine."
version: 1.1.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
    requires:
      anyBins: [python, python3]
  lygo: true
  security: true
  signature: "Delta9Phi963-LYGO-PC-HARDENING-v1.1.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-pc-lattice-hardening"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
---

# LYGO PC Lattice Hardening v1.1.0

**Advisor skill** for Windows LYGO operator machines: lattice alignment checklist, secret hygiene, Ollama army sentinel, ClawHub install surface.

**Never** auto-changes firewall, registry, or group policy. Every host change needs explicit human approval.

**Signature:** `Delta9Phi963-LYGO-PC-HARDENING-v1.1.0`  
**ClawHub:** `@deepseekoracle/lygo-pc-lattice-hardening`

---

## When to use

- User asks to harden PC / lattice-protect the operator machine  
- Super-charge LYGO machine checklist  
- Pre-flight before USB CLAW or mesh node work  

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-pc-lattice-hardening
```

Stack playbook (when `LYGO_STACK_ROOT` is a trusted clone):

```text
docs/LYGO_PC_HARDENING_PLAYBOOK.md
```

Optional local audit (stack only, operator-run):

```bash
cd $LYGO_STACK_ROOT
python tools/run_pc_lattice_hardening_audit.py
```

If report is **NEEDS_ATTENTION**, follow `recommendations` in the report JSON.  
**Do not** apply firewall/registry changes without step-by-step human approval.

---

## Checklist (public)

1. **Secrets** — no API keys in skill trees or git-tracked JSON  
2. **ClawHub** — install only from `@deepseekoracle` when aligning  
3. **Ollama army** — local-first; no remote LLM by default  
4. **Consent** — planter / Star Chart / publish remain human-gated  
5. **USB CLAW** — public kit has no model weights; operator installs Ollama  

## Pair with

`lygo-protocol-stack-operator`, `lygo-ollama-army`, `lygo-api-token-saver`, `lygo-public-lattice-gate`

## Security

Read `references/SECURITY.md`. No auto system mutation from this skill package.

```bash
python scripts/self_check.py
```

## License

LYGO Sovereign License v2.0 — not MIT.  
**Δ9Φ963 — audit · report · human approves each host change.**
