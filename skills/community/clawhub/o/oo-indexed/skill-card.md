## Description:

Use the oo CLI to search and read company data through Indexed using an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers can use the skill to search Indexed company records and retrieve company profiles through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an online installer whose contents were not assessed and may add other agent skills.

Mitigation: Review and approve the CLI installation and any additional skills separately before enabling them.

Risk: Indexed searches and profile queries may consume account credits.

Mitigation: Review the requested action and its stated credit cost; do not retry billing errors as though they were transient.

## Reference(s):

- [Indexed API documentation](https://indexed.vc/docs/api)
- [Indexed](https://indexed.vc)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured company data and concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company lookup and search results vary by action, requested depth, and available Indexed data.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
