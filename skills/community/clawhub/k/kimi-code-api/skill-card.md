## Description:

One-click setup to use Kimi K2.5 (Kimi Code) as your coding model in OpenClaw and Claude Code CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw or Claude Code CLI to route coding work through Kimi K2.5 using Anthropic Messages API-compatible settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and code handled through this setup are sent to Kimi's external API.

Mitigation: Install and use the skill only when routing OpenClaw or Claude Code work through Kimi is intended and acceptable for the data involved.

Risk: Real API keys could be exposed if copied into tracked configuration or shared examples.

Mitigation: Use real keys only in local untracked configuration, environment variables, or a secure secret store, and avoid pasting secrets into examples.

## Reference(s):

- [Kimi Code Console](https://www.kimi.com/code/console)
- [Kimi Coding API Base URL](https://api.kimi.com/coding)
- [Kimi Messages API Endpoint](https://api.kimi.com/coding/v1/messages)
- [Chinese Integration Guide](references/SKILL_CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, curl, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Anthropic-compatible endpoint settings, environment variables, OpenClaw configuration snippets, raw API examples, and setup caveats.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
