## Description: <br>
Enables an agent to operate Pushover through an OOMOL-connected account for notification delivery, group management, Open Client workflows, and account utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send and manage Pushover notifications, delivery groups, client sessions, and related account utilities through an OOMOL-connected Pushover account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Pushover-connected OOMOL account. <br>
Mitigation: Install and use it only when that account access is acceptable for the intended workspace and task. <br>
Risk: Authentication-related or credential-returning actions may expose, store, or rely on sensitive Pushover or Teams tokens. <br>
Mitigation: Require explicit confirmation before actions that return or store tokens, log in a client, register a device, open a client session, or persist Team API token data. <br>
Risk: Write or destructive actions can send notifications, change groups or teams, assign licenses, alter receipts, or acknowledge and delete messages. <br>
Mitigation: Confirm the exact action, target, payload, and expected effect with the user before running write or destructive actions. <br>


## Reference(s): <br>
- [Pushover homepage](https://pushover.net) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-pushover) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions can return JSON data and may change Pushover state depending on the selected action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
