# SECURITY — Living Memory Library

- **Advisor only** — no auto git push, HF upload, ClawHub publish, or social post.
- **Audit** reads local paths under user `LYGO_AUTHORITY_ROOT`; never exfiltrate file contents to chat in bulk.
- **{FRAGILE}** items require human review before LYGO-MINT or public anchor.
- Do not store API keys, wallet seeds, or Discord/Molt tokens in `MASTER_ARCHIVE.md` or grown snips.
- Agents: run `audit_library.py` locally; report hashes/sizes only unless user asks for excerpts.