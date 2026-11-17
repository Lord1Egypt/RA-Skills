## Description:

Use this skill to read and manage ClickSend contacts and lists, calculate SMS prices, and send SMS through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use an agent to work with a connected ClickSend account, including reading account and contact data, managing contacts and lists, calculating SMS prices, and sending messages. The skill requires confirmation before writes and explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill setup may execute downloaded installer code and introduce broader agent changes through automatic skill synchronization.

Mitigation: Review and approve the CLI installation before setup commands; consider disabling automatic synchronization with the publisher-documented OO_SKILLS_SYNC_DISABLED setting.

Risk: Sending messages and changing or deleting contacts can affect the connected ClickSend account.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for the target before destructive actions.

## Reference(s):

- [ClickSend homepage](https://www.clicksend.com/)
- [ClickSend API documentation](https://developers.clicksend.com/docs/#authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON connector responses with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the requested ClickSend action; state-changing actions require confirmation under the skill's safety rules.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
