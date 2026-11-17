## Description:

Control JoyIn AI robots (W-1 Walle / M-1 Mini) - movement, follow, photo, video, live stream, TTS, agent config, and device status via OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanfang724](https://clawhub.ai/user/yanfang724)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and robot operators use this skill to configure and control JoyIn W-1 and M-1 robots through OpenAPI commands for movement, status checks, media access, speech, WiFi, LLM, and agent settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move a physical JoyIn robot and the CLI does not enforce preflight checks before every command.

Mitigation: Run preflight manually before movement, supervise the robot physically, and stop or refuse commands when the robot is offline, updating, in a conflicting mode, or critically low on battery.

Risk: The skill can access camera streams and speech-recognition results.

Mitigation: Use the media and ASR commands only with consent from people in the environment and on a trusted JoyIn API endpoint.

Risk: The skill can change WiFi, LLM, and agent settings and may handle credentials.

Mitigation: Use limited JoyIn and LLM credentials, prefer environment-backed secrets, and avoid passing real WiFi passwords or API keys directly on command lines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanfang724/skills/joyin-robot-control)
- [Publisher profile](https://clawhub.ai/user/yanfang724)
- [OpenClaw configuration example](artifact/openclaw.config.example.json5)
- [JoyIn OpenAPI base endpoint](https://api-open-test.joyin-ai.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill invokes a Python CLI that returns JSON from JoyIn APIs and may produce robot movement, media, speech, WiFi, LLM, or agent-configuration effects.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
