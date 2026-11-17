## Description:

Use Getform through an OOMOL-connected account to list submissions and submit form data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve submissions from protected forms or submit form data through a connected Getform account. It is intended for users who already have the oo CLI installed and Getform connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified installers and may introduce broader agent changes without clear user control.

Mitigation: Review and install the CLI separately; disable automatic skill synchronization if only Getform access is needed.

Risk: Connecting Getform entrusts OOMOL with credential handling and requested form data, and form submission changes data.

Mitigation: Review the connection and submission payload, and keep submission confirmations enabled.

## Reference(s):

- [Forminit documentation](https://forminit.com/docs/)
- [Forminit homepage](https://forminit.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include listing submissions and submitting form data.]

## Skill Version(s):

1.0.5 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
