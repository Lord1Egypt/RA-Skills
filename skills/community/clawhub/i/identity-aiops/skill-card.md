## Description:

Operates Keycloak and authentik identity providers with identity overviews, user and client reviews, event analysis, MFA coverage checks, and governed account changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Identity administrators and security engineers use this skill to review Keycloak or authentik users, events, clients, and MFA coverage, investigate access issues, and carry out account or client changes with audit records. It is intended for self-managed Keycloak and authentik environments; cloud identity providers are out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity changes can affect access, and session revocation or client-secret rotation cannot be undone.

Mitigation: Start with view-only permissions. Before enabling writes, verify the exact account, client, and change, arrange approval controls outside the model, and test in a lab.

Risk: The master password may be exposed through client configuration or shared files.

Mitigation: Prefer secure runtime secret injection; otherwise restrict file access and exclude the password from repositories and shared exports.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/identity-aiops)
- [Project homepage](https://github.com/AIops-tools/Identity-AIops)
- [Capabilities reference](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON tool results with concise Markdown guidance and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only reviews and analyses, plus identity-provider changes whose availability depends on platform support and the connected account's permissions.]

## Skill Version(s):

0.12.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
