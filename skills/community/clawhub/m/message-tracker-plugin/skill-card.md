## Description: <br>
Sends formatted tracked messages to Feishu channels through a configurable webhook with retry handling for failed pushes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjl1004](https://clawhub.ai/user/wjl1004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect tracked message events to a Feishu channel, format the outgoing notification payload, and configure webhook authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracked message content may include confidential or regulated information before it is forwarded to the configured Feishu channel. <br>
Mitigation: Use only approved Feishu destinations and avoid forwarding sensitive content unless the organization has authorized that workflow. <br>
Risk: Webhook URLs and signing secrets can grant notification access if exposed in source code or logs. <br>
Mitigation: Store webhook URLs and signing secrets in an approved secret store and keep them out of source files, prompts, and logs. <br>
Risk: Automatic retry behavior can resend failed notifications and may create duplicate channel messages. <br>
Mitigation: Account for up to three retry attempts in downstream monitoring and message handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wjl1004/message-tracker-plugin) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with a JavaScript usage example and configuration table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The configured plugin sends tracked message content to a Feishu webhook and retries failed pushes up to three times.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
