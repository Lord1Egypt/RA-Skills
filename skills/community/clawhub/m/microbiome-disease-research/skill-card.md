## Description:

研究微生物组与疾病机制证据链并形成研究假设，帮助梳理菌群、代谢物、宿主通路与疾病表型之间的证据链。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, product teams, and developers use this skill to perform Chinese-first microbiome literature and patent landscape research, especially for food and nutrition domains. It supports PatSnap searches, source-grouped evidence review, HTML report generation, and formation of testable research hypotheses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs could be mistaken for medical advice because the skill analyzes microbiome-disease mechanisms.

Mitigation: Treat reports as research summaries, not medical advice, and require qualified expert review before clinical, nutritional, or product decisions.

Risk: Search-based summaries may include incomplete, outdated, or misinterpreted patent and paper evidence.

Mitigation: Review the [S#] citations and full source list, keep patent and paper evidence distinct, and verify key claims against primary sources.

Risk: The security evidence notes Chinese-first behavior and some scope-label inconsistency.

Mitigation: Confirm the intended domain scope before use and request English or bilingual output when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/microbiome-disease-research)
- [Search query templates](artifact/references/search_query_templates.md)
- [HTML report template](artifact/references/html_report_template.md)
- [Topic taxonomy](artifact/references/topic_taxonomy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [HTML report with Markdown source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a standalone HTML landscape report with fixed left navigation, summary cards, grouped representative literature, and [S#] source citations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
