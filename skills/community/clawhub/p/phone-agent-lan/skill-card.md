## Description: <br>
Controls a USB-connected Android phone through ADB by capturing screens and UI XML, finding interface elements, and performing taps, swipes, text entry, key presses, and app launch or stop actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan314](https://clawhub.ai/user/lanlan314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and control an Android phone during app workflows, including opening apps, finding UI elements, entering text, navigating screens, and sending simple messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad device-changing actions on a USB-connected Android phone through ADB. <br>
Mitigation: Install only when intentional phone control is needed, prefer a test or secondary device, and review each action before execution. <br>
Risk: Automated interaction could affect messages, purchases, payments, deletions, public posts, or account settings. <br>
Mitigation: Manually confirm any high-impact action before it is sent, submitted, deleted, purchased, paid, posted, or used to change an account. <br>
Risk: Screenshots and UI dumps may expose sensitive content from open apps. <br>
Mitigation: Keep sensitive apps closed while using the skill and turn off USB debugging after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanlan314/phone-agent-lan) <br>
- [Publisher profile](https://clawhub.ai/user/lanlan314) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Guidance] <br>
**Output Format:** [CLI text output, temporary PNG screenshots, XML UI dumps, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires adb, USB debugging authorization, and a connected Android device; text input is limited to ASCII-style ADB input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
