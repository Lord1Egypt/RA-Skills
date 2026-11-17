## Description:

Controls real Android phones through the Mobilerun API, including screenshots, UI-tree inspection, tapping, swiping, typing, app management, and AI-agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnmalek312](https://clawhub.ai/user/johnmalek312)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent remotely operate an Android device through Mobilerun for app interaction, mobile workflow automation, troubleshooting, and AI-agent phone tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent see and control an Android device, including sensitive screen content.

Mitigation: Use it only with devices and accounts the user is comfortable exposing to Mobilerun, and avoid banking, password, health, and private-message screens.

Risk: Setup may involve a sideloaded APK with Android Accessibility access.

Mitigation: Prefer a verified APK source with a known signature or checksum, and revoke Accessibility permission when the session is no longer needed.

Risk: API keys can grant programmatic access to connected devices.

Mitigation: Never print, log, or share MOBILERUN_API_KEY, and revoke or rotate the key after exposure or when access is no longer needed.

Risk: The skill can support actions that may spend credits, uninstall apps, submit feedback, create AI-agent tasks, or configure webhooks.

Mitigation: Confirm app uninstall, cloud-device spending, AI-agent task, webhook, and feedback submission actions with the user before executing them.

## Reference(s):

- [Mobilerun ClawHub Skill](https://clawhub.ai/johnmalek312/skills/mobile-run)
- [Phone Control API Reference](artifact/phone-api.md)
- [Mobilerun Platform API](artifact/api.md)
- [Mobilerun Setup](artifact/setup.md)
- [Mobilerun Plans and Subscriptions](artifact/subscription.md)
- [Mobilerun API](https://api.mobilerun.ai/v1)
- [Droidrun Portal](https://droidrun.ai/portal)
- [Droidrun Portal GitHub Repository](https://github.com/droidrun/droidrun-portal)
- [Mobilerun API Keys](https://cloud.mobilerun.ai/api-keys)
- [Mobilerun Billing](https://cloud.mobilerun.ai/billing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOBILERUN_API_KEY and a connected Mobilerun device; screenshots and UI trees may contain sensitive personal data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
