## Description: <br>
Kling AI Image Generation API tool that supports text-to-image, image-to-image, multi-image reference generation, Omni-Image, image expansion, and task management through Kling API scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UMRzcz-831](https://clawhub.ai/user/UMRzcz-831) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Kling API credentials, submit image generation or image editing tasks, poll task status, and retrieve task results for creative image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image inputs or image URLs, callback URLs, and task metadata are sent to Kling's API. <br>
Mitigation: Use the skill only for data suitable for Kling processing, avoid sensitive callback URLs, and review inputs before submitting tasks. <br>
Risk: Kling API keys are required for JWT authentication. <br>
Mitigation: Keep KLING_ACCESS_KEY and KLING_SECRET_KEY private, prefer dedicated or limited keys, and store them only in the local environment. <br>
Risk: Python dependencies are installed from package indexes. <br>
Mitigation: Install dependencies in a virtual environment and pin versions when deploying the skill. <br>


## Reference(s): <br>
- [Kling Image Generate on ClawHub](https://clawhub.ai/UMRzcz-831/kling-image-generate) <br>
- [UMRzcz-831 publisher profile](https://clawhub.ai/user/UMRzcz-831) <br>
- [English API reference](references/api-reference.en.md) <br>
- [Chinese API reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit prompts, image references, callback URLs, and task metadata to Kling's API; generated image results are returned through Kling task responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
