## Description:

Reviews Korean patent application claim sets from uploaded PDF, Word, or text files against Korean Patent Act and KIPO examination practice, producing structured findings and claim-by-claim revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent practitioners and IP teams use this skill to inspect Korean patent application claims, identify legal, drafting, scope, and examination-practice issues, and draft claim-by-claim revision recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent claims or extracted technical features may be sent to PatSnap during prior-art searches.

Mitigation: Use the skill only with documents authorized for PatSnap processing, and require explicit user confirmation before external searches involving confidential or unpublished inventions.

Risk: If PatSnap MCP is not configured, prior-art-informed invalidity and examination-risk conclusions may be incomplete.

Mitigation: Treat output as a drafting review framework until PatSnap access is configured, and label any conclusions that are not supported by an external search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/kr-patent-claims-review)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown report with structured tables and optional HTML report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes claim structure summaries, issue ratings, prior-art-informed risk discussion when PatSnap is configured, and claim-by-claim suggested revisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
