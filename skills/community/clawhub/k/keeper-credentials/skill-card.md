## Description:

Securely broker user-authorized Keeper vault credentials into agent-to-agent conversations using scoped access and zero-knowledge encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill when an agent needs access to specific Keeper-stored credentials to authenticate a request with another agent or service. It supports scoped vault access, credential listing without values, and delivery through one-time share links, Keeper notation references, or inline values when explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose raw Keeper credentials when inline delivery or value-fetching commands are used.

Mitigation: Use one-time share or Keeper notation delivery when possible, and require explicit approval for the exact recipient and record before inline delivery.

Risk: Share mode may require a persistent Keeper Commander session in addition to scoped Keeper Secrets Manager access.

Mitigation: Protect KEEPER_COMMANDER_CONFIG as a high-value credential and enable share mode only when the persistent Commander access is acceptable for the deployment.

Risk: The persisted KSM configuration grants ongoing access to the shared vault folders.

Mitigation: Use a dedicated Keeper Secrets Manager application, share only the smallest necessary folders, and protect KEEPER_SKILL_HOME with durable private storage.

Risk: Dependency behavior may change in sensitive credential-handling environments.

Mitigation: Pin or review Keeper dependencies before deployment in sensitive environments.

## Reference(s):

- [Keeper Credentials on ClawHub](https://clawhub.ai/zmtucker/skills/keeper-credentials)
- [Keeper Secrets Manager Developer SDK Library](https://docs.keeper.io/keeperpam/secrets-manager/developer-sdk-library)
- [KSM authentication and cross-session persistence](references/ksm_auth_and_storage.md)
- [Delivery modes and agent-to-agent orchestration](references/delivery_modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce sensitive credential payloads or one-time share URLs depending on delivery mode.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
