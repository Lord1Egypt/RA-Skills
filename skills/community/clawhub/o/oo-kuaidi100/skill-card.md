## Description:

Operate Kuaidi100 through an OOMOL-connected account to query shipment tracking, estimate shipping, and manage pickup orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to look up shipment progress, estimate delivery time or price, and quote or manage pickup orders through a connected Kuaidi100 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup instructions run a downloaded CLI installer, while the installer and CLI implementation are outside the inspected artifact.

Mitigation: Review the CLI installation separately, prefer a verified and pinned release, and check whether it installs other agent skills.

Risk: Shipping details are processed through OOMOL when using the connected account.

Mitigation: Connect only the intended account and understand the data handling before sending shipment details.

## Reference(s):

- [Kuaidi100 API documentation](https://api.kuaidi100.com/document/how-to-use-mcp-service)
- [Kuaidi100](https://www.kuaidi100.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON action results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Kuaidi100 account and the selected action.]

## Skill Version(s):

1.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
