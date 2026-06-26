## Description: <br>
IMA Note helps an agent manage a user's personal IMA notes, including searching notes, browsing notebooks, reading note content, creating notes, and appending content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaolibuzai-ovo](https://clawhub.ai/user/xiaolibuzai-ovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search, read, create, and update personal notes in IMA through the IMA OpenAPI. It is intended for authorized note-management tasks where private note content should be handled carefully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify private IMA notes using the user's credentials. <br>
Mitigation: Treat IMA credentials as sensitive and confirm the target notebook, note, and content before creating or appending notes. <br>
Risk: Private note content may be exposed in shared or group contexts. <br>
Mitigation: Show only titles and summaries in shared contexts unless the authorized user explicitly requests note content. <br>


## Reference(s): <br>
- [IMA home page](https://ima.qq.com) <br>
- [IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [IMA Note API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaolibuzai-ovo/note-test1-limingzhi111111) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
