## Description: <br>
Generates images from text prompts or reference image URLs through the nano-banana2 imgEditNB2 API with optional aspect ratio and 1K, 2K, or 4K size settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runninghcm](https://clawhub.ai/user/runninghcm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create images from prompts, optionally using reference image URLs, aspect ratios, and image-size choices. It is suited for image generation requests such as posters, covers, and prompt-to-image or image-to-image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and the API key are sent to a third-party image-generation service. <br>
Mitigation: Install only if you trust agent.mathmind.cn and kexiangai.com with those inputs, and avoid sending sensitive prompts or private image URLs. <br>
Risk: The skill can optionally save X_API_KEY on disk for reuse. <br>
Mitigation: Prefer a session-scoped X_API_KEY; if local-key mode is used, keep the file restricted and rotate or delete ~/.config/nano-banana2/.env when it is no longer needed. <br>


## Reference(s): <br>
- [nano-banana2 API Guide](references/api-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/runninghcm/nano-banana2) <br>
- [imgEditNB2 API endpoint](https://agent.mathmind.cn/minimalist/api/imgEditNB2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell command examples and structured API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful API calls may return an image URL; use requires X_API_KEY and may optionally read a saved key only when the user enables local-key mode.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter remains 1.0.1 with no file changes in this release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
