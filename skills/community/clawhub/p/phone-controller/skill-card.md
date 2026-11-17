## Description:

AI phone controller via ADB and GLM that controls Android devices with natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure ADB, ADB Keyboard, Open-AutoGLM, and a GLM API key so an agent can inspect Android screens and carry out natural-language phone-control tasks with confirmation for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADB-level control and ADB Keyboard can operate the connected Android device and enter sensitive input.

Mitigation: Use a dedicated test phone without sensitive accounts, avoid banking, payment, password, and private chat screens, and require explicit user confirmation before write, send, order, payment, settings, or deletion actions.

Risk: Screen contents are sent to the external GLM API for understanding.

Mitigation: Do not use the skill on login pages, payment pages, bank apps, password entry screens, or private conversations; hand off sensitive screens to manual control.

Risk: The setup depends on third-party components, including Open-AutoGLM and ADBKeyboard.apk.

Mitigation: Pin and review the Open-AutoGLM revision before installation and verify any APK by hash and signing certificate before enabling it.

Risk: API keys and device debugging state can remain exposed after use.

Mitigation: Avoid passing API keys directly on the command line, then revoke USB debugging authorization, disable USB debugging, switch back from ADB Keyboard, and uninstall ADB Keyboard when it is no longer needed.

## Reference(s):

- [Phone Controller skill page](https://clawhub.ai/moroiser/skills/phone-controller)
- [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM)
- [ADB Keyboard](https://github.com/senzhk/ADBKeyBoard)
- [BigModel Open Platform](https://open.bigmodel.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and Android action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Android device, USB debugging, ADB Keyboard, Open-AutoGLM, and a GLM API key.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
