## Description: <br>
MiniMax image generation tool supporting text-to-image and image-to-image generation with 1-9 images per request and customizable aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang92229](https://clawhub.ai/user/lixiang92229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images from text prompts or reference images through MiniMax, selecting aspect ratio, output count, style options, and output location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to MiniMax for generation. <br>
Mitigation: Use only prompts and reference images that are appropriate to share with MiniMax, and avoid private or sensitive reference photos. <br>
Risk: The skill requires a MiniMax API key and can incur service usage. <br>
Mitigation: Use a limited MiniMax API key, keep it in the MINIMAX_API_KEY environment variable, and avoid committing credentials. <br>
Risk: Generated image files and the local call log may expose prompt summaries, counts, aspect ratios, and saved paths if the workspace is shared or synced. <br>
Mitigation: Choose output paths deliberately and delete generated files or the local log before sharing or syncing the workspace. <br>


## Reference(s): <br>
- [MiniMax Image Generation API Reference](references/api_en.md) <br>
- [MiniMax Image Generation API Reference (Chinese)](references/api.md) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [Project homepage](https://github.com/lixiang92229/lx-minimax-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, API Calls, Shell commands] <br>
**Output Format:** [JSON responses with image URLs, base64 data, and local image file paths; optional shell command examples for CLI use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs may expire after 24 hours; successful calls append a local Markdown usage log.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
