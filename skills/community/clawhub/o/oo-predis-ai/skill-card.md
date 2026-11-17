## Description:

Operate Predis.ai through an OOMOL-connected account to create content and list posts and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create Predis.ai content and retrieve existing posts and templates through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can trigger remote CLI installation without clearly disclosing its changes; the installer and hosted implementation have not been audited.

Mitigation: Review and approve CLI installation separately, inspect whether it installs additional agent skills, and connect only the intended Predis.ai account.

Risk: Requests pass through OOMOL while using the Predis.ai integration.

Mitigation: Understand the OOMOL connection path before connecting the account, and share only information appropriate for that service.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Predis.ai](https://predis.ai)
- [Predis.ai API authorization documentation](https://predis.ai/developers/docs/predis-api/authorization/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector payloads and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill supports content creation and post or template listings.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
