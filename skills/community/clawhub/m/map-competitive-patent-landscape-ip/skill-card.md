## Description:

Build an evidence-backed competitive patent landscape for a defined industry, technology, competitor set, geography, and time window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External strategy, product, competitive-intelligence, and IP teams use this skill to map competitor patent activity across a defined technology, competitor set, geography, and time window. It supports executive landscape reports, representative patent review, geographic filing comparison, and evidence-backed opportunity hypotheses, not infringement or freedom-to-operate opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries and report context may include competitor, technology, or client-sensitive information.

Mitigation: Confirm PatSnap MCP use is acceptable for the project and keep sensitive context limited to the research inputs needed for the report.

Risk: PatSnap API keys or connection credentials could be exposed in prompts, reports, logs, or source control.

Mitigation: Keep API keys outside reports, prompts, logs, and source control, as the skill directs.

Risk: If live patent retrieval is unavailable or capped, sample-based observations could be overstated.

Mitigation: Use the documented fallback path and label missing, capped, sampled, or not-executed analysis clearly.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/yuanzhian-patsnap/skills/map-competitive-patent-landscape-ip)
- [Competitive patent landscape search strategy](references/SEARCH_STRATEGY.md)
- [Competitive patent landscape report template](references/REPORT_TEMPLATE.md)
- [PatSnap Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance, files]

**Output Format:** [HTML report with cited analysis, tables, charts, methodology notes, and fallback report shell when live retrieval is unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local HTML report using a safe filename; report content should include source notes, cut-off dates, denominators, and clear not-executed labels when data retrieval is unavailable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
