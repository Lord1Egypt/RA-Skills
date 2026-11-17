## Description:

Design and generate a configurable single-file enterprise patent-portfolio operations workspace with a dashboard, asset register, fee/deadline view, outside-counsel analytics, competitor monitoring, FTO workflow intake, patent-value screening, and novelty-search intake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

In-house IP operations teams, patent portfolio managers, and R&D legal teams use this skill to prototype or refresh a patent-portfolio workspace from authorized patent data. It supports portfolio status review, fee and deadline coordination, counsel analytics, competitor monitoring, and intake workflows for FTO, valuation, and novelty review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential patent information, attorney work product, API keys, billing data, or personal information could be exposed to an unapproved connector or external service.

Mitigation: Use only authorized patent portfolio data and confirm that PatSnap or backend connectors are approved for confidential IP work before sharing sensitive inputs.

Risk: A generated static HTML workspace could be mistaken for a production system with persistence, notifications, payments, writeback, or secure backend controls.

Mitigation: Treat generated HTML as a read-only prototype unless a secure backend is separately approved for persistence, notifications, payments, or writeback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/manage-patent-portfolio-ip)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Global Core Patent Database MCP](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and self-contained HTML workspace code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a portable prototype and data/workflow contract; backend-dependent persistence, notifications, payments, writeback, and connector actions require separate approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
