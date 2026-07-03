## Description: <br>
保险责任分析技能会从保险条款图片、粘贴文本或产品链接中提取保险责任、责任免除、时间条件、金额规则、理赔条件、可持续性、健康告知和特别约定等关键信息，评分并生成交互式 HTML 可视化分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to review insurance product terms, surface coverage limits and exclusions, and produce a concise risk-oriented report before making insurance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install Python packages from the network and modify the user's environment during normal use. <br>
Mitigation: Review before installing, run it in an isolated environment, and prefer preinstalling reviewed, pinned dependencies. <br>
Risk: Insurance documents may contain sensitive policyholder or health information. <br>
Mitigation: Avoid providing highly sensitive policyholder data unless the user accepts the local processing and package-install behavior. <br>


## Reference(s): <br>
- [保险责任八维分析框架](references/analysis_framework.md) <br>
- [保险条款关键信息提取模式](references/clause_patterns.md) <br>
- [保险术语解释词典](references/insurance_terms.md) <br>
- [Tesseract OCR documentation](https://github.com/UB-Mannheim/tesseract/wiki) <br>
- [ClawHub skill listing](https://clawhub.ai/bettermen/insurance-liability-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Markdown summary, structured JSON analysis, and generated interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Python scripts for OCR, web scraping, and HTML report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
