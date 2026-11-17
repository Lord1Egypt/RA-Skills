## Description:

Manage Elastic Email contacts and lists by reading, creating, updating, and deleting records through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Elastic Email account can retrieve and manage contact records and contact lists through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses downloads that have not been verified, and the linked CLI documents changes to installed agent skills.

Mitigation: Review and install a pinned CLI release; disable automatic skill synchronization if you do not want changes across agent installations.

Risk: Contact and list changes or deletions can alter account data.

Mitigation: Keep the approval requirements for every change and deletion, and confirm the target and payload before execution.

## Reference(s):

- [Elastic Email API Documentation](https://elasticemail.com/developers/api-documentation/rest-api)
- [Elastic Email](https://elasticemail.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON action results with concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected Elastic Email account; changes and deletions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
