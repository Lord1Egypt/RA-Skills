## Description:

Give an OpenClaw agent control of a real Android phone through the official Mobilerun API, including screenshots, UI tree inspection, taps, swipes, typing, and app management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pelae1](https://clawhub.ai/user/pelae1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate Android apps on a connected personal or cloud device through Mobilerun. It supports mobile testing, app workflows, data collection, and task execution that require observing and interacting with a phone screen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-mediated Android automation can expose sensitive screens, credentials, MFA prompts, or confidential app content.

Mitigation: Prefer a test phone or non-sensitive cloud device, and avoid banking, password, MFA, and confidential workflows.

Risk: The workflow depends on a sideloaded Portal app and Android Accessibility permission for screen reading and control.

Mitigation: Verify the APK source before sideloading, grant Accessibility permission only when needed, and revoke the permission or uninstall the Portal app when finished.

Risk: Misplaced API keys could allow unwanted access to the user's Mobilerun account and connected devices.

Mitigation: Use the MOBILERUN_API_KEY environment variable, do not paste API keys into chat, and revoke expired or exposed keys from the Mobilerun dashboard.

## Reference(s):

- [Mobilerun Skill Page](https://clawhub.ai/pelae1/skills/mobilerun-official)
- [Mobilerun API](https://api.mobilerun.ai/v1)
- [Mobilerun API Keys](https://cloud.mobilerun.ai/api-keys)
- [Droidrun Portal APK](https://droidrun.ai/portal)
- [Mobilerun Billing](https://cloud.mobilerun.ai/billing)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Markdown guidance with HTTP endpoints and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MOBILERUN_API_KEY for authenticated Mobilerun requests.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
