## Description:

Contract Review + Contract Ops Copilot for solo entrepreneurs that analyzes contracts, flags risks, suggests redline language and negotiation emails, tracks deadlines, and maintains a structured contract archive with cross-contract portfolio insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonfjr](https://clawhub.ai/user/leonfjr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, solo entrepreneurs, and one-person company CEOs use this skill for first-pass routine commercial contract review, negotiation preparation, deadline tracking, archive creation, search, and portfolio-level contract insights. It is not a substitute for professional legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store contract documents, extracted metadata, reports, indexes, and portfolio insights in a local contracts directory.

Mitigation: Use it only in an approved workspace, restrict access to the contracts directory, and review archive outputs before sharing or relying on them.

Risk: Contract analysis, redline suggestions, and negotiation strategy may be mistaken for legal advice.

Mitigation: Treat outputs as a first-pass business risk review and consult a qualified attorney before making binding or high-risk decisions.

Risk: Local deadline and index scripts read and write contract archive files.

Mitigation: Run scripts against the intended contracts directory, keep backups for important archives, and inspect generated indexes, reports, and insights.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonfjr/skills/opc-contract-manager)
- [Contract Red Flags Checklist](artifact/references/red-flags-checklist.md)
- [Solo Entrepreneur Concerns Guide](artifact/references/solo-entrepreneur-concerns.md)
- [Standard Clauses Reference](artifact/references/standard-clauses.md)
- [Termination for Convenience Deep Dive](artifact/references/termination-for-convenience.md)
- [Contract Metadata Schema](artifact/templates/contract-metadata-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and email drafts, JSON contract metadata and indexes, shell commands for local archive scripts, and plain-English guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include practical risk reviews, suggested redline language for discussion, negotiation strategy, deadline dashboards, contract archive files, and portfolio insights.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
