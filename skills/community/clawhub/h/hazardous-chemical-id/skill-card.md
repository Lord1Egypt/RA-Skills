## Description:

危险化学品辨识技能。当用户需要查询某个化学品是否属于危险化学品、查询其危险性分类、重点监管类别、易制毒/易制爆/监控化学品属性、重大危险源临界量、安全措施和应急处置原则时，使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[709571520](https://clawhub.ai/user/709571520)

### License/Terms of Use:

MIT-0

## Use Case:

External users, safety professionals, compliance staff, emergency managers, and chemical-industry practitioners use this skill to identify whether chemicals fall under China-specific hazardous chemical, precursor, explosive precursor, monitored, specially controlled, highly toxic, or key-regulated categories. It produces structured reference reports for chemical safety and regulatory review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hazardous-chemical classification or safety guidance may be incomplete, outdated, or unsuitable as the sole basis for safety and compliance decisions.

Mitigation: Treat outputs as reference material and verify results against current official regulations and the applicable MSDS/SDS before taking operational, safety, or compliance action.

Risk: The skill may rely on a named ima knowledge base and public chemical sources for lookups.

Mitigation: Confirm that the knowledge base and public-source access are approved for the deployment environment and review source notes in generated reports.

## Reference(s):

- [危险化学品辨识流程详解](references/identification-workflow.md)
- [法规与目录参考](references/regulations-and-catalogs.md)
- [ClawHub Skill Page](https://clawhub.ai/709571520/skills/hazardous-chemical-id)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report or batch summary table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include chemical identifiers, hazardous classifications, regulatory-list membership, major-hazard threshold information, safety measures, emergency response principles, and source notes when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
