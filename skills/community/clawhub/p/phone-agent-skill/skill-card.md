## Description:

Phone agent uses the AutoGLM Phone Agent SDK to help an agent control Android devices with natural language for app testing, UI interaction, data collection, screenshots, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaojizhou](https://clawhub.ai/user/gaojizhou)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and automation teams use this skill to operate Android devices or emulators through natural language instructions for app testing, UI journeys, data collection, and reproducing mobile workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real actions on an Android device or emulator, including taps, typing, app launches, and screenshots.

Mitigation: Use test devices and test accounts when possible, and request confirmation screenshots before risky or irreversible changes.

Risk: Phone automation can interact with apps that expose personal, financial, or public-posting access.

Mitigation: Avoid sensitive apps unless the task is intentional and authorized; review on-screen state before submitting forms, purchases, posts, or account changes.

Risk: Mobile workflows may vary by region, app version, network state, or hardware prompts such as biometric authentication.

Mitigation: Provide explicit fallbacks, verify device connectivity and permissions, and avoid tasks that require bypassing hardware authentication prompts.

## Reference(s):

- [Open-AutoGLM upstream documentation](https://github.com/zai-org/Open-AutoGLM)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include action logs, screenshots, structured observations, and backend error text when the Phone Agent SDK returns them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
