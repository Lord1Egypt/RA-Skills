## Description:

根据输入的职业技能标准文档，生成基于知识图谱的三层职业技能学习路径，并支持 JSON、CSV 和 JSON-LD 输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzp2026](https://clawhub.ai/user/wzp2026)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, instructors, and developers use this skill to turn occupational skill standards into structured, source-labeled learning paths for vocational learning or certification preparation. The artifact focuses on Chinese domestic occupational skill standards and official domestic reference sources.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security summary says the bundled scripts and configuration may not reliably match the promised document-based, official-source workflow.

Mitigation: Manually verify generated standards, citations, and quality scores before using outputs for certification, compliance, or curriculum decisions.

Risk: Artifact scripts may use broader web sources than advertised for validation and enrichment.

Mitigation: Restrict network access where possible and require official-source review for any generated learning-path node marked as reference or inferred.

Risk: Demo or test script behavior may write local output files.

Mitigation: Run scripts only in a disposable workspace and avoid executing them on systems containing sensitive data.

## Reference(s):

- [Artifact README](artifact/references/README.md)
- [Artifact configuration](artifact/references/config.yaml)
- [ClawHub release page](https://clawhub.ai/wzp2026/skills/learning-path-builder)
- [技能人才评价工作网](https://www.osta.org.cn/)
- [国家标准全文公开系统](https://openstd.samr.gov.cn)
- [中国大学MOOC](https://www.icourse163.org)
- [教育部官网](https://www.moe.gov.cn)
- [工业和信息化部官网](https://www.miit.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON, CSV, and JSON-LD files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source labels, quality checks, progress notes, and generated learning-path artifacts.]

## Skill Version(s):

2.4.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
