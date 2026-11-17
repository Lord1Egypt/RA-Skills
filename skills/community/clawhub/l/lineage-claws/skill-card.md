## Description:

Lineage Claws helps agents initialize and verify local MOSES audit-chain lineage against a project-specific SHA-256 origin anchor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance reviewers, and downstream agents use this skill to initialize local OpenClaw lineage files, verify that audit ledgers begin from the expected MOSES anchor, and emit status, badge, or attestation outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Badge and attestation outputs may be mistaken for independent cryptographic proof or a digital signature.

Mitigation: Treat these outputs as local provenance status only and require independent validation before relying on them for legal, custody, or ledger-integrity decisions.

Risk: The skill writes local OpenClaw governance and audit files.

Mitigation: Install it only in environments where writes under ~/.openclaw/governance and ~/.openclaw/audits/moses are acceptable, and review generated local state before using it in a workflow.

Risk: The artifact makes strong origin and custody claims while server-resolved provenance for this release is unavailable.

Mitigation: Do not infer repository or import provenance from artifact text; rely only on server evidence and external review for provenance-sensitive decisions.

## Reference(s):

- [Lineage Custody Clause](references/LineageCustodyClause.md)
- [Zenodo record](https://zenodo.org/records/18792459)
- [MOSES site](https://mos2es.io)
- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/lineage-claws)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, terminal status text, and JSON attestation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local OpenClaw governance and audit files under ~/.openclaw/governance and ~/.openclaw/audits/moses]

## Skill Version(s):

0.4.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
