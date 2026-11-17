## Description:

Omniscient helps an agent plan and execute cognitive tasks, code or shell workflows, and broad Windows system-control actions across desktop, hardware, network, peripheral, camera, audio, Bluetooth, serial, and smart-home interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask an agent to reason through tasks, generate and run code or shell commands, and operate supported Windows device-control scripts. It is most appropriate when the user intentionally wants local automation over windows, processes, hardware settings, network configuration, peripherals, capture devices, and smart-home endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue broad local Windows automation and device-control actions, including process termination, network changes, power actions, GUI interaction, and peripheral control.

Mitigation: Install only where this level of local control is intended, review commands before execution, and require explicit consent for destructive or state-changing operations.

Risk: Camera capture, microphone recording, screenshots, Wi-Fi profile details, and smart-home control may expose sensitive data or affect the user's physical environment.

Mitigation: Use only with trusted prompts, avoid untrusted webpages or prompt sources, protect HA_TOKEN, and confirm the target device, account, and Home Assistant URL before use.

Risk: The authoritative security evidence rates the release suspicious because its scope is broad and safety controls are inconsistent for routine installation.

Mitigation: Treat the skill as high-trust local automation, limit installation to reviewed environments, and perform security review against the bundled checklist before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/omniscient)
- [System Control Command Reference](artifact/references/command_reference.md)
- [Security Review Checklist](artifact/references/security_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with inline commands and generated code where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or invoke local scripts that return JSON, status text, files, screenshots, photos, or audio recordings depending on the requested operation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
