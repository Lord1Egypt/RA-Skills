## Description: <br>
IMA personal-note API skill for searching, browsing, reading, creating, and appending to a user's IMA notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzswk](https://clawhub.ai/user/yzswk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents with authorized IMA credentials use this skill to search personal notes, browse notebooks, read note content, create Markdown notes, and append content through the IMA OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify private IMA notes, and evidence flags broad activation with write access as needing user review. <br>
Mitigation: Use explicit prompts for searches and writes, and review the target notebook or note plus the exact content before any create or append action. <br>
Risk: Personal note content may be exposed in shared or group-chat contexts. <br>
Mitigation: Show only titles and summaries in group contexts, and avoid displaying full note content unless the user explicitly authorizes it in an appropriate private context. <br>
Risk: Vague requests such as saving or finding prior writing could be misinterpreted as note operations. <br>
Mitigation: Confirm intent before writes or broad searches, especially when the request does not explicitly mention IMA notes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yzswk/ima-skills-1-0-4) <br>
- [IMA homepage](https://ima.qq.com) <br>
- [IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [IMA note API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API request bodies and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY; read and write actions operate on the user's IMA notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
