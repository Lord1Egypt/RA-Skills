## Description:

Operate HaiGuanJia for shipment, customs, document, and tracking workflows through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Shipping and customs teams use this skill to look up shipment and vessel information, process customs filings, manage documents, and track cargo through a connected HaiGuanJia account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The software setup may execute unchecked downloads and startup synchronization may introduce changes to other agents.

Mitigation: Install a verified CLI release; consider setting OO_SKILLS_SYNC_DISABLED=1; keep write and delete approvals, check charges, and share only authorized documents and tracking data.

## Reference(s):

- [HaiGuanJia Open Platform](https://openapi.hgj.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [HaiGuanJia skill page](https://clawhub.ai/oomol/skills/oo-hgj)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured service responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, submit, update, or delete records; some requests may incur charges.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
