## Description:

Assess a narrowly defined technology opportunity through reproducible patent searches, full-scope metrics, representative patent evidence, transparent scoring, and an offline multi-page decision report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent-intelligence analysts, and commercialization teams use this skill to assess narrowly defined technical opportunities for R&D, licensing, partnering, portfolio review, or commercialization diligence. It produces evidence-qualified decision support, not legal, investment, valuation, or freedom-to-operate advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overread patent activity as proof of market demand, valuation, investment merit, or freedom to operate.

Mitigation: Treat the report as decision support only and route legal, investment, valuation, market, regulatory, and freedom-to-operate questions to separate specialist diligence.

Risk: Unavailable or partial connector outputs can make applicant, regional, status, trend, or subfield metrics misleading if substituted with representative samples.

Mitigation: Use only full-population aggregations or complete reproducible buckets for population metrics, and mark unsupported metrics unavailable instead of estimating from Top-K records.

Risk: Poorly scoped technology questions can create noisy searches and weak commercialization conclusions.

Mitigation: Confirm technical mechanism, application boundary, date range, geography, family rule, and exclusions before freezing the query and generating the report.

Risk: Generated report files can carry incorrect assumptions or stale provenance if reviewed outside the output package.

Mitigation: Run the skill in a dedicated output folder and review the generated methodology, evidence mapping, patent records, and quality-check files together.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/identify-patent-commercialization-opportunities-ip)
- [PatSnap Advanced Patent Search MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Deep Patent Mining MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [PatSnap Global Core Patent Database MCP Server](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance plus JSON, CSV, and offline HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a ten-file offline patent-opportunity report package with methodology, representative patent records, evidence mapping, and quality-check artifacts.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
