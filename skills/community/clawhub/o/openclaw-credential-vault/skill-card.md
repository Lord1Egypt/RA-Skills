## Description: <br>
Encrypted credential management for OpenClaw that keeps API keys, tokens, and passwords out of the AI agent context with AES-256-GCM encryption, subprocess-scoped injection, and automatic output scrubbing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karanuppal](https://clawhub.ai/user/karanuppal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate an OpenClaw credential vault that stores secrets locally, injects them only into matching subprocesses, and scrubs output before the agent receives it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad credential-hook access for OpenClaw command execution, outbound messages, and session transcripts. <br>
Mitigation: Review the npm package source before installing, especially hook registration, credential injection, output scrubbing, key derivation, and audit logging. <br>
Risk: The security summary reports an unexplained vault token in the skill instructions. <br>
Mitigation: Inspect the published package and submitted skill text before use, and do not add real credentials until the token handling and scrubbing behavior are verified in a local test environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/karanuppal/openclaw-credential-vault) <br>
- [Source repository](https://github.com/karanuppal/openclaw-credential-vault) <br>
- [Hook implementation](https://github.com/karanuppal/openclaw-credential-vault/tree/main/src/hooks) <br>
- [npm package](https://www.npmjs.com/package/openclaw-credential-vault) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create encrypted vault files, injection rules, metadata, and audit logs under ~/.openclaw/vault/.] <br>

## Skill Version(s): <br>
1.0.0-beta.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
