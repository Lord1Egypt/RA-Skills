## Description:

Mainland China A-share stock and sector analysis tool for stock snapshots, finance indicators, chip and price levels, sector lookup, subscription workflows, strategy and researcher queries, bayesian monitor lookup, and preview stock or sector deep research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jickchen34](https://clawhub.ai/user/jickchen34)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Mainland China A-share stock snapshots, financial context, sector analysis, strategy and researcher lookups, subscription and bucket workflows, and preview stock or sector deep research. It is intended for non-sensitive public market queries with authenticated Tianshan API access where required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles persistent KUNGFU_OPENKEY credentials and account-scoped finance data.

Mitigation: Install only if the publisher and Tianshan API operator are trusted, and provision KUNGFU_OPENKEY through a secure secret manager where possible.

Risk: Subscription and bucket workflows can change account-scoped finance state.

Mitigation: Review requested subscription or bucket changes before running mutating flows.

Risk: Optional research search can send requests to a separately configured endpoint.

Mitigation: Enable research search only with a trusted HTTPS endpoint and a separate search credential.

Risk: The release includes a self-update path.

Mitigation: Require explicit approval before applying updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jickchen34/skills/kungfu-finance)
- [Parsed Metadata Homepage](https://github.com/kungfu-trader/kungfu-skills)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Research Flows Overview](artifact/references/research-flows/README.md)
- [Stock Analysis Flow Contract](artifact/references/research-flows/stock-analysis/flow_contract.md)
- [Sector Analysis Flow Contract](artifact/references/research-flows/sector-analysis/flow_contract.md)
- [Data Product Schemas](artifact/references/schemas/data_products.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown and structured text, with generated SVG or PNG chart files for indicator chart flows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return needs_input, blocked, degraded coverage, or file path fields depending on the selected workflow.]

## Skill Version(s):

0.4.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
