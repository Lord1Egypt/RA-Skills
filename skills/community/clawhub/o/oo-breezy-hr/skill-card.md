## Description:

Breezy HR (breezy.hr). Use this skill for ANY Breezy HR request — searching and reading data. Whenever a task involves Breezy HR, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams use the skill to search and read candidate, position, company, and current-user records in an OOMOL-connected Breezy HR account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-CLI fallback can run installer code that has not been verified and may change other installed agent skills.

Mitigation: Review and approve CLI installation separately, prefer a pinned and verified release, and check or disable automatic synchronization of other skills.

Risk: The connected account can expose HR records to the hosted connector.

Mitigation: Confirm OOMOL is authorized to access the requested HR records and limit the connected account's permissions.

## Reference(s):

- [Breezy HR](https://breezy.hr/)
- [Breezy HR API reference](https://developer.breezy.hr/reference/overview)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON data with concise text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HR records returned depend on the connected account, selected action, and its permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
