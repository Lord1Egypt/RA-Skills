## Description:

Use Affinda to read, create, and update data through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents handling Affinda tasks use this skill to inspect document types, documents, organizations, and workspaces; retrieve a document; or submit a document URL for parsing through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded software automatically; the remote installer behavior remains unverified.

Mitigation: Review and approve a specific, verified CLI release before setup, including any skills it adds to other agents.

Risk: The connected Affinda account can be used to submit document URLs for upload and parsing.

Mitigation: Keep permissions limited and retain confirmation for uploads.

## Reference(s):

- [Affinda API documentation](https://docs.affinda.com/)
- [Affinda homepage](https://www.affinda.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Affinda skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-affinda)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions and oo CLI commands; Affinda connector responses in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document uploads change Affinda state and require confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
