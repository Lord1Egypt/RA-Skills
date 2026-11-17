## Description:

Controls JFTech smart door locks by checking lock support, logging in, retrieving device access tokens, reading configuration, and sending remote unlock commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and device operators use this skill to manage bound JFTech smart door locks, verify device capabilities, retrieve access tokens, inspect lock configuration, and perform authorized remote unlock operations.

### Deployment Geography for Use:

China mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Remote unlock operations can open a physical door if invoked without explicit approval.

Mitigation: Require explicit human confirmation before unlock actions and tightly control who can invoke the skill.

Risk: Lock passwords, app credentials, and printed DeviceToken values are sensitive credentials.

Mitigation: Avoid passing real lock passwords on the command line, store credentials through controlled secret handling, and limit exposure of printed token values.

Risk: Changing the API endpoint can send smart-lock requests outside the documented vendor hosts.

Mitigation: Keep JF_ENDPOINT fixed to a documented JFTech hostname for the intended region.

## Reference(s):

- [JFTech Open Platform Documentation](https://docs.jftech.com)
- [ClawHub skill listing](https://clawhub.ai/jftech/skills/jf-open-pro-smart-doorlock-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command-line examples and text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print device tokens and lock operation status; treat DeviceToken values as sensitive temporary credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
