## Description: <br>
WeCom Bot helps an agent send text, markdown, markdown_v2, image, and news messages through a WeCom bot webhook by using the OOMOL oo CLI and wecom_bot connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent prepare and send WeCom Bot webhook messages through an OOMOL-connected account. It is intended for confirmed message-sending workflows where the agent inspects the live connector schema before constructing payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WeCom Bot messages that change external communication state. <br>
Mitigation: Confirm the exact message payload and intended effect with the user before running any write action. <br>
Risk: The setup instructions include remote shell installer commands. <br>
Mitigation: Use a verified package or inspect the installer before execution, and run setup only after an auth or connection failure requires it. <br>
Risk: The routing language is broader than the listed message-sending actions. <br>
Mitigation: Treat the skill as scoped to WeCom Bot message sending and inspect the live connector schema before each action. <br>


## Reference(s): <br>
- [WeCom Bot homepage](https://work.weixin.qq.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-wecom-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to inspect live connector schemas before running message-sending actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
