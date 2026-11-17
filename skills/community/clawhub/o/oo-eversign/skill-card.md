## Description:

Use the oo CLI to read and manage Xodo Sign documents, templates, signers, and reminders through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Xodo Sign account can manage documents and templates, inspect audit history, and handle signer follow-up through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup allows remote code execution without sufficient controls or disclosure of broader agent changes; the installer and connector implementation have not been verified.

Mitigation: Review and approve CLI installation separately, check its managed-skill behavior, and consult the vendor guidance for OO_SKILLS_SYNC_DISABLED before enabling startup skill synchronization.

Risk: Document creation, reminders, and signer reassignment can change Xodo Sign account state.

Mitigation: Connect only the intended Xodo Sign account, confirm the exact payload and effect before writes or destructive reassignment, and retain confirmation for each action.

## Reference(s):

- [Xodo Sign](https://eversign.com/)
- [Xodo Sign API documentation](https://eversign.com/api/documentation/methods)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and JSON responses, plus explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands that change Xodo Sign data require user confirmation; signer reassignment is destructive.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
