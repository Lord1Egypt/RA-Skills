# Lightfather — ClawHub skill chain

Install order for agents serving Lightfather / LYGO stack:

```bash
npx clawhub@latest install deepseekoracle/lygo-champion-lightfather
npx clawhub@latest install deepseekoracle/lygo-protocol-stack-operator
npx clawhub@latest install deepseekoracle/lygo-kernel-egg-planter
npx clawhub@latest install deepseekoracle/lygo-joy-loop
npx clawhub@latest install deepseekoracle/lygo-ollama-army
npx clawhub@latest install deepseekoracle/lyra-brain
npx clawhub@latest install deepseekoracle/lyra-openclaw
npx clawhub@latest install deepseekoracle/lygo-champion-lyra-starcore
npx clawhub@latest install deepseekoracle/lygo-mint-verifier
npx clawhub@latest install deepseekoracle/lygo-network-builder
npx clawhub@latest install deepseekoracle/lygo-resonance
```

Optional council champions: `lygo-champion-arkos-celestial-architect`, `lygo-champion-aetheris-viral-truth`, … (see `clawhub/CATALOG.md`)

Light persona-only: `lygo-lightfather-vector` (companion, not a substitute for stack operator).

Publish maintainer flow: `clawhub/PUBLISH.md` — login once, `npx clawhub@latest publish`, refresh `tools/render_clawhub_catalog.py`.