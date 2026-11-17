## Description:

Audit and harden an OpenClaw installation for common security misconfigurations including exposed listeners, missing authentication, permissive tool policies, open DM access, plaintext API keys, and insecure file permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review an OpenClaw setup during installation, reconfiguration, or security review. It guides local checks for gateway exposure, authentication, privileges, tool policy, channel access, and secret handling before proposing fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local OpenClaw configuration, process state, permissions, environment values, and secret hygiene signals.

Mitigation: Run it only in the intended workspace and review any proposed changes before approving them.

Risk: Security checks can require configuration or permission changes that affect OpenClaw operation.

Mitigation: Require explicit user confirmation before changing files, permissions, users, or startup commands, and restart OpenClaw after accepted configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billyhetech/skills/openclaw-hardening-v1)
- [ClawHub publisher profile](https://clawhub.ai/user/billyhetech)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and a concise text report card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local OpenClaw configuration, process state, permissions, environment values, and secret hygiene signals; changes require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
