## Description: <br>
Uses MiniMax vision capabilities to analyze screenshots and images for CAPTCHA content, slider positions, visible text, and web page elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-nurmamat](https://clawhub.ai/user/ai-nurmamat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to capture screenshots, send images to a MiniMax vision tool, and interpret returned visual analysis for authorized image, screenshot, text, and slider-position workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help analyze CAPTCHA or anti-bot verification challenges. <br>
Mitigation: Use it only for legitimate, authorized analysis of screenshots or images you own or are permitted to process. <br>
Risk: Screenshots may contain secrets, credentials, or personal data before being sent to a vision model. <br>
Mitigation: Review and redact sensitive image content before invoking the MiniMax vision tool. <br>
Risk: The helper script constructs a shell command from user-provided prompt and image values. <br>
Mitigation: Avoid running the helper on untrusted input unless it is changed to call the command with safe argument arrays. <br>


## Reference(s): <br>
- [MiniMax Vision Captcha on ClawHub](https://clawhub.ai/ai-nurmamat/minimax-vision-captcha) <br>
- [Publisher profile: ai-nurmamat](https://clawhub.ai/user/ai-nurmamat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text visual analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MiniMax vision through mcporter and may read a local screenshot path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and marketplace.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
