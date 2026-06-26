## Description: <br>
Sends Murasame voice bubbles and matching Chinese text in Feishu chats using label and keyword mappings with manual voice toggles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxundaozu](https://clawhub.ai/user/chenxundaozu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu automation users can use this skill to send emotion-labeled Murasame voice responses while preserving readable Chinese text in the chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends real Feishu messages using configured credentials and receiver information. <br>
Mitigation: Use narrowly scoped Feishu credentials, confirm FEISHU_RECEIVER before use, and run only when sending messages to that receiver is intended. <br>
Risk: Voice sending depends on an unbundled feishu-voice helper script. <br>
Mitigation: Review and scan the helper script before enabling voice delivery. <br>
Risk: Outgoing text may be stored in a local debug file. <br>
Mitigation: Remove the debug write or accept and monitor the local file before using the skill with sensitive chat content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenxundaozu/murasame-feishu-voice) <br>
- [mapping.json](references/mapping.json) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu credentials, a receiver OpenID, ffmpeg/ffprobe, local Murasame audio files, and the referenced Feishu voice helper script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
