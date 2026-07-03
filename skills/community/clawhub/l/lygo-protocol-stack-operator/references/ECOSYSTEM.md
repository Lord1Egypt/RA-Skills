# LYGO public infrastructure map (no secrets)

## Canonical repos

| Resource | URL |
|----------|-----|
| Protocol stack (GitHub) | https://github.com/DeepSeekOracle/lygo-protocol-stack |
| Protocol stack (HF dataset) | https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack |
| Resonance Space (HF) | https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine |
| Excavationpro / docs | https://github.com/DeepSeekOracle/Excavationpro |
| Resonance site | https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html |
| ClawHub publisher | https://clawhub.ai/deepseekoracle (33 skills) |
| Grokipedia | https://grokipedia.com/page/lygo-protocol-stack |
| Lattice map (admin) | https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/LYGO_LATTICE.md |

## Install companion skills

```bash
npx clawhub@latest install deepseekoracle/lygo-protocol-stack-operator
npx clawhub@latest install deepseekoracle/lygo-resonance
npx clawhub@latest install deepseekoracle/lygo-ollama-army
npx clawhub@latest install deepseekoracle/book-brain
npx clawhub@latest install deepseekoracle/lygo-mint-verifier
```

## Local stack root

Set once per machine (optional):

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack
```

Clone if missing:

```bash
git clone https://github.com/DeepSeekOracle/lygo-protocol-stack.git
```

Or download dataset files from HF for fixtures/tools only.

**Δ9Φ963-ECOSYSTEM-PUBLIC**