## Description: <br>
Material Generator helps generate Unreal Engine material node graphs from natural language descriptions, including common nodes such as TextureSample, Multiply, Lerp, Constant, TexCoord, and MaterialOutput. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Unreal Engine material authors, technical artists, and developers use this skill to turn natural language material concepts into editable UE-style node graphs and example graph JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the skill publicly includes what appears to be a reusable MiniMax API key. <br>
Mitigation: Remove and rotate the exposed key, then require users to provide their own secret through protected configuration. <br>
Risk: The hosted workflow may send material prompts or project details through a publisher-controlled MiniMax integration. <br>
Mitigation: Avoid entering sensitive project details unless the publisher and MiniMax data handling path are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tianheihei002/material-generator) <br>
- [Hosted Material Generator app](https://k2lucelsen19.space.minimaxi.com) <br>
- [Example blood post-process material JSON](https://k2lucelsen19.space.minimaxi.com/BP_BloodPostProcess.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with URLs, configuration details, and example JSON references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated material graphs should be reviewed before use in Unreal Engine projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
