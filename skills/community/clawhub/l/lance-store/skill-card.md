## Description:

Persist and retrieve structured data using the Lance columnar format for cross-session storage, querying, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitorhugoze](https://clawhub.ai/user/vitorhugoze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Lance Store to persist structured records, retrieve datasets, and maintain knowledge or research data across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local persistent storage can write or delete data more broadly than users may expect.

Mitigation: Use the skill in an isolated workspace and require explicit confirmation before delete, drop, or broad write operations.

Risk: Important or sensitive data may be stored in local datasets without additional safeguards.

Mitigation: Avoid storing secrets or sensitive personal data unless the workspace and retention policy are approved for that data.

Risk: Unpinned dependencies may change behavior over time.

Mitigation: Pin dependencies or install from a reviewed lockfile before relying on the skill for important workflows.

## Reference(s):

- [ClawHub Lance Store listing](https://clawhub.ai/vitorhugoze/skills/lance-store)
- [Lance project repository](https://github.com/lance-format/lance)
- [Lance documentation](https://lance.org)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Configuration]

**Output Format:** [JSON responses from local Python command-line operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates, updates, reads, backs up, and deletes local Lance datasets in the current workspace.]

## Skill Version(s):

1.0.12 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
