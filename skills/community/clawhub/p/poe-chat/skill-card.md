## Description: <br>
Uses @gemini, @gpt, @claude, and similar trigger words to call Poe models, select a concrete model ID, state which model was used, and support file uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longmans](https://clawhub.ai/user/longmans) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to route prompts and optional local files to a selected Poe model from an agent workflow. It helps inspect available Poe models, choose a concrete model ID, and return the model response with the model name clearly identified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and files passed to the skill are sent to Poe and its model providers. <br>
Mitigation: Use the skill only when that data transfer is intended, avoid uploading secrets or regulated/private documents, and review files before using --file. <br>
Risk: Supplying Poe API keys on the command line may expose credentials through shell history or process listings. <br>
Mitigation: Prefer the POE_API_KEY environment variable over command-line keys. <br>
Risk: Dependencies are not pinned in scripts/requirements.txt. <br>
Mitigation: Pin reviewed dependency versions before production use. <br>


## Reference(s): <br>
- [Poe models API endpoint](https://api.poe.com/v1/models) <br>
- [ClawHub skill page](https://clawhub.ai/longmans/poe-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown and terminal text output with optional JSON model-list files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses begin with the concrete Poe model ID used; optional returned attachments are listed with name, content type, and URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
