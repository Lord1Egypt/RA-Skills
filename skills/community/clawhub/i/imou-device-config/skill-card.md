## Description:

Manages Imou device channel security configuration for motion detection schedules, motion detection sensitivity, privacy mode, and IoT thing-model property or service operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imou-openplatform](https://clawhub.ai/user/imou-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Imou cameras through the Imou Open API, including PaaS channel settings and IoT thing-model properties or services. It is intended for users with an Imou developer account and device authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly change Imou device settings, including privacy mode, motion detection plans, sensitivity, IoT properties, and service commands.

Mitigation: Review each proposed command before execution, resolve thing-model refs from the product model, and use a dedicated least-privilege Imou developer app when possible.

Risk: Credential-bearing requests are sent to the user-configured IMOU_BASE_URL, which evidence says is not validated.

Mitigation: Set IMOU_BASE_URL only to documented HTTPS Imou endpoints and keep IMOU_APP_SECRET out of shared shells, logs, and transcripts.

Risk: The release depends on an unpinned requests package.

Mitigation: Pin dependencies in a controlled environment before using the skill with real cameras.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imou-openplatform/skills/imou-device-config)
- [Imou Open API Reference - Device Config](artifact/references/imou-config-api.md)
- [Imou Open developer portal](https://open.imou.com)
- [Imou overseas developer portal](https://open.imoulife.com)
- [Imou development specification](https://open.imoulife.com/book/http/develop.html)
- [Get accessToken API](https://open.imou.com/document/pages/fef620/)
- [Get product thing model API](https://open.imou.com/document/pages/2a238c/)
- [IoT service API](https://open.imou.com/document/pages/fa0726/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and optional text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMOU_APP_ID, IMOU_APP_SECRET, IMOU_BASE_URL, and the requests Python package.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
