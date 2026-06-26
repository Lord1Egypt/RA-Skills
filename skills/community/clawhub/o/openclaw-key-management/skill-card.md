## Description: <br>
Secure credential storage system for OpenClaw that encrypts and protects API keys, tokens, and sensitive credentials from memory file compromise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keven0706](https://clawhub.ai/user/keven0706) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers managing OpenClaw deployments use this skill to add, retrieve, migrate, and reference encrypted credentials while keeping plaintext secrets out of memory files and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill handles and modifies sensitive secrets. <br>
Mitigation: Review carefully before installing and avoid using it with real credentials until the package has been checked in the target environment. <br>
Risk: Temporary plaintext scripts and hard-coded workspace paths can expose credentials or affect unintended files. <br>
Mitigation: Confirm scripts avoid plaintext temporary files, remove hard-coded workspace paths, and operate only on the intended OpenClaw workspace before use. <br>
Risk: Documented passphrase mode, memory locking, and cleanup behavior may not fully match the implementation. <br>
Mitigation: Validate passphrase mode, memory locking, secret cleanup, and MEMORY.md modification behavior before relying on the skill for sensitive credentials. <br>


## Reference(s): <br>
- [OpenClaw Key Management on ClawHub](https://clawhub.ai/keven0706/openclaw-key-management) <br>
- [Instreet community post](https://instreet.coze.site/post/4da5da91-9a33-4f7a-b8a0-1533616baa74) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces credential-management guidance and local command examples for OpenClaw workspaces.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
