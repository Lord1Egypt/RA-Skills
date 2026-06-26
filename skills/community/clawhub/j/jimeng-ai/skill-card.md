## Description: <br>
基于火山引擎即梦AI的文生图/文生视频能力，支持通过文本描述生成图片和视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogenes](https://clawhub.ai/user/ogenes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to submit and query VolcEngine Jimeng AI text-to-image and text-to-video generation jobs from prompts, then retrieve generated media and task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to VolcEngine for image or video generation. <br>
Mitigation: Avoid submitting sensitive prompts or confidential generation requirements unless that use is approved for the VolcEngine account and environment. <br>
Risk: VolcEngine credentials are provided through environment variables, and debug mode may expose operational details in shared logs. <br>
Mitigation: Use temporary or least-privileged credentials where possible and avoid debug mode in shared terminals, CI, or support sessions. <br>
Risk: Task metadata and generated media are stored locally in output folders. <br>
Mitigation: Keep output folders out of source control and store generated files only in locations appropriate for their sensitivity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ogenes/jimeng-ai) <br>
- [VolcEngine Jimeng AI text-to-image documentation](https://www.volcengine.com/docs/85621/1820192) <br>
- [VolcEngine Jimeng AI text-to-video documentation](https://www.volcengine.com/docs/85621/1792702) <br>
- [VolcEngine Console](https://console.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files] <br>
**Output Format:** [Markdown guidance with CLI commands, structured JSON status, and local image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task metadata and generated media under prompt-hash output folders unless a custom output directory is provided.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
