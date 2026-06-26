## Description: <br>
OpenClaw two-step pipeline that expands a user brief into a three-shot storyboard, saves it to storyboard/storyboard.json, and runs scripts/video-generate.py to call Zhipu CogVideoX-3 three times for 10-second clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilaus](https://clawhub.ai/user/ilaus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to convert a short video idea into a three-segment storyboard JSON, then submit those prompts to Zhipu CogVideoX-3 to generate three 10-second video clips. It is suited for OpenClaw storyboard-to-video workflows where the final 30-second result can be assembled from separate generated clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls Zhipu's video API with the user's API key. <br>
Mitigation: Keep ZHIPUAI_API_KEY out of source control and chat logs, and install the skill only when Zhipu CogVideoX-3 usage is intended. <br>
Risk: Storyboard prompts may contain confidential or sensitive content that is sent to an external video-generation service. <br>
Mitigation: Review storyboard/storyboard.json before running the script and avoid confidential prompt content. <br>
Risk: Changing BIGMODEL_API_BASE can redirect requests to an alternate endpoint. <br>
Mitigation: Override BIGMODEL_API_BASE only when the endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilaus/openclaw-video-pipeline) <br>
- [CogVideoX-3 model guide](https://docs.bigmodel.cn/cn/guide/models/video-generation/cogvideox-3) <br>
- [Zhipu video generation async API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E5%BC%82%E6%AD%A5) <br>
- [Zhipu async result query API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%9F%A5%E8%AF%A2%E5%BC%82%E6%AD%A5%E7%BB%93%E6%9E%9C) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON storyboard files, shell commands, video URLs, and optional downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPUAI_API_KEY; accepts storyboard JSON with exactly three prompts or segments and can save outputs as segment_01.mp4 through segment_03.mp4.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
