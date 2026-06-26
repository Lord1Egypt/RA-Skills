# Ledger templates

Use these templates when appending to Drive GDocs.

## Invariants & Rules entry (short, stable)
- **Rule**: <one sentence>
- **Scope**: <hunter-system | keyword-engine | common>
- **Rationale**: <why>
- **Source of truth**: <config file / doc link / script path>
- **Status**: CONFIRMED | DEPRECATED

## Decision Log entry
- **Project**: <normalized slug, e.g. hunter-system | keyword-engine | common>
- **Interfaces**: <optional, e.g. hunter-system ↔ keyword-engine>
- **Decision**: <what we decided>
- **Why**: <tradeoff / rationale>
- **Alternatives**: <A vs B>
- **Scope**: <what it affects>
- **Date**: <YYYY-MM-DD>
- **Status**: CONFIRMED | REVISITED | DEPRECATED
- **Evidence**: <links/ids (optional)>

## Change Log entry (must be traceable)
- **Project**: <normalized slug, e.g. hunter-system | keyword-engine | common>
- **Interfaces**: <optional, e.g. hunter-system ↔ keyword-engine>
- **Change**: <what changed>
- **Why**: <trigger + objective>
- **Files/IDs**: <paths + Drive fileIds/folderIds (optional in local-only mode)>
- **Evidence**: <journalctl snippet location / query output / screenshots link>
- **Impact**: <what steps/services are affected>
- **Rollback**: <exact rollback steps>
- **Date**: <YYYY-MM-DD>
- **Tags**: <drive|sqlite|systemd|feishu|notebooklm|miners|docs>
