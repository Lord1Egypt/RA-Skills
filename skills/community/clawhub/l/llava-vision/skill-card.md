## Description: <br>
Call a local llama.cpp server with the LLaVA model to analyze images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[447992399](https://clawhub.ai/user/447992399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit a local image path or remote image URL to a local LLaVA llama.cpp server and receive a text description of the image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local image paths and prompts are sent to the local server, and remote image URLs are fetched before analysis. <br>
Mitigation: Use the skill only with trusted local llama.cpp/LLaVA servers and review image paths, URLs, and prompts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/447992399/llava-vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns image-analysis text or structured error details from the local server call.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
