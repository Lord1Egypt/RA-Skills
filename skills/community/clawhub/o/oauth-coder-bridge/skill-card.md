## Description: <br>
Routes OpenClaw Anthropic API calls through oauth-coder (Claude CLI with OAuth), no API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and run a local bridge that converts OpenClaw Anthropic Messages requests into oauth-coder calls backed by an authenticated Claude CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge routes requests through a locally authenticated Claude CLI session. <br>
Mitigation: Install only when oauth-coder and the local Claude CLI session are trusted, and keep the bridge bound to 127.0.0.1. <br>
Risk: Setup modifies the local OpenClaw configuration. <br>
Mitigation: Review the ~/.openclaw/openclaw.json provider change before using the bridge. <br>
Risk: Prompts or responses may be logged locally when file logging is enabled. <br>
Mitigation: Avoid sensitive logging and leave OAUTH_CODER_BRIDGE_LOG_FILE unset unless local logs are intentionally needed. <br>
Risk: Autostart can keep the OAuth-backed local bridge running across sessions. <br>
Mitigation: Enable the systemd user service only when persistent bridge availability is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/oauth-coder-bridge) <br>
- [Project homepage](https://github.com/earlvanze/oauth-coder-bridge) <br>
- [Upstream oauth-cli-coder project](https://github.com/codeninja/oauth-cli-coder) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Shell commands, Configuration] <br>
**Output Format:** [Anthropic-compatible JSON responses and Markdown setup guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local HTTP bridge output may include text and tool-use content blocks from the Claude CLI session.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
