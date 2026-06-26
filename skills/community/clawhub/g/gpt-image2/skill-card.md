## Description: <br>
Generate high-quality images with GPT Image 2 (OpenAI gpt-image-2) through the ClawdChat tool gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxyd-ai](https://clawhub.ai/user/lxyd-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit GPT Image 2 image-generation jobs, poll for completed image URLs, and create images from prompts or reference-image URLs with explicit cost confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image-generation submissions send prompts and reference-image URLs to the ClawdChat gateway and use a ClawdChat credential. <br>
Mitigation: Install only if the user trusts ClawdChat and the uno-cli dependency, and avoid private or identifying prompt content unless the user accepts ClawdChat's data handling. <br>
Risk: Each image-generation submission deducts 300 ClawdChat credits from the logged-in account. <br>
Mitigation: Confirm the prompt, reference image URLs, image count, size, style, and submit cost before each paid generation or pre-authorized batch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxyd-ai/gpt-image2) <br>
- [ClawdChat](https://clawdchat.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces job IDs, polling guidance, generated image URLs, and surfaced error messages; image files are not written locally by the skill.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
