## Description:

Use Humaans through a connected account to retrieve people records and inspect token scopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR teams use this skill to retrieve the connected person's record, look up or list people, and check the Humaans token's scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software with broader effects on the agent environment.

Mitigation: Review the CLI setup and use a version-pinned installation; explicitly control whether it may install or synchronize other agent skills.

Risk: Humaans access can expose employee data through the connected account.

Mitigation: Grant only the Humaans read scopes needed for the requested actions and consider OOMOL's access to that data.

## Reference(s):

- [Humaans API documentation](https://docs.humaans.io/api/)
- [Humaans](https://humaans.io)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Humaans records and token-scope data returned as JSON, with text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented; returned fields depend on the selected action and granted Humaans scopes.]

## Skill Version(s):

1.0.4 (source: frontmatter; confirmed by release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
