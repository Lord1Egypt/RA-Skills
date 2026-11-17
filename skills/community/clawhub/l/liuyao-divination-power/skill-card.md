## Description:

专业六爻纳甲筮法排盘与解卦，支持自动起卦排盘、十步分析、独立审查流程和 HTML 报告生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanding1998](https://clawhub.ai/user/seanding1998)

### License/Terms of Use:

个人免费·商业授权

## Use Case:

External users and agent operators use this skill to run a structured 六爻纳甲 divination workflow: confirm the question, generate or parse a hexagram, perform stepwise analysis, validate the result, and produce a deliverable report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create persistent local case folders and reports containing a user's full question and analysis.

Mitigation: Avoid highly sensitive personal data, store generated case files in an expected location, and delete or restrict access to reports that should not be retained or shared.

Risk: The workflow recommends installing an unpinned optional package for calendar calculations.

Mitigation: Prefer the pure-Python fallback when appropriate, or review and pin the optional dependency before installation in managed environments.

Risk: Generated HTML may include unsafe unescaped user- or model-supplied fields.

Mitigation: Do not open or share generated HTML from untrusted or adversarial input until report escaping is verified.

Risk: Reports may contain fixed personal contact branding.

Mitigation: Review generated reports before distribution and make branding optional or remove it where it is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanding1998/skills/liuyao-divination-power)
- [README](README.md)
- [六十四卦八宫归属](references/64-gua.md)
- [八卦万物类象](references/bagua-leixiang.md)
- [地支合冲刑害关系全表](references/di-zhi-relations.md)
- [动变法则详解](references/dong-bian-fa-ze.md)
- [伏神飞神·日月入卦·卦身](references/fushi-riyue-guashen.md)
- [HTML 报告生成指南](references/html-report-guide.md)
- [解卦详细执行手册](references/jie-gua-xiang-jie.md)
- [六亲六神兽类象](references/liuqin-liushen-leixiang.md)
- [规则编号注册表](references/rule-index.md)
- [十二地支万物类象](references/shier-dizhi-leixiang.md)
- [特殊格局速查](references/te-shu-ge-ju.md)
- [五行生克完整速查](references/wuxing-shengke.md)
- [高级应期法则](references/yingqi-faze.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis, JSON case data, and HTML report files with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow writes persistent local case folders and reports that may contain the user's full question and analysis.]

## Skill Version(s):

2.0.1 (source: SKILL.md metadata.version, README, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
