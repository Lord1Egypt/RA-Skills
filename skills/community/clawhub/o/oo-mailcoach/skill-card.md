## Description:

Operate Mailcoach email lists and subscriber records through a connected account using the OOMOL oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Mailcoach users can manage email lists and subscriber records through their connected account. The skill supports reading records and making requested changes, including subscriptions, updates, confirmations, and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup includes an automatic installer fallback for a downloaded CLI whose contents were not verified.

Mitigation: Review and install the CLI separately from a verified release before enabling the skill.

Risk: Write and destructive actions can change or remove Mailcoach data.

Mitigation: Confirm the exact payload and effect before writes, and confirm the target with explicit approval before destructive actions; connect only the intended Mailcoach account.

## Reference(s):

- [Mailcoach](https://www.mailcoach.app)
- [Mailcoach API documentation](https://www.mailcoach.app/api-documentation/introduction/about-api/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and concise text summaries, using oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses and actions depend on the selected Mailcoach operation and its input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
