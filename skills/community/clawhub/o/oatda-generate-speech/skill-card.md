## Description: <br>
Generate speech or audio from text using OATDA's unified audio API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert text into spoken audio, narration, voiceovers, or accessibility audio through OATDA's speech API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech synthesis is sent to OATDA. <br>
Mitigation: Avoid sending secrets, regulated data, or confidential drafts unless that data flow is acceptable for the use case. <br>
Risk: The skill requires an OATDA API key to call the speech and model-discovery endpoints. <br>
Mitigation: Use a scoped API key where possible and verify only that the key exists instead of printing the full value. <br>


## Reference(s): <br>
- [OATDA Homepage](https://oatda.com) <br>
- [OATDA Audio Models Endpoint](https://oatda.com/api/v1/llm/models?type=audio) <br>
- [OATDA Speech Endpoint](https://oatda.com/api/v1/llm/speech) <br>
- [ClawHub Skill Page](https://clawhub.ai/devcsde/oatda-generate-speech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a saved audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an OATDA API key; speech responses are saved as local audio files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
