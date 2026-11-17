## Description:

Documenso (documenso.com). Use this skill for ANY Documenso request — searching and reading data. Whenever a task involves Documenso, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search and retrieve Documenso envelopes and templates through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions direct the agent to run a downloaded installer without first asking for approval.

Mitigation: Review and install the CLI yourself before use, and require approval for setup changes.

Risk: Connecting Documenso entrusts OOMOL with account credentials and access to requested data; automatic skill synchronization settings also warrant review.

Mitigation: Review the automatic skill synchronization settings and understand the requested data access before connecting Documenso.

## Reference(s):

- [Documenso API documentation](https://docs.documenso.com/docs/developers/api)
- [Documenso](https://documenso.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON data returned by the Documenso connector]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval of envelopes and templates; available data depends on the connected account's permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
