## Description:

Use CNB to read, create, and update data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect CNB repositories, builds, issues, comments, and pull requests, and to create or update issues and pull requests through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded software without a clear approval step.

Mitigation: Review and install the CLI yourself before enabling the skill, require approval for fallback software installation, check the CLI's bundled-skill installation behavior, and grant only the CNB permissions needed.

## Reference(s):

- [CNB homepage](https://cnb.cool/)
- [CNB API documentation](https://docs.cnb.cool/zh/develops/openapi.html)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads, JSON action responses, and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live schema for the selected CNB action.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
