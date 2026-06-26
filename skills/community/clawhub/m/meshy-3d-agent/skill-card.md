## Description: <br>
Generate 3D models, textures, images, rigged characters, animations, and 3D print ready assets through the Meshy AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arlieeee](https://clawhub.ai/user/arlieeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and 3D printing users use this skill to generate or transform Meshy assets, manage asynchronous API tasks, download model outputs, and prepare files for printing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meshy API requests can spend paid credits. <br>
Mitigation: Require a clear cost summary and explicit user confirmation before creating paid Meshy tasks. <br>
Risk: Prompts, image URLs, or selected local image data may be sent to Meshy. <br>
Mitigation: Disclose the data transfer and use only user-provided or user-approved inputs for API calls. <br>
Risk: Console logs may include an API key prefix. <br>
Mitigation: Treat logs as sensitive and avoid exposing the full API key in output, files, or shared artifacts. <br>
Risk: The skill can detect or open local slicer applications. <br>
Mitigation: Ask for explicit approval before probing for slicers or opening local applications. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/arlieeee/skills/meshy-3d-agent) <br>
- [Meshy API documentation](https://docs.meshy.ai) <br>
- [Meshy API reference](artifact/reference.md) <br>
- [Meshy API endpoint](https://api.meshy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Meshy API tasks after user confirmation and save generated assets under meshy_output/.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
