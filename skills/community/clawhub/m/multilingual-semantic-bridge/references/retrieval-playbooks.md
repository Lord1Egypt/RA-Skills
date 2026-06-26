# Retrieval Playbooks

Use retrieval as the downstream consumer of the bridge pipeline.

Main priority order:
1. recover the right target
2. choose the right source
3. compare source authority correctly

Typical targets:
- memory
- local docs/files
- official docs
- skill/tool path

Target-oriented retrieval rule:
- memory: original phrasing often works; add canonical intent by default; add a pivot when ranking precision matters
- official docs: strongly favor canonical intent + English technical pivot
- skill/tool path: strongly favor product/action nouns and English technical pivots when metadata is English-heavy
- local docs/files: use the pivot whenever filenames or headings are operationally English-heavy
- exact-token surfaces: preserve exact identifiers, config keys, provider names, CLI commands, and errors verbatim

Surface-selection rule:
- prior work / decisions / local chronology / local incidents / local lessons → memory first
- upstream behavior / official semantics / official error handling / config-reference docs → official docs/artifact first
- installed skill choice / skill instructions / skill-local references → skill artifact first
- self-service recovery / local operating procedure / handoff / runbook use → runbook/local-file first
- exact command / exact config path / exact filename / exact identifier → exact-token artifact first

Interpretation rule:
- do not mistake a strong memory hit about a target for proof that the target artifact itself is the right first surface
- when a target class is clear, route to the matching surface first and use memory as secondary context if needed

Do not multiply playbooks unless they materially strengthen the mainline.
