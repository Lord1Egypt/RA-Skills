## Description: <br>
one-mail is a unified email-management CLI for Gmail, Outlook, and NetEase Mail accounts that helps agents fetch, read, search, send, and summarize mailbox activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangbaixun](https://clawhub.ai/user/huangbaixun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical operators, and agent users can use this skill to configure mailbox accounts, retrieve and search messages across providers, send email, and inspect mailbox statistics from shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived mailbox credentials locally. <br>
Mitigation: Use only accounts where persistent local access is acceptable and protect ~/.onemail/credentials.json with strict file permissions and local access controls. <br>
Risk: Unsafe command construction could allow crafted email arguments to execute unintended commands. <br>
Mitigation: Inspect generated send and search commands before execution and avoid untrusted or agent-generated email fields until the command-construction issues are fixed. <br>
Risk: Automated email workflows can send, reply to, forward, or search sensitive mailbox content without enough human review. <br>
Mitigation: Avoid unattended auto-reply or forwarding workflows and require human review before sending messages or processing sensitive mailbox data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangbaixun/one-mail) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON email results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local mailbox configuration under ~/.onemail/ and may call provider APIs through CLI scripts.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
