## Description:

Control Xiaomi Mi Home smart devices through the Xiaomi Cloud API, including device status checks, property changes, automation scenes, fish-feeder automation, and XiaoAI speaker text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonzhang2015](https://clawhub.ai/user/jasonzhang2015)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Xiaomi Mi Home devices, inspect device state, create Mi Home automation scenes, and run a lock-event-based fish-feeding workflow for devices they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Xiaomi account credentials and service tokens for a smart-home account.

Mitigation: Use only an account and devices you control, avoid command-line passwords, protect credential files, and rotate any password previously entered through command-line arguments.

Risk: The release includes household-specific home and device identifiers and can create or use local cache and state files.

Mitigation: Replace bundled identifiers with your own configuration before use, and protect or remove local device cache and fish-feeding state files when they are no longer needed.

Risk: The fish-feeding workflow polls door-lock events and can infer occupancy-related behavior.

Mitigation: Enable the cron workflow only when this automation is explicitly desired, test with dry-run or status commands first, and disable it if occupancy-derived automation is not acceptable.

Risk: The skill can operate real smart-home devices through cloud API commands.

Mitigation: Review generated shell commands and scene JSON before execution, and limit use to non-safety-critical devices unless the behavior has been independently verified.

## Reference(s):

- [Mijia Control on ClawHub](https://clawhub.ai/jasonzhang2015/skills/mijia-control)
- [Publisher Profile](https://clawhub.ai/user/jasonzhang2015)
- [Device Registry](references/devices.json)
- [Scene Template](references/scene_template.json)
- [Xiaomi Account Login](https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true)
- [MIoT Spec Reference](https://home.miot-spec.com/spec/<model>)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local credential, device cache, scene JSON, and fish-feeding state files when the provided commands are run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
