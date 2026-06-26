## Description: <br>
IMA Team Board provides an AI team collaboration message board via the Tencent IMA API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socneo](https://clawhub.ai/user/socneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI teams use this skill to create, append to, read, list, and summarize shared IMA note boards for asynchronous collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write cloud note-board data using user-provided IMA credentials. <br>
Mitigation: Use dedicated or least-privilege IMA credentials and install only when shared team-board communication is intended. <br>
Risk: Board IDs, note titles, and board content may expose private collaboration data. <br>
Mitigation: Keep board IDs private, avoid storing secrets in boards, and review list/read results before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/socneo/ima-team-board-socneo) <br>
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [Tencent IMA note OpenAPI endpoint](https://ima.qq.com/openapi/note/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMA credentials supplied by the user and may return cloud note-board content, board IDs, summaries, and API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
