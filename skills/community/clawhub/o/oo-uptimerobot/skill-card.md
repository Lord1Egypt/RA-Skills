## Description: <br>
UptimeRobot (uptimerobot.com). Use this skill for reading, creating, updating, and deleting UptimeRobot data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage UptimeRobot monitors and account information from an agent session through the OOMOL oo CLI connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete UptimeRobot monitors in the connected account. <br>
Mitigation: Review the exact payload and target before approving write or destructive actions, especially monitor deletion. <br>
Risk: The skill requires access to an OOMOL-connected UptimeRobot account. <br>
Mitigation: Use an OOMOL/UptimeRobot connection with the minimum scopes acceptable for the intended work. <br>


## Reference(s): <br>
- [UptimeRobot homepage](https://uptimerobot.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-uptimerobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed JSON payloads for schema-checked UptimeRobot connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
