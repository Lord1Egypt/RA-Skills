## Description: <br>
Mac Control helps an agent automate macOS UI interactions with screenshots, coordinate handling, cliclick mouse and keyboard actions, and AppleScript window inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill for supervised macOS desktop automation, including locating UI elements, clicking, typing, capturing screenshots, and checking display or window bounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over macOS screenshots, mouse clicks, and keyboard input. <br>
Mitigation: Use only in supervised sessions where the operator intends desktop control, and review the skill before installation. <br>
Risk: Screenshots may expose sensitive windows or private content. <br>
Mitigation: Close or obscure sensitive windows before capture and delete temporary screenshots after use. <br>
Risk: Incorrect coordinates or protected pages can cause unintended clicks or actions. <br>
Mitigation: Verify coordinates before clicking and avoid login, OAuth, financial, and administrative flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EasonC13/mac-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts for screenshots, coordinate calibration, image cropping, element location, clicks, and window/display information.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
