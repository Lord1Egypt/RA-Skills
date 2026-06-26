## Description: <br>
Converts text to speech with Edge TTS and sends audio, or paired text and audio, to Feishu using credentials supplied through environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayiv-ai](https://clawhub.ai/user/mayiv-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to send generated voice messages, or combined text and voice summaries, to Feishu from agent workflows or shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message content is transmitted to external TTS and Feishu services. <br>
Mitigation: Use the skill only for content approved for those services by the deploying organization. <br>
Risk: Credentials or recipient IDs with excessive scope can cause unintended message delivery. <br>
Mitigation: Use least-privilege Feishu app credentials and verify the recipient ID before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayiv-ai/mayiv-feishu-voice) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends user-provided content to Edge TTS and Feishu services when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
