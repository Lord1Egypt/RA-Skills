## Description:

Use a connected Mixmax account to find sequences and recipients, and add recipients to sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to list Mixmax sequences, search and inspect recipients, and add selected recipients to a sequence through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup depends on a downloaded CLI installer that was not verified in this review.

Mitigation: Review and approve a verified CLI installation separately before enabling the skill.

Risk: The CLI may automatically change other agents’ installed skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 as documented by upstream, and retain user confirmation before adding or scheduling recipients.

## Reference(s):

- [Mixmax](https://www.mixmax.com/)
- [Mixmax API documentation](https://developer.mixmax.com/reference/getting-started-with-the-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results are returned as JSON; adding recipients changes Mixmax state and requires user confirmation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
