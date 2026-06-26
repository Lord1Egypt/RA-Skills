## Description: <br>
Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Regan-Milne](https://clawhub.ai/user/Regan-Milne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to persist, restore, and manage encrypted agent memory across sessions and machines through a remote Jackal-backed service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Encrypted memories are stored through a remote service and may contain sensitive content. <br>
Mitigation: Confirm the storage posture is acceptable before use, avoid storing secrets, and treat memory content as sensitive data. <br>
Risk: Loss or exposure of the local encryption key can make memories unrecoverable or compromise encrypted memory content. <br>
Mitigation: Back up encryption keys securely, avoid logging JACKAL_MEMORY_API_KEY or JACKAL_MEMORY_ENCRYPTION_KEY, and rotate or delete keys according to local policy. <br>


## Reference(s): <br>
- [Jackal Memory homepage](https://web-production-5cce7.up.railway.app) <br>
- [Jackal Memory API login](https://web-production-5cce7.up.railway.app/auth/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plaintext command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JACKAL_MEMORY_API_KEY and optional JACKAL_MEMORY_ENCRYPTION_KEY environment variables; memory content is encrypted client-side before remote storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
