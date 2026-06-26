## Description: <br>
Novel Workshop generates, reviews, revises, and archives prompt-based fiction with multiple LLMs, with optional Feishu progress updates and document storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicaldd](https://clawhub.ai/user/magicaldd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers and agent users can provide a fiction prompt and receive a generated draft, parallel critiques, a revised story, a local Markdown archive, and an optional Feishu document with progress messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated manuscripts can be sent to OpenRouter-backed models and stored in Feishu. <br>
Mitigation: Review prompts before running the workflow, avoid sensitive material, and add confirmation, redaction, or a local-only option when needed. <br>
Risk: The workflow can send and share full generated content to hard-coded Feishu chat, folder, and owner destinations. <br>
Mitigation: Set user-controlled Feishu chat, folder, and owner values, and remove hard-coded defaults or automatic full_access grants before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicaldd/novel-workshop) <br>
- [Publisher profile](https://clawhub.ai/user/magicaldd) <br>
- [OpenRouter API endpoint used by workflow](https://openrouter.ai/api/v1) <br>
- [Feishu token API endpoint used by workflow](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu messaging API endpoint used by workflow](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown files, Feishu documents, progress messages, and a JSON summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenRouter-backed models and optional Feishu storage; generated content may be sent to external services.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
