## Description:

Use Intercom to read workspace data and manage conversations and contacts through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support teams use this skill to look up Intercom workspace data and manage conversations and contacts through an already connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an unverified remote CLI installer.

Mitigation: Review and verify the installer before allowing setup to run it.

Risk: The hosted connector can access Intercom account and customer data.

Mitigation: Review the permissions granted and connect only the intended account.

Risk: Write and destructive actions can change Intercom data.

Mitigation: Confirm the exact action and payload with the user before running it.

## Reference(s):

- [Intercom REST API documentation](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Intercom](https://www.intercom.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; state-changing and destructive actions require user confirmation.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
