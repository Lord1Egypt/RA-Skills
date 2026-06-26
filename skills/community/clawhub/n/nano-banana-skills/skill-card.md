## Description: <br>
Generate or refine images from text prompts and optional input images using Google Gemini models through the Wisdom Gate API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0n1onr1ng](https://clawhub.ai/user/0n1onr1ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate, edit, combine, and iteratively refine images from natural-language prompts and selected image inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and conversation history are sent to Wisdom Gate/Gemini. <br>
Mitigation: Use only approved content, avoid confidential or regulated images unless authorized, and review data handling requirements before use. <br>
Risk: API credentials are required for Wisdom Gate access. <br>
Mitigation: Use a dedicated, revocable API key and rotate or revoke it if it is exposed. <br>
Risk: The skill writes generated images and optional conversation history to local paths. <br>
Mitigation: Choose output and history paths intentionally and keep them limited to files intended for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0n1onr1ng/nano-banana-skills) <br>
- [Wisdom Gate](https://wisgate.ai) <br>
- [Wisdom Gate Gemini generateContent endpoint](https://api.wisgate.ai/v1beta/models/{model}:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local image or JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated image files and optional conversation history JSON; sends prompts, selected images, and refinement history to Wisdom Gate/Gemini.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
