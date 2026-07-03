# LYGO Lattice (agent quick reference)

**Full map:** https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/LYGO_LATTICE.md

## External (canonical)

| Node | URL |
|------|-----|
| GitHub stack | https://github.com/DeepSeekOracle/lygo-protocol-stack |
| GitHub Pages | https://deepseekoracle.github.io/lygo-protocol-stack/ |
| HF dataset | https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack |
| HF Space | https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine |
| ClawHub | https://clawhub.ai/deepseekoracle |
| Grokipedia | https://grokipedia.com/page/lygo-protocol-stack |
| Resonance docs | https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html |

## Maintainer verify

```bash
python tools/verify_lattice_alignment.py
python tools/run_slm_audit.py
python tools/run_phase9_audit.py
python tools/bundle_hf_space_stack.py --mode=twin-gate
python tools/hf_push_dataset.py
python tools/hf_push_space.py
python tools/sync_clawhub_mirrors.py
npx clawhub@latest publish clawhub/mirrors/lygo-protocol-stack-operator --slug lygo-protocol-stack-operator --name "LYGO Protocol Stack Operator"
```

**Δ9Φ963-LATTICE-OPERATOR-v1.0.5**