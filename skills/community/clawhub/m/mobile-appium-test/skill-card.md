## Description:

Android UI automation testing using Appium with USB-connected real devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[never112](https://clawhub.ai/user/never112)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to plan and run Appium-based Android UI tests on USB-connected physical devices, including connection checks, app installation, UI inspection, test execution, screenshots, and log collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appium relaxed-security mode can allow broader device and host-side automation than a normal local test server needs.

Mitigation: Start Appium on 127.0.0.1 without `--relaxed-security` by default, enable only specific insecure features when required, and stop the server after testing.

Risk: ADB and Appium can control a USB-authorized Android device and access test logs, screenshots, and app behavior.

Mitigation: Use trusted devices and apps, keep port 4723 local, review commands before execution, and avoid running global npm installation steps with administrator privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/never112/skills/mobile-appium-test)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADB, Appium Server, a USB-authorized Android device, and user-provided app/test capabilities.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
