## Description: <br>
Guides agents in reading Feishu IM conversation history, thread replies, cross-chat search results, and message attachments that the user is authorized to access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to retrieve Feishu chat history, inspect thread replies, search messages across conversations, or download message resources such as images, files, audio, or video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu messages and downloaded attachments may contain sensitive or private information. <br>
Mitigation: Keep searches narrowly scoped to the user's request and retrieve only conversations and resources the user is authorized to access. <br>
Risk: Images, files, audio, or video attachments can create retained local copies of sensitive content. <br>
Mitigation: Ask the user to confirm before downloading attachments and remove downloaded copies when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenfa188/openclaw-feishu-im-read) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, API calls] <br>
**Output Format:** [Markdown guidance with JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides Feishu message retrieval, search, pagination, thread expansion, and attachment download decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
