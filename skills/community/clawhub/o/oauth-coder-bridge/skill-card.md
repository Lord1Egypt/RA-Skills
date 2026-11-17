## Description:

Routes OpenClaw Anthropic API calls through oauth-coder (Claude CLI with OAuth), no API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw to send Anthropic Messages API requests to a local oauth-coder bridge backed by the Claude CLI and OAuth tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an OAuth-backed Claude bridge with weak access controls.

Mitigation: Run it only for an intended local Claude OAuth bridge, keep it bound to 127.0.0.1, and do not expose port 8787 through proxies or container port mappings.

Risk: Setup makes persistent local OpenClaw configuration changes.

Mitigation: Review changes to ~/.openclaw/openclaw.json before relying on the added claude-cli provider.

Risk: Auto-starting the bridge can keep the local service running longer than intended.

Mitigation: Avoid enabling auto-start unless you understand how to stop and remove the service.

Risk: Prompt and response content may be logged locally when log-file configuration is enabled.

Mitigation: Leave local file logging disabled unless the destination and retention of logs are acceptable.

## Reference(s):

- [Project homepage](https://github.com/earlvanze/oauth-coder-bridge)
- [Upstream oauth-cli-coder project](https://github.com/codeninja/oauth-cli-coder)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python scripts, and OpenClaw configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs and runs a localhost HTTP bridge that passes prompts to oauth-coder and updates the local OpenClaw provider configuration.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
