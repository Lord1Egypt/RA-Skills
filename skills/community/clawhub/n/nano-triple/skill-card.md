## Description: <br>
Generates three parallel Nano Banana Pro image options from one prompt, then lets the user pick a winner or refine another set. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and creative operators use this skill to generate three candidate images from a single image prompt and quickly select or refine an option. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill passes raw user prompt text to shell commands, which can be unsafe if an agent interpolates the prompt into a shell string. <br>
Mitigation: Pass prompt text as a safely quoted argument or argv value, and avoid shell interpolation when calling the image helper. <br>
Risk: The skill depends on an external Nano Banana Pro helper and Gemini credentials for generation. <br>
Mitigation: Install only trusted helper code, configure GEMINI_API_KEY or OpenClaw credentials intentionally, and avoid putting secrets or sensitive data in prompts. <br>
Risk: Each prompt or refinement triggers three image generations. <br>
Mitigation: Set user expectations for cost and latency before repeated refinement cycles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvanhorn/nano-triple) <br>
- [Google AI Studio](https://aistudio.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Markdown] <br>
**Output Format:** [Markdown with shell commands and three labeled generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates three 1K image options per prompt or refinement.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
