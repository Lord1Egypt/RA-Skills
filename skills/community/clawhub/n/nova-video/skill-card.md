## Description: <br>
Generate images or videos using the Nova Video OpenAPI with a single sentence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onesoloapp](https://clawhub.ai/user/onesoloapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate images, create videos from text or image references, check generation status, and list prior generations through the Nova Video API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image references, and generated media are sent to an external generation service. <br>
Mitigation: Install only if the user trusts Nova Video with submitted content, and avoid private or signed image URLs unless sharing them is intended. <br>
Risk: The skill requires a Nova Video API key. <br>
Mitigation: Use a revocable API key and keep it in the NOVA_API_KEY environment variable rather than embedding it in prompts or shared files. <br>
Risk: Generated video links may be saved locally in video_url.txt. <br>
Mitigation: Delete video_url.txt when the link is no longer needed. <br>


## Reference(s): <br>
- [NovaVideo ClawHub listing](https://clawhub.ai/onesoloapp/nova-video) <br>
- [Nova Video hosted skill instructions](https://nova-video.onesolo.app/SKILL.md) <br>
- [Nova Video API service](https://nova-video.onesolo.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated video URLs to video_url.txt to preserve long signed URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
