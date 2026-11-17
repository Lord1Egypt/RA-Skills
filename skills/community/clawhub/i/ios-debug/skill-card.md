## Description:

Provides iOS developers with workflows for debugging apps on an iPhone 14, including stdout log capture, QuickTime-based screenshots, app build/install/launch commands, and device status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sougannkyou](https://clawhub.ai/user/sougannkyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when debugging iOS apps on an authorized physical iPhone 14, collecting stdout logs, capturing the mirrored device screen, and managing build, install, launch, uninstall, and device status workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot workflow can capture private information from a connected iPhone screen.

Mitigation: Use it only on an authorized test device, switch to a safe screen before capture, and delete captured image files when finished.

Risk: Log capture can expose sensitive app or device data.

Mitigation: Collect logs only from authorized apps and devices, and review output before sharing or storing it.

Risk: Install, reinstall, and uninstall commands can alter app state or remove app data.

Mitigation: Require explicit confirmation before uninstalling or reinstalling apps and back up data that must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sougannkyou/skills/ios-debug)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are procedural debugging guidance and commands intended for review before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
