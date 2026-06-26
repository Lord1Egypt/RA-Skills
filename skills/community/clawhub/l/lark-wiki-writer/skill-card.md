## Description: <br>
Creates Lark/Feishu wiki documents from Markdown content with support for headings, rich text, lists, links, code blocks, and document validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to validate Lark/Feishu app credentials and create wiki documents from inline Markdown or Markdown files. It is intended for teams that need agent-assisted publishing into a configured Lark/Feishu knowledge space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Lark/Feishu app credentials and can access workspace content. <br>
Mitigation: Use a least-privilege Lark/Feishu app, provide credentials through environment variables or approved secret storage, and rotate or revoke credentials after testing. <br>
Risk: The skill can create or modify business documents in a configured wiki space. <br>
Mitigation: Confirm the target space ID, parent node token, title, and Markdown content before execution, especially in shared or production workspaces. <br>
Risk: Markdown content may include sensitive or unintended business information before it is sent to Lark/Feishu APIs. <br>
Mitigation: Review source Markdown files and generated content for confidential data before publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/griffithkk3-del/lark-wiki-writer) <br>
- [Publisher profile](https://clawhub.ai/user/griffithkk3-del) <br>
- [Lark Open Platform app console](https://open.larksuite.com/app) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [config.example.json](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, JSON configuration examples, and Python API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can issue authenticated Lark/Feishu API calls that create and write wiki documents when credentials and workspace identifiers are supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
