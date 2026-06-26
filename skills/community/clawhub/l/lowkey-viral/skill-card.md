## Description: <br>
Create short-form social media videos and photo carousel slideshows using the Lowkey Viral API for TikTok, Instagram Reels, carousel posts, and other vertical social formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiotdev](https://clawhub.ai/user/tiotdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to generate briefs, images, 2x2 grid videos, and photo slideshow assets through the Lowkey Viral API. It helps agents prepare authenticated API calls, polling steps, and output handling guidance for short-form social content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Lowkey Viral account API key. <br>
Mitigation: Store LOWKEY_VIRAL_API_KEY in the environment, avoid pasting it into prompts or files, and install the skill only when account access is intended. <br>
Risk: Prompts and images are sent to Lowkey Viral for media generation. <br>
Mitigation: Use only content that is appropriate for processing by the service and avoid submitting sensitive or unauthorized media. <br>
Risk: Generation and rendering operations consume account credits and are subject to rate limits. <br>
Mitigation: Monitor credit usage, observe documented rate limits and Retry-After responses, and confirm generation scope before running calls. <br>
Risk: The skill documents a delete action for briefs. <br>
Mitigation: Require explicit confirmation of the target brief ID before issuing any DELETE request. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tiotdev/lowkey-viral) <br>
- [Configured skill homepage](https://github.com/tiotdev/lowkey-viral) <br>
- [Lowkey Viral API key dashboard](https://lowkeyviral.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOWKEY_VIRAL_API_KEY and curl; API calls may upload media, generate assets, render videos or slides, poll progress, list account data, and delete briefs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
