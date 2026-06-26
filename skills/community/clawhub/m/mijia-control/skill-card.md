## Description: <br>
Control Xiaomi Mi Home smart devices through Xiaomi Cloud APIs for device status checks, property changes, batch commands, automation scenes, speaker TTS, and fish-feeder automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonZhang2015](https://clawhub.ai/user/JasonZhang2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and control Xiaomi Mi Home devices, create Mi Home automation scenes, and run supported helper scripts for household workflows. It is intended for environments where the user has authorized Xiaomi Cloud credentials and understands the connected physical devices. <br>

### Deployment Geography for Use: <br>
Global, subject to Xiaomi Cloud regional account and device support. <br>

## Known Risks and Mitigations: <br>
Risk: Xiaomi Cloud credentials can grant broad control over smart-home devices. <br>
Mitigation: Use the skill only in trusted environments, keep the credential file restricted, avoid plaintext storage where possible, and rotate Xiaomi credentials if they are exposed. <br>
Risk: Lock-event polling can reveal occupancy patterns and trigger physical feeder automation. <br>
Mitigation: Confirm the exact devices and automations before use, test with dry-run or status commands, and disable cron or lock-event feeder automation unless it is explicitly wanted. <br>
Risk: Device commands and scenes can change the state of lights, heaters, speakers, feeders, and other connected hardware. <br>
Mitigation: Review device identifiers, scene JSON, and command values before execution, and start with targeted manual commands until behavior is verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JasonZhang2015/mijia-control) <br>
- [MIoT Spec Reference](https://home.miot-spec.com/spec/) <br>
- [Device Registry](references/devices.json) <br>
- [Automation Scene Template](references/scene_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct execution of scripts that use Xiaomi Cloud credentials and can affect physical smart-home devices.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
