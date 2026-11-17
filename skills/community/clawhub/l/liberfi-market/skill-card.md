## Description:

Liberfi Market helps agents fetch and present public trending-token and newly listed-token rankings across supported blockchains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover trending or newly listed tokens, compare rankings by chain and time window, and identify tokens for follow-up research before interacting with them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary states that the skill tells agents to silently install a global npm CLI.

Mitigation: Manually install or approve a pinned, reviewed LiberFi CLI version in an isolated environment before enabling the skill.

Risk: The security summary states that the skill tells agents to hide certain installation failures from the user.

Mitigation: Require the agent to report installation failures truthfully and stop until the user approves retry or remediation.

Risk: Token rankings and new-token lists can be mistaken for an endorsement or safety signal.

Mitigation: Present rankings as informational discovery only and run a token security audit before any trading or interaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombmod/skills/liberfi-market)
- [LiberFi homepage](https://liberfi.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and tables, with inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON CLI output as source data for ranked token summaries.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
