## Description:

Use the oo CLI to inspect Confluent organizations and Kafka clusters, and manage Confluent Cloud environments through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Confluent organizations, environments, and Kafka clusters, and to create, update, or delete environments through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install remote CLI software without a separate approval step; installer contents and the eventual installed release were not verified.

Mitigation: Review and approve CLI installation separately, preferably using a verified release.

Risk: The connected Confluent account can be used for environment changes and deletion.

Mitigation: Limit the account's permissions and retain confirmation for changes and deletions.

## Reference(s):

- [Confluent Cloud API documentation](https://docs.confluent.io/cloud/current/api-docs/cloud-overview.html)
- [Confluent](https://www.confluent.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON payloads and CLI results with Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Confluent account and requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
