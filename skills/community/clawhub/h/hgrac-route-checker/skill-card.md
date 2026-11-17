## Description:

Helps assess whether a human genetic resources activity in China may require approval or filing, returning a decision-support result for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, project reviewers, and compliance teams use the skill to triage collection, storage, use, transfer, or international cooperation involving human genetic resources before confirming requirements against official rules.

### Deployment Geography for Use:

China (regulatory scope)

## Known Risks and Mitigations:

Risk: The declared file, web, and shell tool access exceeds the skill's stated no-permission design.

Mitigation: Review and limit tool permissions before installation; remove unnecessary write, web, and broad shell or file access unless justified.

Risk: Human genetic resource details could include sensitive personal information.

Mitigation: Avoid entering personal identifiers or raw sensitive records unless organizational policy permits their use.

Risk: An incorrect route or unverified rule citation could mislead a compliance decision.

Mitigation: Confirm the route and cited clauses against current official texts with a qualified reviewer before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/hgrac-route-checker)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an approval-or-filing route, supporting rule references, obligations and warnings; incomplete or invalid inputs require review. Not legal advice.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
