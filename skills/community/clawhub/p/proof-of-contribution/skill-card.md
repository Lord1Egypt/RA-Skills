## Description:

Guides developers through setting up a GitHub Action for Bitcoin and Lightning payments tied to open source package downloads and installs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when exploring how to monetize open source projects with Bitcoin, Lightning micropayments, and GitHub workflow integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on third-party financial and CI infrastructure for Bitcoin and Lightning payment workflows.

Mitigation: Review the integration before use, verify payment and support domains directly, and require explicit confirmation for wallet or payout setup.

Risk: A GitHub Action reference could change behavior if it is not pinned.

Mitigation: Pin the action to a reviewed commit SHA and use minimal workflow permissions.

Risk: Workflow secrets may be exposed if the CI configuration is broader than needed.

Mitigation: Scope workflow permissions and secrets narrowly, and avoid exposing unrelated secrets.

## Reference(s):

- [Proof of Contribution ClawHub page](https://clawhub.ai/welove111/skills/proof-of-contribution)
- [Proof of Contribution homepage](https://github.com/welove111/proof-of-contribution)
- [BTC Vision](https://btcvision.org)
- [BTC Vision MCP endpoint](https://btcvision.org/.netlify/functions/mcp)
- [Zaprite payment link](https://pay.zaprite.com/pl_001CbTRNDN)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with YAML workflow snippets and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup guidance for third-party financial and CI services.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
