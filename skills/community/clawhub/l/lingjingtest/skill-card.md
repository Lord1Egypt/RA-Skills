## Description: <br>
lingjingtest helps agents turn natural-language image and video generation requests into structured JoyCreator tasks, recommend a matching model, and submit JD Cloud JoyCreator API jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Scorpiongao](https://clawhub.ai/user/Scorpiongao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to prepare JoyCreator image or video generation jobs, select among Doubao, Hailuo, Kling, and PaiWo models, and produce API-ready requests or runnable command-line code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public media URLs are sent to JD Cloud JoyCreator using the user's App Key. <br>
Mitigation: Use a dedicated, revocable App Key and avoid confidential prompts, regulated data, or private images unless sharing them with JoyCreator through public URLs is acceptable. <br>
Risk: Credentials can be exposed if the App Key is pasted into commands, logs, or scripts. <br>
Mitigation: Prefer JOYCREATOR_APP_KEY or a hidden prompt over command-line arguments, and rotate the key if it may have been exposed. <br>
Risk: The skill can submit generation jobs to an external service after model selection. <br>
Mitigation: Review the recommended model, prompt, parameters, and media URLs before confirming each submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Scorpiongao/lingjingtest) <br>
- [Router rules](references/router-rules.md) <br>
- [Choice rules](references/choice-rules.md) <br>
- [Doubao API reference](references/doubao.md) <br>
- [Hailuo API reference](references/hailuo.md) <br>
- [Kling API reference](references/kling.md) <br>
- [PaiWo API reference](references/paiwo.md) <br>
- [JoyCreator task submission endpoint](https://model.jdcloud.com/joycreator/openApi/submitTask) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell or Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JoyCreator App Key and, for image-conditioned tasks, public media URLs; submitted jobs are polled through the JoyCreator service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
