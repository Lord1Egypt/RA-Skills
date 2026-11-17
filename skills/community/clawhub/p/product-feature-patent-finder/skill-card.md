## Description:

Researches a product feature, searches related patents, scores patent relevance, maps patents to technical dimensions, and generates a self-contained HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, and product teams use this skill to turn a natural-language product feature description into a structured patent relevance report with technical-dimension mapping and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send product-feature descriptions to web and patent-search tools.

Mitigation: Avoid entering confidential unreleased product details unless those tools are approved for that information.

Risk: Generated HTML reports can contain untrusted text, links, or image URLs from external sources.

Mitigation: Escape generated report content and restrict unsafe links or image URLs before sharing or deploying reports.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanzhian-patsnap/skills/product-feature-patent-finder)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Analysis, Files, Code, Guidance]

**Output Format:** [Self-contained HTML report with embedded CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local report under @session/reports/patent_finder_<timestamp>.html; patent search results depend on configured PatSnap MCP tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
