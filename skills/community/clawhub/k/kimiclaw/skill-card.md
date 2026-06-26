## Description: <br>
KimiClaw helps agents configure Kimi K2.5 as an Anthropic-compatible backend for OpenClaw, Claude Code CLI, and ACP coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to set Kimi K2.5 as the model backend for OpenClaw, Claude Code CLI, or spawned ACP coding agents. It provides configuration snippets, environment variables, and quick test commands for that setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires API credentials for the Kimi integration, and mishandled keys could be exposed in source control or logs. <br>
Mitigation: Use least-privileged, revocable keys; store them in a secret manager or untracked local environment file; avoid logging them; and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [Kimi Code Console](https://www.kimi.com/code/console) <br>
- [ClawHub Skill Page](https://clawhub.ai/jack-yang-ai/kimiclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown with JSON, bash, curl, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese guidance for API-key based provider configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
