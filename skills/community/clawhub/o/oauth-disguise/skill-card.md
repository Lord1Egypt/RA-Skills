## Description: <br>
Configure Anthropic OAuth tokens to work as OpenClaw API keys through environment variable injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill when they choose to configure Anthropic OAuth or subscription tokens as provider credentials and need environment-based setup, per-agent selection, verification, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches persistent use of Anthropic OAuth or subscription tokens as OpenClaw API credentials, which can expose account credentials or conflict with provider policy. <br>
Mitigation: Prefer officially supported API keys where possible, scope configuration per agent instead of globally, avoid sharing shell history or committed config with raw tokens, and rotate or revoke any token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafar/oauth-disguise) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users must supply and protect their own credentials.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
