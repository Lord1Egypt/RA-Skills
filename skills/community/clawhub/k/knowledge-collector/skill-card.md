## Description:

Collects and catalogs equipment-institute knowledge from group chats, manual entries, and batch file imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and reviewers in an equipment institute use this skill to turn technical discussions, manual notes, and folder-based imports into structured knowledge records for later search and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and share chat or folder contents without a reliable confirmation step.

Mitigation: Require explicit opt-in for monitored channels and preview approval before every knowledge entry is stored.

Risk: Batch import can ingest supported text and source files from a user-specified folder.

Mitigation: Use folder allowlists, exclusion rules for private or secret-bearing paths, redaction checks, and retention limits before import.

Risk: Reviewer routing and access behavior depend on local configuration.

Mitigation: Review reviewer assignments and access-control settings before using the skill in a shared workplace knowledge base.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/knowledge-collector)
- [README.md](artifact/README.md)
- [Sample Knowledge Entry](artifact/examples/sample_knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown knowledge entries, text notifications, and JSON-like batch import reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses keyword dictionaries, reviewer configuration, and templates to classify records by direction, type, and knowledge level.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
