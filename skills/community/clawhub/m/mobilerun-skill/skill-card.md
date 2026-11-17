## Description:

Control real Android phones through the Mobilerun API for tapping, swiping, typing, screenshots, UI-tree reading, app management, and autonomous Droidrun Agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariozada](https://clawhub.ai/user/mariozada)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to remotely control a connected Android device, automate app workflows, inspect screenshots and accessibility trees, provision cloud devices, or delegate multi-step phone tasks to the Droidrun Agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Android control can expose sensitive screenshots, UI text, account data, and app state.

Mitigation: Use a non-primary device or test profile when possible, avoid sharing screenshots or UI trees beyond the user, and keep MOBILERUN_API_KEY out of chat and logs.

Risk: The required sideloaded Portal APK and Accessibility service grant broad visibility and control over the device.

Mitigation: Verify the APK source as much as possible, enable Accessibility only when needed, and disable the service after use.

Risk: Autonomous tasks, app management, cloud-device termination, field clearing, feedback submission, or plan-consuming operations may affect accounts or spend credits.

Mitigation: Require explicit user confirmation before destructive, account-affecting, billing-related, or autonomous actions.

## Reference(s):

- [Mobilerun Skill Page](https://clawhub.ai/mariozada/skills/mobilerun-skill)
- [Publisher Profile](https://clawhub.ai/user/mariozada)
- [Mobilerun API Base](https://api.mobilerun.ai/v1)
- [Mobilerun API Keys](https://cloud.mobilerun.ai/api-keys)
- [Mobilerun Billing](https://cloud.mobilerun.ai/billing)
- [Droidrun Portal](https://droidrun.ai/portal)
- [Droidrun Portal Source](https://github.com/droidrun/droidrun-portal)
- [Phone Control API Reference](artifact/phone-api.md)
- [Mobilerun Platform API](artifact/api.md)
- [Mobilerun Setup](artifact/setup.md)
- [Mobilerun Plans and Subscriptions](artifact/subscription.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration guidance, Markdown, Text]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MOBILERUN_API_KEY and may return screenshots, UI accessibility data, task status, and device-control results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
