## Description:

Enables an agent to operate an OOMOL-connected Instagram professional account through the oo CLI for account, media, and insight retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Instagram professional-account profile, media, and insight data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a broad routing instruction for Instagram tasks, which can steer unrelated Instagram browsing requests through the connector.

Mitigation: Use the skill only for tasks that need the connected Instagram professional account and its supported read actions.

Risk: The setup guidance includes remote installer commands that were flagged for review.

Mitigation: Prefer a signed or checksum-verified oo CLI installation path before running installer commands.

Risk: The skill processes Instagram professional-account data through OOMOL-connected credentials.

Mitigation: Confirm the user intends to use the connected account and avoid sending unrelated or unnecessary Instagram data through the connector.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-instagram)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md)
- [Instagram Homepage](https://www.instagram.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include data and meta.executionId; action payloads should be built from the live action schema.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
