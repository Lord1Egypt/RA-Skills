## Description:

Remap a Google TV Streamer remote button without root by filtering its key event and launching another app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uberstone](https://clawhub.ai/user/uberstone)

### License/Terms of Use:

MIT-0

## Use Case:

Google TV Streamer owners and developers use this skill to remap a physical remote app button to launch a chosen app without rooting the device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An enabled accessibility service can intercept hardware key events.

Mitigation: Grant access only after reviewing the service code and confirming that key filtering is needed.

Risk: ADB settings changes can disable other accessibility services.

Mitigation: Record currently enabled services before changes; enable or disable only the remapping component.

Risk: The example APK requests visibility into all installed packages.

Mitigation: Review or rebuild the APK, and remove QUERY_ALL_PACKAGES unless arbitrary app discovery is necessary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/uberstone/skills/google-tv-button-remap)
- [App-button remapping procedure](references/app-button-remap.md)
- [Building an APK without Gradle](references/build-apk-without-gradle.md)
- [Button-remapping engineering notes](docs/rcu-app-button-remap-engineering.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands and Java/XML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Device-specific keycodes and target app packages require confirmation; verify with a physical button press.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
