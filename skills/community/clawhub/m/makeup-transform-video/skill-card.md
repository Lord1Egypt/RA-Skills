## Description: <br>
Generates short anthropomorphic animal makeup transformation videos, from bare-faced starting frames to polished beauty looks, using confirmed prompts and WeryAI video-generation parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agent users use this skill to plan and run short vertical makeup-transformation video generations for anthropomorphic animal characters. The skill helps gather makeup style, character, and contrast preferences, confirms parameters before execution, and calls the WeryAI CLI workflow when approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, or image inputs may be sent to WeryAI during generation. <br>
Mitigation: Use the skill only with inputs appropriate for WeryAI processing and review WERYAI_BASE_URL before execution. <br>
Risk: Generation requests can consume WeryAI account credits. <br>
Mitigation: Confirm model, duration, aspect ratio, prompt, and audio settings before submitting generation jobs. <br>
Risk: The CLI requires an API key for models, generation, and status checks. <br>
Mitigation: Use a dedicated WERYAI_API_KEY where possible and avoid sharing it in prompts, logs, or generated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/makeup-transform-video) <br>
- [WeryAI API base URL](https://api.weryai.com) <br>
- [WeryAI model registry](https://api-growth-agent.weryai.com/growthai/v1/video/models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with parameter tables, inline shell commands, and JSON CLI responses containing task status and generated video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and WERYAI_API_KEY; generation may use WeryAI account credits and may send prompts, image URLs, or image inputs to WeryAI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
