## Description:

用于专利全景项目的环节3。本 Skill 推荐标引体系，包括 4 列技术拆解表（≤40 个三级节点，彼此互斥）、≥10 个关键技术问题、≥10 个推荐专利包（每包≥3 个同族，六项推荐规则），并提供 20–30 条记录的标引示范和待标引导出文件。全量逐条标引在客户 SaaS 标引工具中完成，不在本 Skill 中完成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent-analysis teams use this skill after candidate-pool search, SaaS tagging, and statistics generation to design a structured patent tagging taxonomy, select representative patent packages, create a small tagged sample, and export files for downstream SaaS tagging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review labels the release suspicious because installation and workflow sequencing are ambiguous.

Mitigation: Install only from a pinned, reviewed version or commit and confirm where this skill belongs in the patent-analysis workflow before use.

Risk: The skill depends on patent project inputs and SaaS-tagging handoffs; using broad workspace access may expose unrelated project files.

Mitigation: Limit MCP authorization and accessible input files to the relevant patent project workspace.

Risk: The skill's outputs are recommendations and samples, not legal review or exhaustive patent analysis.

Mitigation: Review generated taxonomies, sample tags, package rationales, and exported files before using them in customer workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-panorama-insights-tag)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [Open Platform marketplace entry](https://open.zhihuiya.com/marketplace/skill-hub/patent-panorama-insights-tag)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, html, configuration, guidance]

**Output Format:** [Structured project files including JSON taxonomy and question outputs, CSV patent-package and tagging exports, Markdown rationale, and optional HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a patent-tagging proposal and sample outputs; full-corpus per-record tagging is handed off to a customer SaaS tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
