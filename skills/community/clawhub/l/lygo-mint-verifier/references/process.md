# LYGO-MINT process (v1.1)

1. Align / write the pack (no secrets).
2. `python scripts/mint_cli.py mint --pack PATH --version VER [--i-consent]`
3. Copy the printed **Anchor Snippet** and post it yourself (X / Moltbook / Discord / …).
4. `python scripts/mint_cli.py backfill --hash … --channel x --id URL --i-consent`
5. Later: `verify --pack PATH --hash …` to confirm the file still matches.

Optional Continuum Integrator receipt after mint:

```bash
python ../lygo-continuum-integrator/scripts/integrator_cli.py integrate \
  --truth "pack:<sha256>" --chaos "creative-revision" --node-id mint
```
