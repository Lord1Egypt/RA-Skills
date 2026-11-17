## Description:

Automates Kmong sign-up, identity verification, profile setup, and service registration using OpenClaw browser with SMS and captcha handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide an agent through creating and preparing a Kmong expert seller account, including registration, profile setup, and service listing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent through sensitive identity verification, including national-ID digits, SMS codes, CAPTCHA/security characters, and screenshots that may contain identity data.

Mitigation: Use it only for an authorized Kmong account, keep identity verification and seller-term confirmation in the official browser interface, and do not allow the agent to view or store sensitive identity data or verification codes.

Risk: The server security verdict is suspicious because the registration helper lacks adequate safeguards around sensitive verification flows.

Mitigation: Review the skill carefully before installing or running it, and restrict use to trusted workspaces with no credential or screenshot retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/kmong)
- [Kmong](https://kmong.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with browser automation steps and inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local secret and workspace configuration paths for account details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
