## Description: <br>
Operates Dailybot through an OOMOL-connected account for reading workspace data and sending confirmed messages or emails via the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users who manage Dailybot workspaces use this skill to inspect authenticated account, organization, team, and user data, open direct conversations, and send confirmed Dailybot messages or email notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Dailybot workspace through an OOMOL-connected account. <br>
Mitigation: Install and use it only when the user intends to let the OOMOL CLI operate that Dailybot workspace. <br>
Risk: Write actions can send Dailybot chat messages or email notifications. <br>
Mitigation: Review and approve the exact payload and expected effect with the user before running write actions. <br>
Risk: Setup and connection steps may open authentication or billing flows unnecessarily. <br>
Mitigation: Use setup, login, connection, or billing steps only after a command fails with the matching auth, connection, credit, or missing CLI error. <br>


## Reference(s): <br>
- [Dailybot homepage](https://www.dailybot.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Dailybot skill page](https://clawhub.ai/oomol/oo-dailybot) <br>
- [Dailybot metadata icon](https://static.oomol.com/logo/third-party/dailybot.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector runs return JSON with data and meta.executionId when the oo CLI action is executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
