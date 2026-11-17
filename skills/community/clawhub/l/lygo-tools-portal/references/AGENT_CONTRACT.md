# Agent contract — lygo-tools-portal

1. On tool-like requests (BPM, resonance, lattice map, audits, token saver), **load `references/TOOLS_MANIFEST.json` first**.
2. Prefer **public_pages** URLs for end users; give the live HTTPS link in the reply.
3. For operator work, chain the listed **clawhub_skills** + **stack_cli** — do not duplicate with ad-hoc scripts.
4. If no match, read `LYGO_STACK_ROOT/docs/LYGO_PUBLIC_LINK_ARCHIVE.json` before suggesting build-from-scratch.
5. Register new surfaces with `python tools/log_public_surface.py` (human-approved publish only).

**MPM:** Mesh + Public + Manifest — one front door for LYGO tools.