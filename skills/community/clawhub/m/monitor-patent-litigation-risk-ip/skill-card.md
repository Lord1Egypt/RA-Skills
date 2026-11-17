## Description:

Monitor patent-litigation exposure for a primary company and up to four named comparison parties. Use when users need target-centric identification of potentially litigated patents, patent-family and claim analysis, verified proceeding timelines, case deep dives, inventor activity, geographic exposure, litigation alerts, technology trends, and an evidence-backed HTML report with structured JSON or CSV attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, IP teams, and developers use this skill to monitor patent-litigation exposure for a named target and comparison parties, separating patent-data leads from verified tribunal or official-register facts. It supports evidence-backed HTML reporting with optional structured JSON and CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may contain sensitive legal or business analysis.

Mitigation: Keep API keys and credentials out of prompts and reports, write generated JSON/HTML/CSV files only to a chosen output folder, and review outputs before sharing.

Risk: Patent-data litigation signals or secondary sources may be mistaken for verified proceeding facts.

Mitigation: Verify material claims against primary tribunal, court, agency, or official-register records and label evidence states for unresolved or conflicting facts.

Risk: Connector access can expose broad patent and public-source research capability.

Mitigation: Approve only the needed PatSnap connectors and use the official marketplace connection flow without exposing credentials.

## Reference(s):

- [PatSnap Global Core Patent Database MCP](https://open.patsnap.com/marketplace/mcp-servers/core-patents)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [ClawHub skill release page](https://clawhub.ai/yuanzhian-patsnap/skills/monitor-patent-litigation-risk-ip)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, offline HTML reports, JSON evidence records, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are target-centric and evidence-backed; optional helpers create schema-compatible JSON and safe offline HTML.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
