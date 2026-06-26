## Description: <br>
Multi-layer blocklist guard for OpenClaw that hard-blocks tool calls matching banned patterns, injects a security directive at agent bootstrap, warns on incoming messages, and broadcasts Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rgr4y](https://clawhub.ai/user/rgr4y) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to enforce a configurable blocklist across bootstrap context, incoming messages, and tool-call execution. It is intended for environments that deliberately want persistent policy enforcement and Telegram incident alerts for blocked terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently controls agent behavior by injecting bootstrap policy, warning on messages, and blocking matching tool calls. <br>
Mitigation: Install only when persistent blocklist enforcement is desired, review the default blocked terms before enabling, and document how to remove the hooks and reverse file lock-down. <br>
Risk: Incident metadata is sent to Telegram by default when a block fires. <br>
Mitigation: Decide whether Telegram alerts are acceptable, set alertTelegram to false if external reporting is not wanted, and restrict Telegram allowFrom recipients to trusted administrators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rgr4y/openclaw-snitch) <br>
- [Publisher profile](https://clawhub.ai/user/rgr4y) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](README.md) <br>
- [Plugin manifest](openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw policy directives, warning messages, block responses, logs, and optional Telegram alert text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
