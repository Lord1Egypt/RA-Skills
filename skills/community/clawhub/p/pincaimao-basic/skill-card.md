## Description: <br>
聘才猫平台基础能力 Use when calling any Pincaimao platform API — file upload, presigned URL, conversation list, message history, audio-to-text, resume JSON upload, or the base chat-messages interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Pincaimao platform APIs for authenticated chat, file upload, temporary file links, conversation retrieval, audio transcription, and structured resume JSON upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can send recruiting files, structured resume data, job descriptions, contract text, and audio-derived content to api.pincaimao.com. <br>
Mitigation: Confirm the user is authorized to share the data before calling the APIs and avoid uploading data outside the intended recruiting workflow. <br>
Risk: API keys, cos_key paths, presigned URLs, and temporary file URLs can expose access to sensitive recruiting data. <br>
Mitigation: Keep API keys in environment variables, do not hardcode or log credentials, and treat returned cos_key paths and temporary URLs as sensitive. <br>
Risk: Using a general key for agent chat or mixing keys between agents can cause authentication failures or unintended access patterns. <br>
Mitigation: Use agent-specific keys for chat-messages and PCM_ANY_KEY only for the documented non-chat endpoints. <br>


## Reference(s): <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-basic) <br>
- [Pincaimao API key registration](https://www.pincaimao.com/agents/login?invite_code=uwqc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PCM_ANY_KEY or agent-specific API keys and returns API responses such as answers, conversation data, file URLs, transcriptions, and cos_key values.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
