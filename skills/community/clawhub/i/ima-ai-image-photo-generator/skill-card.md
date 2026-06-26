## Description: <br>
AI image generator and photo generator with SeeDream 4.5, Midjourney, Nano Banana 2, and Nano Banana Pro for posters, thumbnails, logos, art, illustrations, product photos, and social media graphics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dai-shuo](https://clawhub.ai/user/dai-shuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit visual assets from prompts or input images through IMA Studio models, including marketing graphics, thumbnails, product imagery, logos, and illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and the IMA API key are sent to IMA services for generation and upload workflows. <br>
Mitigation: Use the skill only with an IMA account and key you are comfortable using; start with a low-quota or test key and avoid sensitive images unless uploading them to IMA services is acceptable. <br>
Risk: Image-to-image tasks can upload local images to IMA media-upload services, and generation consumes IMA credits. <br>
Mitigation: Confirm inputs and expected credit use before running generation, especially for premium models or user-provided local images. <br>
Risk: The skill keeps small local preference and log files under ~/.openclaw. <br>
Mitigation: Clear ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ when local traces should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dai-shuo/ima-ai-image-photo-generator) <br>
- [IMA Studio](https://imastudio.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated image URLs or media delivery instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY and may spend IMA credits when generation requests are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
