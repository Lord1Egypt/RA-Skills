## Description: <br>
Generate images with Nano Banana (Gemini 3 Pro Image) and animate them into videos with Veo 3.1 for websites, landing pages, and marketing materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bermyboystechsolutions](https://clawhub.ai/user/bermyboystechsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and marketing teams use this skill to generate static visual assets and optional short videos from prompts using Gemini and Veo APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gemini API key and sends prompts or images to Google Gemini/Veo services. <br>
Mitigation: Use a limited-scope API key in an isolated environment and review the script before running it. <br>
Risk: The security summary flags under-scoped handling of the Gemini API key, including video download host validation. <br>
Mitigation: Patch or review host validation before forwarding the API key during video download. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated image or MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and Google Gemini/Veo API access; image output is PNG or JPG and optional video output is MP4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
