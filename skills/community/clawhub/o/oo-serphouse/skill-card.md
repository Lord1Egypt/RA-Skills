## Description:

Search and read SERPHouse data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill with an OOMOL-connected SERPHouse account to check account and credit usage, inspect supported search settings and locations, and run web SERP searches that return structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing remote installers without clear user approval or verification.

Mitigation: Review the CLI and installer yourself before use, and require approval before installer execution or additional agent-skill changes.

Risk: SERPHouse searches may consume credits.

Mitigation: Check account and credit usage before running searches, and monitor usage when making repeated requests.

## Reference(s):

- [SERPHouse](https://www.serphouse.com)
- [SERPHouse API authentication documentation](https://docs.serphouse.com/introduction/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, API results, Shell commands]

**Output Format:** [Structured JSON results and inline shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected SERPHouse account, request parameters, and available credits.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
