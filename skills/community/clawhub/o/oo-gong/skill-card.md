## Description:

Gong (gong.io). Use this skill for ANY Gong request — searching and reading data. Whenever a task involves Gong, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Gong-connected users use this skill to search and read company call records, transcripts, users, and call outcomes through the Gong connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the agent to execute an unverified remote installer without separate user approval.

Mitigation: Review the installer first; install a verified CLI release yourself or require explicit approval before agent installation. Confirm that your organization permits OOMOL to access Gong data.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Connect Gong in OOMOL](https://console.oomol.com/connections/gong)
- [Gong](https://www.gong.io/)
- [Gong API access documentation](https://help.gong.io/docs/receive-access-to-the-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Gong data]

**Output Format:** [JSON responses from Gong connector actions, with textual setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented call, transcript, user, and call-outcome data; results depend on the connected Gong account and requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
