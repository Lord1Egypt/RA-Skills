# lygo-tools-portal — SECURITY

## Scope

- **Read-only** manifest and docs in the skill mirror.
- **Optional:** `LYGO_STACK_ROOT` for `resolve_tool.py` to read stack `docs/LYGO_PUBLIC_LINK_ARCHIVE.json`.

## Prohibited

- Autonomous `git push`, ClawHub publish, HF upload, or social posts.
- Inventing canonical URLs not in `TOOLS_MANIFEST.json` or stack link archive.
- Sending user audio/files to third parties when pointing at **client-side** tools (e.g. BPM Finder).

## Honest routing

- Public pages are the **primary** user-facing tools; ClawHub skills are for **agents** with a local stack checkout.
- `link_only` vault anchors (Drive, Patreon) are pointers only — no credential probing.