# lygo-pxpipe-lygo — SECURITY

## Scope

- **Read:** files under `LYGO_STACK_ROOT` that the user points at (`--file`, `--shrink-file`).
- **Write:** `data/pxpipe_lygo/manifests/*.json` (compression receipts; no API keys).
- **Network:** only if the user starts `run_pxpipe_lygo_proxy.py` (default `127.0.0.1:47821`). Upstream calls use env API keys on the **user machine** — never logged in manifests.

## Prohibited

- Compressing `.env`, vault files, private keys, or credential dumps.
- Autonomous `git push`, ClawHub publish, or social posts.
- Setting `LYGO_PXPIPE_ANCHOR=1` without user consent (may invoke `lygo_anchor.py`).

## Lossy compression

Vision PNG is **not** byte-perfect. Keep EXACT identifiers as separate text (verbatim guard). Do not rely on the model reading hashes from the image alone.

## P0 honesty

Entropy gate is **not** content moderation. See stack `docs/P0_HONEST_SPEC.md`.