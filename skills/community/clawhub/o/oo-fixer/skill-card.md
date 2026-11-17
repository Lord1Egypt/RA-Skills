## Description:

Fixer (fixer.io). Use this skill for ANY Fixer request — searching and reading data. Whenever a task involves Fixer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Fixer users can retrieve historical or latest exchange rates and look up supported currency symbols through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run an installer whose remote behavior has not been verified, and the CLI dependency may install additional agent skills.

Mitigation: Review the CLI installer and release before installing. Set OO_SKILLS_SYNC_DISABLED=1 if you only want Fixer access.

Risk: Fixer requests use the user's OOMOL-connected account, with credentials mediated by OOMOL.

Mitigation: Confirm the intended Fixer account is connected before running a lookup.

## Reference(s):

- [Fixer API documentation](https://fixer.io/documentation)
- [Fixer homepage](https://fixer.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Fixer account; action schemas determine request fields.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
