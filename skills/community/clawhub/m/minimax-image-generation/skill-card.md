## Description: <br>
Generates images with MiniMax image-01 and image-01-live models, supporting text-to-image, image-to-image, multiple aspect ratios, and optional styles with a MiniMax API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanycun](https://clawhub.ai/user/wanycun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call MiniMax's Coding Plan image generation API from the command line for prompt-based image creation and optional image-to-image transformations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and optional input image URLs to MiniMax for processing. <br>
Mitigation: Avoid sensitive prompts or private image URLs unless MiniMax processing is acceptable for the intended use. <br>
Risk: The skill requires a MiniMax API key for API calls. <br>
Mitigation: Use a revocable API key and provide it through the MINIMAX_API_KEY environment variable rather than embedding secrets in commands or files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanycun/minimax-image-generation) <br>
- [MiniMax API key page](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Command-line text or JSON containing generated image URLs and task metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can request URL or base64 response formats; returned image URLs are documented as valid for 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
