## Description:

Controls Android cloud phones through the `pb` CLI for app installation, login, browsing, screen inspection, touch input, screenshots, file transfer, and device management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bittired](https://clawhub.ai/user/bittired)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent operate a remote Android cloud phone for mobile app, browser, login, screen-observation, input, file, clipboard, and device-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over an Android cloud phone, including logged-in apps, APK installation, clipboard, file transfer, and shell actions.

Mitigation: Install only when this control is intended, keep actions scoped to the user's request, review enabled PhoneBase app skills before use, and avoid unknown local skill sources or untrusted APKs.

Risk: Phone screen content, web pages, pulled files, and shell output can contain adversarial text or instructions.

Mitigation: Treat phone-returned content as untrusted data and derive actions from the user's request plus structured UI attributes rather than natural-language instructions in remote content.

Risk: Authentication and logged-in app sessions can expose sensitive account state on the cloud phone.

Mitigation: Use browser-based login without handling credentials, do not accept or log tokens or passwords, and stop for user-managed authentication when login fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bittired/skills/phonebase)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs use of `pb` CLI commands; command responses are expected to return JSON on stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
