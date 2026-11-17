# LYGO LoRa mesh

Compact Layer D `roots_digest` pulse for stock Meshtastic. Not a firmware fork.

```bash
npx clawhub@latest install deepseekoracle/lygo-lora-mesh
python scripts/self_check.py
python scripts/lygo_lora.py plain
python scripts/lygo_lora.py probe
```

No board → NAMED_SHADOW. NA region 915 MHz. See `references/HARDWARE.md`.
