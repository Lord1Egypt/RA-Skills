## Description:

Generates executive-facing industry-chain strategy reports with patent, supply-chain, market, technology, innovation, trend, and roadmap analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise executives, strategy teams, and analysts use this skill to generate 10-page white paper-style HTML reports for company or industry-chain positioning, upstream bottleneck risk, downstream market opportunity, technical competition, innovation gaps, and action planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may appear authoritative even when underlying data is static, incomplete, or unverified.

Mitigation: Verify MCP calls, source bindings, citations, and data freshness before using reports for decisions or external distribution.

Risk: Reports generated from untrusted company or industry-chain inputs may produce unsafe or misleading HTML content.

Mitigation: Review generated HTML before opening or sharing it, and use trusted inputs and a controlled preview environment.

Risk: Person-level targeting or government-mode profiling may raise policy or compliance concerns.

Mitigation: Require policy review before using talent targeting, supplier matching, or government support profiling outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/industry-chain-intelligence)
- [PatSnap open platform](https://open.zhihuiya.com/)
- [Report template](references/report_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown summary and generated HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PatSnap MCP access for current database-backed conclusions; without that access, outputs should be treated as a report framework or template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
