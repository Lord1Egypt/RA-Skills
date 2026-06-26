## Description: <br>
Use AI AutoGLM Phone Agent for automated mobile device control. Suitable for tasks requiring mobile phone automation, such as APP automated testing, data collection, UI interaction, etc. Supports controlling the mobile interface through natural language instructions to implement operations such as clicking, sliding, inputting, and screenshotting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaojizhou](https://clawhub.ai/user/gaojizhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate Android device interactions for app testing, UI workflows, data collection, and reproducing user journeys. It can drive taps, swipes, text entry, app launches, screenshots, and UI observation through the AutoGLM Phone Agent SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control of an Android device and read screen contents. <br>
Mitigation: Use an emulator or dedicated test phone with test accounts, keep the Phone Agent service local and trusted, and revoke accessibility or overlay permissions when finished. <br>
Risk: Automated UI actions may affect purchases, posts, deletions, account settings, privacy settings, or security settings. <br>
Mitigation: Require explicit confirmation before high-impact actions and ask for confirmation screenshots when changes are risky. <br>
Risk: Phone automation may be unreliable when app versions, regions, network conditions, or device calibration differ. <br>
Mitigation: Provide explicit fallbacks, verify screenshots or observations, and recalibrate device resolution or restart the accessibility service when taps land incorrectly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaojizhou/phone-agent-skill) <br>
- [AutoGLM Phone Agent SDK](https://github.com/zai-org/Open-AutoGLM) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and SDK-returned action logs, screenshots, structured observations, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on device state, installed apps, network availability, and the configured Phone Agent endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
