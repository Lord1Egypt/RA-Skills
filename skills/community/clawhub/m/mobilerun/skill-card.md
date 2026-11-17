## Description:

Mobilerun helps an agent control, automate, observe, and run tasks on Android phones or Mobilerun cloud devices through authenticated API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnmalek312](https://clawhub.ai/user/johnmalek312)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation users can use this skill to interact with Android devices, inspect screenshots and UI state, manage apps, run mobile workflows, and submit Mobilerun AI agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give Mobilerun remote control visibility into an Android device, including screenshots and UI state that may contain sensitive personal data.

Mitigation: Prefer a test or cloud device for evaluation, avoid sensitive apps unless necessary, and keep screenshot or UI data limited to the current user task.

Risk: The Android Portal app requires Accessibility Service permission, which enables screen reading and simulated taps, swipes, and text input.

Mitigation: Grant the permission only on devices intended for this automation and revoke Accessibility permission when the task or evaluation is complete.

Risk: The Portal APK is sideloaded outside the Play Store.

Mitigation: Verify the Portal APK source independently before installation.

Risk: Shell, destructive device actions, and automatic feedback payloads may have consequences beyond simple observation.

Mitigation: Review destructive actions and feedback content before allowing them, and use values returned by trusted API responses when constructing commands.

## Reference(s):

- [Mobilerun ClawHub Skill](https://clawhub.ai/johnmalek312/skills/mobilerun)
- [Mobilerun OpenAPI Schema](https://api.mobilerun.ai/v1/openapi.json)
- [Mobilerun Quickstart](https://docs.mobilerun.ai/quickstart)
- [Mobilerun Dashboard](https://cloud.mobilerun.ai)
- [Droidrun Portal App](https://github.com/droidrun/droidrun-portal)
- [Droidrun Framework](https://github.com/droidrun/droidrun)
- [Setup & Billing](references/setup-and-billing.md)
- [Security & Privacy](references/security.md)
- [Troubleshooting](references/troubleshooting.md)
- [Use Cases](references/use-cases.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOBILERUN_API_KEY plus curl and jq; may produce PNG screenshots when requested by the user's task.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
