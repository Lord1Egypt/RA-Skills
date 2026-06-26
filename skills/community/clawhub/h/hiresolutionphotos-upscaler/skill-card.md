## Description: <br>
AI Image Upscaling submits PNG, JPG, or WebP images to HiResolutionPhotos and returns a private retrieval page for 4K or 8K upscaled results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setdemos](https://clawhub.ai/user/setdemos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upscale a user's local or web image through the HiResolutionPhotos service, then return a download page link instead of downloading the large output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected image is sent to hiresolutionphotos.com and the result is hosted externally. <br>
Mitigation: Avoid uploading sensitive images unless the user accepts the service's privacy and retention practices. <br>
Risk: Upscaled outputs can be large and direct download attempts may be unreliable for agents. <br>
Mitigation: Return the provided retrieval page link to the user instead of downloading the raw generated image. <br>
Risk: The service limits submissions to 15 upscale requests per hour per IP. <br>
Mitigation: Keep requests within the documented rate limit and surface 429 responses to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/setdemos/hiresolutionphotos-upscaler) <br>
- [HiResolutionPhotos homepage](https://hiresolutionphotos.com) <br>
- [HiResolutionPhotos upscale API](https://hiresolutionphotos.com/api/upscale) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with curl commands and a result URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a retrieval webpage link; agents should not download the large generated image directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
