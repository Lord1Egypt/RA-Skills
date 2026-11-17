# SECURITY — lygo-pc-lattice-hardening

- Advisor checklist only inside this package.
- No firewall, registry, or OS hardening scripts ship here.
- Stack audit tools (if present under LYGO_STACK_ROOT) are operator-run and must not auto-mutate.
- Never store or print API keys, tokens, or private keys in skill output.
- No auto git push / publish / social.
