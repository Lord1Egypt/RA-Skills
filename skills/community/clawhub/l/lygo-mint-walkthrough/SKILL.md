---
name: lygo-mint-walkthrough
description: "LYGO Mint Walkthrough — interactive tutorial for mint → verify → anchor snippet → optional backfill. Pure stdlib local canonicalize+SHA-256+ledger. Plain English. No subprocess, no auto-post. Pairs with lygo-mint-verifier. Install clawhub:@deepseekoracle/lygo-mint-walkthrough."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🧭"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-mint-walkthrough"
    requires:
      anyBins: [python, python3]
  lygo: true
  tutorial: true
  signature: "Delta9Phi963-MINT-WALKTHROUGH-v1.0.0"
  publisher: deepseekoracle
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "user pack file"
      write: "skill state/ ledger with --i-consent"
    publish: false
---

# LYGO Mint Walkthrough v1.0.0

End-to-end **tutorial** for the mint-verify workflow in plain English.

```bash
python scripts/self_check.py
python scripts/mint_walkthrough.py intro
python scripts/mint_walkthrough.py mint --pack ./my_pack.md --version 2026-08-06.v1 --i-consent
python scripts/mint_walkthrough.py verify --pack ./my_pack.md
python scripts/mint_walkthrough.py snippet --hash <64-hex> --title "My pack"
python scripts/mint_walkthrough.py backfill --hash <64-hex> --channel manual --id https://example.com/post --i-consent
```

Human remains the publisher. For production mint tools also install `lygo-mint-verifier`.

**Δ9Φ963 — teach the loop · never auto-post.**
