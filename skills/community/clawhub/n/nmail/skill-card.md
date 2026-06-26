## Description: <br>
nmail helps agents and humans configure, search, monitor, read, and send Naver and Daum email from a command-line interface with JSON output by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harlockius](https://clawhub.ai/user/Harlockius) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and email automation users use nmail to access Korean email providers through shell commands for inbox review, message search, message reading, new-mail polling, and outbound plain-text email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox app passwords are accepted and stored in ways the security evidence flags for review. <br>
Mitigation: Use a dedicated limited-scope app password where possible, avoid entering it directly on the command line, and protect or remove ~/.nmail/config.yaml when not needed. <br>
Risk: An agent using this skill can monitor mailbox contents and send email from configured accounts. <br>
Mitigation: Only configure mailboxes whose contents and send permissions are appropriate for the agent, and review before enabling watch or send workflows. <br>


## Reference(s): <br>
- [ClawHub nmail listing](https://clawhub.ai/Harlockius/nmail) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Harlockius) <br>
- [Naver account security settings](https://nid.naver.com/user2/help/myInfoV2) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented usage patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on configured local mailbox accounts and default to JSON output; pretty text output is available for human display.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
