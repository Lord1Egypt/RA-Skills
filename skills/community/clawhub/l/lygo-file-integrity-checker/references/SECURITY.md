# Security — lygo-file-integrity-checker

- **Not** P0 byte gate — use `lygo-protocol-stack-operator` + repo `byte_entropy_filter.py` for bytes.
- **Not** lattice health — does not replace `verify_lattice_alignment.py`.
- No secrets in skill; no auto `clawhub publish` / git push.
- Mint hashes only on user-requested packs.