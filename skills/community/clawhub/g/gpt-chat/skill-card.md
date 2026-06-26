## Description: <br>
GPT聊天 - 使用GPT模型进行对话和内容生成 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilisidu1210-ui](https://clawhub.ai/user/lilisidu1210-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to select supported GPT models and send prompts for conversational responses or generated content through Node.js scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and API credentials to an endpoint selected by OPENAI_API_BASE, including the default proxy endpoint in the main script. <br>
Mitigation: Use OPENAI_API_KEY from an environment variable or managed secret, and set OPENAI_API_BASE only to the official OpenAI API or another endpoint you explicitly trust. <br>
Risk: The included local server is unauthenticated and can allow callers who reach the port to use the configured API key for chat requests. <br>
Mitigation: Avoid running scripts/server.js unless access is restricted and authentication is added. <br>


## Reference(s): <br>
- [OpenAI API pricing](https://openai.com/api/pricing/) <br>
- [ClawHub skill page](https://clawhub.ai/lilisidu1210-ui/gpt-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and generated Markdown content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the selected GPT model and may write generated article content to a Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
