## Description: <br>
Generate high-quality images from text descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn text prompts into image-generation requests through Gitee AI and return the resulting image URL in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and generation settings are sent to Gitee AI. <br>
Mitigation: Avoid confidential, regulated, or sensitive content in prompts and settings. <br>
Risk: The Gitee AI API key is required for generation. <br>
Mitigation: Set GITEEAI_API_KEY as an environment variable instead of passing the key on the command line. <br>
Risk: The skill depends on the Python openai package to call the external provider. <br>
Mitigation: Use an isolated Python environment when installing and running the dependency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fchange/moark-image-gen) <br>
- [Gitee AI API endpoint](https://ai.gitee.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with an image link and generation settings summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GITEEAI_API_KEY environment variable or an API key argument; returns the generated image URL without downloading the image by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
