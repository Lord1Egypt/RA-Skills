## Description:

专利挖掘 Agent 面向企业研发工程师，输入技术领域与挖掘目的后，执行四块十步专利挖掘流程并生成结构化专利挖掘报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise R&D engineers, technical leads, and intellectual-property practitioners use this skill to structure patent-mining work from a technical domain and mining purpose. It helps identify candidate invention directions, assess them with patent and web research, and produce structured patent-mining reports while preserving required user confirmation checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent project details, company context, competitor notes, constraints, and CP-0 additions may be copied verbatim into generated reports.

Mitigation: Avoid entering confidential details unless they are intended to appear in the final report, and review or redact generated reports before sharing.

Risk: Patent data and competitive analysis can be incomplete or unreliable when required PatSnap and web research tools are unavailable or misconfigured.

Mitigation: Confirm required data access before relying on analysis, preserve source labels, and treat missing or uncertain information as requiring follow-up.

Risk: The skill supports patent-mining analysis but does not replace technical invention work, patent-agent drafting, or legal review.

Mitigation: Use outputs as structured preparation material and have qualified technical and intellectual-property reviewers validate conclusions before filing or disclosure decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-mining-agent)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or HTML reports with structured tables, confirmation cards, checkpoints, source labels, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include patent-mining confirmation snapshots, technical decomposition trees, problem lists, invention concepts, assessment summaries, six-month roadmaps, and final reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
