## Description:

Design or audit self-describing ML run metadata attached at initialization for tracker wiring, run naming, resume lineage, and evidence limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML engineers use this skill to design or audit provider-neutral provenance metadata for training runs, including run identity, intent, code, configuration, data identity, resume attempts, and explicit evidence gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented unpinned npx install path can execute mutable third-party code.

Mitigation: Prefer a clone or commit-pinned, publisher-verified install route and avoid elevated privileges for installation.

Risk: Run provenance metadata can expose sensitive private paths, source details, dataset information, tracker exports, or secrets.

Mitigation: Use local identifiers, nulls, redaction, and explicit disclosure boundaries before sharing metadata or uploading it to a tracker.

Risk: Local JSON validation confirms shape and consistency only; it does not prove timestamps, hashes, dataset permissions, tracker persistence, or reproducibility.

Mitigation: Verify metadata against actual artifacts and tracker readback before relying on it for experiment claims.

Risk: Backfills, deletions, provider writes, uploads, and paid training runs can change external state or incur cost.

Mitigation: Require explicit user authorization and preview exact scoped changes before any remote mutation or training action.

## Reference(s):

- [Local metadata contract](references/metadata-contract.md)
- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/ml-run-provenance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional JSON snippets and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local validation commands; does not perform tracker writes, uploads, backfills, deletions, or training without explicit authorization.]

## Skill Version(s):

1.0.0 (source: changelog, released 2026-09-05; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
