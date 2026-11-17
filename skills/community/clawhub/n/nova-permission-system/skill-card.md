## Description:

Nova Permission System provides a personal AI assistant permission framework with role-based access checks, identity verification, approval handling, audit logging, and local JSON configuration templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rancho718](https://clawhub.ai/user/rancho718)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal AI assistant operators use this skill to add role-based permission checks, identity verification, approval workflows, and audit records before an agent performs sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent control over the agent could affect tool use, file access, private data, and external-account actions.

Mitigation: Review and scope the integration before installation; avoid AGENTS.md-wide mandatory rules until the behavior is limited to explicit permission-check entry points.

Risk: Broken or fail-open authentication behavior can allow sensitive operations when identity data is missing, configuration is disabled, or an exception occurs.

Mitigation: Require fail-closed authorization paths, consistent user/account data schemas, and tests for missing identifiers, disabled configuration, exceptions, and denied roles.

Risk: Shared verification codes and approval data may expose secrets or sensitive identity state.

Mitigation: Hash or redact shared secrets, restrict access to local data files and audit logs, and define retention and uninstall procedures.

Risk: Owner approvals are represented as text commands and may not prove the approver is authenticated.

Mitigation: Bind approval actions to an authenticated owner identity and reject approval messages that cannot be tied to that identity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rancho718/skills/nova-permission-system)
- [Publisher Profile](https://clawhub.ai/user/rancho718)
- [Artifact Install and Usage Guide](artifact/SKILL.md)
- [Permission Check Documentation](artifact/permission-check/SKILL.md)
- [Permission Gate Documentation](artifact/permission-gate/SKILL.md)
- [Identity Management Documentation](artifact/identity-management/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets plus JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local permission-system guidance and configuration assets for an agent workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
