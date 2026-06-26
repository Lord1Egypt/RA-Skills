## Description: <br>
DingTalk Bot helps agents send DingTalk custom bot messages through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send text, markdown, link, feed card, and action card messages to DingTalk custom bot webhooks through an OOMOL-connected DingTalk Bot account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages through an OOMOL-connected DingTalk webhook. <br>
Mitigation: Review the message content, target, payload, and expected effect before approving any write action. <br>
Risk: The optional oo CLI installer executes a remote install script. <br>
Mitigation: Run the installer only when the CLI is needed and only if the installer source is trusted. <br>
Risk: The skill depends on an active OOMOL account connection and server-side credentials. <br>
Mitigation: Install it only for environments where OOMOL-managed DingTalk Bot access is intended and authorized. <br>


## Reference(s): <br>
- [DingTalk Bot ClawHub Page](https://clawhub.ai/oomol/oo-dingtalk-bot) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [DingTalk](https://www.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to inspect live connector schemas before building payloads and to confirm write actions before sending messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
