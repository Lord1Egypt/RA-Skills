## Description:

Use the oo CLI to search and read Intelliprint backgrounds, mailing lists, recipients, and print jobs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to retrieve Intelliprint records, including mailing lists, recipients, backgrounds, and print jobs. It guides the agent to inspect each action's live schema and return the resulting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup can run downloaded code, and the external CLI and connector implementations were not verified.

Mitigation: Review the CLI installation instructions and installer, and check any bundled agent-skill changes before installing or running the skill.

Risk: OOMOL mediates account credentials and Intelliprint requests.

Mitigation: Understand this credential and request flow before connecting the account, and use the skill only with an account you intend to authorize through OOMOL.

## Reference(s):

- [Intelliprint API documentation](https://docs.intelliprint.net/)
- [Intelliprint](https://www.intelliprint.net)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses and Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieved records follow each action's live schema and may include pagination or filtering fields.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
