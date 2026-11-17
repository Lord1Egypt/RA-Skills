## Description:

养老与传承标准化解决方案生成 Skill。读取「风险评估报告」与「二次沟通记录」，把 P0-P3 风险盘点总表逐条映射为可落地方案：医疗品质保障、养老现金流、应急保值优化、传承与监护安排、条件章节、风险-解决方案对照总表、行动优先级与时间轴、保险产品配置计划预留页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hukaiyi777](https://clawhub.ai/user/hukaiyi777)

### License/Terms of Use:

MIT-0

## Use Case:

External financial and insurance advisers use this skill after follow-up client consultations to turn a risk assessment report and second-meeting notes into a structured retirement, inheritance, insurance, and action-planning solution. The generated solution stays at tool-category, configuration-logic, and parameterized amount levels, leaving specific product names and final product details for compliant human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is used in retirement, inheritance, insurance, legal, tax, trust, and underwriting contexts where incorrect advice could affect client decisions.

Mitigation: Have qualified humans review the generated solution, disclaimers, product placeholders, compliance posture, and all regulated content before client use.

Risk: Input reports and meeting notes can include sensitive client financial, health, family, and inheritance information.

Mitigation: Use de-identified materials where possible and handle all client documents according to applicable privacy, retention, and compliance rules.

Risk: The included DOCX generator writes document metadata and branded defaults that may not match a specific adviser or client engagement.

Mitigation: Review and update adviser name, slogan, disclaimer, DOCX metadata, and default template data before distributing generated documents.

Risk: The artifact separates solution logic from specific product recommendations, but a user may ask the agent to fill concrete products or brands directly.

Mitigation: Keep specific product names, benefits, premiums, and final product plans in the reserved section only after adviser screening and institutional compliance approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hukaiyi777/skills/hky-insure-solution)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Local DOCX generator](artifact/assets/solution_template.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and Python DOCX-generation configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a warm-yellow Chinese retirement and inheritance solution document structure and configure the included local DOCX template; final financial, legal, tax, trust, underwriting, and product details require qualified human review.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
