## Description:

Connects to Subvisory through an OOMOL-connected account to read, create, update, and delete categories, payment methods, and subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Subvisory data can use the skill to inspect and maintain subscriptions, payment methods, and categories through their connected account. The skill guides agents to check an action's schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI can execute downloaded code; the installer payload was not independently inspected.

Mitigation: Review and install the CLI yourself from a source you trust before using the skill.

Risk: The OOMOL-connected account and automatic agent-skill synchronization may introduce broader changes to the agent environment.

Mitigation: Decide whether synchronization is wanted, review resulting changes, and keep confirmation for writes and deletions.

## Reference(s):

- [Subvisory](https://www.subvisory.com)
- [Subvisory API documentation](https://www.subvisory.com/api/v1/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON requests and responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation before execution.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
