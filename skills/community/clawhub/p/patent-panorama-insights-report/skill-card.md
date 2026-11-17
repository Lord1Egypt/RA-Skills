## Description:

This skill converts upstream patent panorama statistics, value signals, tagging taxonomies, patent packages, and SaaS-tagged pools into technology evolution analysis, moat and value interpretation, and self-contained HTML insight reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, IP strategy teams, and developers use this skill at the final stage of a patent panorama workflow to turn validated statistics, tagging outputs, and tagged patent pools into client-ready insight reports. It supports business-readable technology evolution, competitive landscape, value signal, limitation, and recommended patent package sections while preserving legal-review boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent report outputs can be mistaken for legal opinions about freedom to operate, infringement, SEP essentiality, validity, novelty, or inventiveness.

Mitigation: Keep report language framed as patent signals under the dataset, include limitations near relevant analysis, and require expert legal review before legal or enforcement decisions.

Risk: Database-backed results depend on correct PatSnap/Zhihuiya MCP configuration and authorized access.

Mitigation: Verify the MCP configuration path and account authorization before use; without configuration, limit the skill to analysis framing rather than database-backed conclusions.

Risk: Installation from a mutable package or repository reference can introduce supply-chain drift.

Mitigation: Install from a pinned package version or immutable commit and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-panorama-insights-report)
- [Zhihuiya Open Platform skill marketplace page](https://open.zhihuiya.com/marketplace/skill-hub/patent-panorama-insights-report)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown instructions that guide generation of self-contained HTML reports, JSON manifests, optional evidence registers, limitation notes, and CSV summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected report outputs include report.html and report_manifest.json; optional outputs include evidence_register.json, report_limitations.md, and recommended_patent_package.csv.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
