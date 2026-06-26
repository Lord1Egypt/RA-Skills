## Description: <br>
Generate a video task based on user-provided text and images (supports image URLs and local file paths), and submit it to a remote video service using an API Key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leizhang-magiclight](https://clawhub.ai/user/leizhang-magiclight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a text prompt and source image to MagicLight, then receive the generated task ID and final video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and local image contents are sent to MagicLight for video generation. <br>
Mitigation: Use only inputs appropriate for that service, and avoid sensitive prompts, private or internal URLs, and confidential local images. <br>
Risk: The required MAGIC_API_KEY authorizes service calls that may consume quota or credits. <br>
Mitigation: Use a scoped or dedicated key where possible and confirm intended usage before submitting generation tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leizhang-magiclight/magic-image-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON] <br>
**Output Format:** [Plain text or Markdown status messages with JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a task ID during creation and a video URL after polling; requires MAGIC_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
