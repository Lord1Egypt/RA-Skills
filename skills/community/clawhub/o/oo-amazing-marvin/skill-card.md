## Description:

Use this skill to read, create, and update Amazing Marvin data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Amazing Marvin through an OOMOL-connected account can read tasks, projects, categories, and labels, and create or complete tasks and projects. The skill requires confirmation before actions that change data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may run unverified downloaded code and install or update additional agent skills with uncertain effects.

Mitigation: Review the CLI setup and any additional skills before installation; the remote installers could not be inspected.

Risk: The integration can change Amazing Marvin data through write actions.

Mitigation: Confirm the exact action and payload before each data change.

## Reference(s):

- [Amazing Marvin](https://amazingmarvin.com/)
- [Amazing Marvin API documentation](https://help.amazingmarvin.com/amazing-marvin/api-getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include tasks, projects, categories, labels, and dates.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
