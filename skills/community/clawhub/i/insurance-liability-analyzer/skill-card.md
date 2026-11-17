## Description:

保险责任分析可从保险条款图片、文本或网页链接中提取关键条款，按八个维度评分并生成交互式 HTML 分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze Chinese insurance product terms from screenshots, pasted text, or product URLs. It identifies coverage duties, exclusions, timing rules, payment limits, claim conditions, sustainability terms, health disclosures, and special clauses so the user can review key risks before making insurance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Python packages at runtime.

Mitigation: Run it in an isolated environment and preinstall dependencies from a locked manifest instead of allowing runtime package installation.

Risk: The skill can fetch arbitrary URLs supplied by a user.

Mitigation: Do not provide internal, localhost, or private-network URLs, and restrict outbound network access for untrusted use.

Risk: Generated HTML reports may contain content derived from untrusted insurance text or web pages.

Mitigation: Open generated reports only in a non-sensitive browser session and review the report before sharing or acting on it.

## Reference(s):

- [保险责任八维分析框架](references/analysis_framework.md)
- [保险条款关键信息提取模式](references/clause_patterns.md)
- [保险术语解释词典](references/insurance_terms.md)
- [Tesseract OCR installation notes](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text summary, structured JSON analysis data, and generated HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes eight-dimension scoring, risk signals, recommendations, a timeline-oriented analysis, and a radar-chart visualization.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
