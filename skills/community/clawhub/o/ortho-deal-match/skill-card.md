## Description:

Matches orthopedic buyers and suppliers with five-dimension scoring, contact exchange only after mutual consent, and local controls for registration, quotas, blocking, role visibility, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

External business users and operators use this skill to publish orthopedic sourcing needs or supplier capabilities, score potential matches, manage mutual-consent introductions, and import public expo company leads for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles business contact details and deal records in local files.

Mitigation: Use it only in trusted local or internal environments, protect and back up the SQLite database, registry, blocklist, and audit files, and avoid storing private records in shared workspaces.

Risk: Consent, roles, blocking, and data changes rely on caller-supplied user identities.

Mitigation: Add real authentication, object-level authorization, and stronger consent records before using it with multiple untrusted users.

Risk: Runtime data and caches can contain registration, contact, matching, and audit records.

Mitigation: Exclude data, registry, audit, archive, backup, and bytecode cache paths from release packages and deployment bundles.

## Reference(s):

- [Workflow guide](artifact/references/WORKFLOW.md)
- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ortho-deal-match)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite, JSONL registry, blocklist, and audit files when the user runs the included scripts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
