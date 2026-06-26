## Description: <br>
Automate hospital appointment booking on the 医联 (Yilian) Android app using uiautomator2, covering hospital search, department selection, date/time slot selection, and confirmation without Appium. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlittlebear](https://clawhub.ai/user/openlittlebear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to guide an agent through Android ADB/uiautomator2 workflows for booking doctor appointments in the 医联 (Yilian) app, including navigation, text input, schedule selection, SMS-code handling, and final confirmation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to submit a real medical appointment. <br>
Mitigation: Require manual confirmation of the hospital, department, patient, date/time slot, SMS code, and final '确定预约' action before submission. <br>
Risk: The setup may force-stop the 12306 app to avoid Android accessibility service conflicts. <br>
Mitigation: Use only on a device where stopping 12306 is acceptable, and warn the user before running the force-stop command. <br>
Risk: Android UI state, availability, or clickable containers may differ from the documented flow. <br>
Mitigation: Inspect the current UI hierarchy or screenshot before each action, poll for schedule loading, and stop for user review when expected elements are missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlittlebear/hospital-android-adb) <br>
- [Publisher profile](https://clawhub.ai/user/openlittlebear) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing procedural guidance for controlling an Android device; final appointment submission should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
