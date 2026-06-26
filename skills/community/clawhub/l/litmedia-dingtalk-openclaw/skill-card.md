## Description: <br>
Connects DingTalk Stream mode to OpenClaw AI conversations by receiving DingTalk bot messages, calling the OpenClaw HTTP API for replies, and sending responses back through a DingTalk webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongshendota](https://clawhub.ai/user/tongshendota) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a DingTalk AI assistant that relays chat messages to a local OpenClaw HTTP API and posts AI replies back to DingTalk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DingTalk secrets, OpenClaw tokens, or webhook URLs could be exposed during setup or operation. <br>
Mitigation: Keep credentials private, restrict access to the bot configuration, and avoid committing tokens or webhook URLs. <br>
Risk: Chat text is forwarded to OpenClaw and may be written to logs. <br>
Mitigation: Use the bot only in approved conversations and redact or disable message logs when privacy requirements call for it. <br>
Risk: Runtime dependencies and bot permissions may be unsuitable for production without review. <br>
Mitigation: Review and pin Python dependencies, limit the bot to approved DingTalk conversations, and validate the processed-message file handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tongshendota/litmedia-dingtalk-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps and example bot configuration; users provide DingTalk and OpenClaw credentials, tokens, and webhook URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
