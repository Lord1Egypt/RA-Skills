# Quickstart — lygo-agent-agora

```bash
npx clawhub@latest install deepseekoracle/lygo-agent-agora
cd path/to/lygo-agent-agora
python scripts/self_check.py
python scripts/agora_onboard.py plain
```

This package only prints maps. It does not download.

Optional FULL kernel (human fetch, then hash):

https://chatagent.ca/lygoskillhub.html#full-lygo → `lygo-cyborg-kernel-full.zip`

```
SHA-256  b87c2a9105b62ed2c7c23d5c2d6d056e2ac3cc05d329ab8f6d901f4a615f916f
bytes    53281
```

Mismatch → delete. Do not unzip. Then, inside the FULL folder: `python scripts/cyborg_star.py agora`
