## Description:

Operate updown.io checks and monitoring node data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to inspect updown.io checks and monitoring node data, and to create, update, or delete checks after confirming the exact change. It requires the oo CLI to be installed, signed in, and connected to updown.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup may add persistent agent instructions beyond this skill’s stated purpose.

Mitigation: Review the CLI’s broader installation behavior before enabling it. Use a vetted CLI release, and disable managed-skill synchronization if only updown.io access is needed.

Risk: Remote installers and the hosted runtime have not been audited, so their full behavior is uncertain.

Mitigation: Use a vetted CLI release and retain the required approvals for account changes and deletions.

## Reference(s):

- [updown.io](https://updown.io)
- [updown.io API documentation](https://updown.io/api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action input fields are determined from the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
