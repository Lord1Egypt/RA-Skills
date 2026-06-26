## Description: <br>
Create and manage AI-generated videos and images using Miraflow, including avatar videos, cinematic clips, image generation, editing, and media uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minforge](https://clawhub.ai/user/minforge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Miraflow avatar videos and AI images, check asynchronous generation status, fetch download links, and upload media for editing or video creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's Miraflow API key to create media and access account resources. <br>
Mitigation: Store the key only in MIRAFLOW_API_KEY, never hardcode it, and install the skill only for accounts intended to use Miraflow. <br>
Risk: Video and image generation can consume account credits and creation endpoints are non-idempotent. <br>
Mitigation: Confirm the requested generation before calling creation endpoints and avoid automatic retries of expensive POST requests. <br>
Risk: Prompts, scripts, and uploaded media are sent to Miraflow and associated storage services. <br>
Mitigation: Avoid submitting secrets, regulated data, or private media unless the user intends that data to be processed by those services. <br>


## Reference(s): <br>
- [Miraflow API Reference](references/api.md) <br>
- [Miraflow API](https://miraflow.ai/api) <br>
- [Miraflow API Keys](https://miraflow.ai/apikeys) <br>
- [Miraflow ClawHub Page](https://clawhub.ai/minforge/miraflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API request examples, status summaries, IDs, links, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce job IDs, status messages, signed download URLs, and local media file paths when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
