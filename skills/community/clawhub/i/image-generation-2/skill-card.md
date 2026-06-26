## Description: <br>
Single-gateway image generation CLI for async text-to-image and image-to-image, with polling, download handling, and request alignment to the current gateway OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative teams, and agents use this skill to generate or transform images through a WeryAI-backed CLI workflow. It supports prompt assembly, style presets, model defaults, batch jobs, polling, and download handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to the WeryAI gateway. <br>
Mitigation: Avoid sensitive prompts or reference images unless the user intends to upload them to that service. <br>
Risk: The skill uses IMAGE_GEN_API_KEY and can persist local setup files when configured. <br>
Mitigation: Use a project-scoped key with limited billing exposure, keep credentials out of shared workspaces, and rotate or remove the key when access should end. <br>
Risk: The security verdict is suspicious because the skill gives the agent broad setup and credential-handling authority. <br>
Mitigation: Review tool-install prompts and setup changes before enabling the skill in a workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/632657122/image-generation-2) <br>
- [WeryAI Platform Notes](references/weryai-platform.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [WeryAI API Introduction](https://docs.weryai.com/en) <br>
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>
- [WeryAI Task Status API](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files, API calls] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON summaries, configuration files, and downloaded image files or image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write output images and optional local configuration under project or user .image-skills/image-generation directories.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
