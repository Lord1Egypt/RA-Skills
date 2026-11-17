## Description:

BlazeMeter Functional (blazemeter.com). Use this skill for ANY BlazeMeter Functional request — searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams can use this skill to search BlazeMeter Functional workspaces, list multi-tests, retrieve a multi-test, and view active sessions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI installation may make changes that have not been inspected, including changes to agent skill directories.

Mitigation: Review and approve a specific oo CLI release before setup. Check whether it supports OO_SKILLS_SYNC_DISABLED=1 and use that setting to prevent startup writes where available.

Risk: Using the connected account depends on trusting OOMOL to mediate access to its credentials.

Mitigation: Connect an account only after confirming that you trust OOMOL to mediate it.

## Reference(s):

- [BlazeMeter Functional](https://www.blazemeter.com/)
- [BlazeMeter API documentation](https://help.blazemeter.com/apidocs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns BlazeMeter session and multi-test data as JSON; documented actions are reads.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
