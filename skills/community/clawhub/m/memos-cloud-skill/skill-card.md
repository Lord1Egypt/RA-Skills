## Description: <br>
External long-term memory and knowledge base backed by the MemOS Cloud API for memory search, message storage, feedback-based correction, profile retrieval, and knowledge base document management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuisu](https://clawhub.ai/user/xiaohuisu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent persistent MemOS Cloud memory, user profile retrieval, and knowledge base management across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content may be sent to and retained by a third-party MemOS Cloud service by default. <br>
Mitigation: Deploy only where that storage behavior is approved, configure credentials through the host environment, and avoid use in chats containing secrets, regulated data, or private documents unless policy permits it. <br>
Risk: Delete commands and knowledge-base uploads can change or expose stored data without strong recovery controls shown in the artifact. <br>
Mitigation: Require operator review for delete and upload actions, verify target memory or file IDs before execution, and keep independent backups or recovery procedures for important knowledge bases. <br>
Risk: The skill requires sensitive credentials for MemOS Cloud access. <br>
Mitigation: Provide MEMOS_API_KEY and MEMOS_USER_ID through deployment-managed environment variables, never expose the token in prompts or logs, and rotate credentials if they may have been disclosed. <br>


## Reference(s): <br>
- [ClawHub release: Memos Cloud Server](https://clawhub.ai/xiaohuisu/memos-cloud-skill) <br>
- [Publisher profile: xiaohuisu](https://clawhub.ai/user/xiaohuisu) <br>
- [MemOS Cloud API endpoint](https://memos.memtensor.cn/api/openmem/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMOS_API_KEY and MEMOS_USER_ID; may upload local files or URLs to a configured knowledge base.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
