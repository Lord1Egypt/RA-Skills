## Description:

Search and retrieve TianAPI data through an OOMOL-connected account, including trends, calendar information, holidays, and traditional entertainment interpretations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents with an OOMOL-connected TianAPI account use this skill to query Chinese platform trends, calendar and holiday data, and traditional entertainment interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute a downloaded CLI installer, and the installer's exact local changes are unverified.

Mitigation: Review and approve a fixed CLI release before setup; check the CLI's automatic skill synchronization and connect only the intended TianAPI account.

Risk: TianAPI requests routed through OOMOL may consume credits.

Mitigation: Check account access and remaining credits before making requests that may incur usage.

## Reference(s):

- [TianAPI](https://www.tianapi.com/)
- [TianAPI Account Information API documentation](https://www.tianapi.com/apiview/96)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data and availability depend on the selected TianAPI endpoint, account access, and available credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
