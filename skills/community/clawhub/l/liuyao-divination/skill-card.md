## Description: <br>
提供六爻排盘和传统易学占卜解读，生成本卦、变卦、世应、六亲、六神、空亡和吉凶判断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qichenx](https://clawhub.ai/user/qichenx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to generate Liuyao divination charts and formatted readings from a question and optional gender input. It is intended for traditional divination-style interpretation, not medical, legal, financial, or other professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may overrely on divination outputs for medical, legal, financial, or other professional decisions. <br>
Mitigation: Present readings as traditional divination-style guidance only and direct users to qualified professionals for high-stakes decisions. <br>
Risk: Private questions can include sensitive personal context. <br>
Mitigation: Avoid sensitive details when possible and review or delete saved history if the runtime stores one. <br>
Risk: Optional LLM mode may send questions to an external API. <br>
Mitigation: Enable LLM-assisted interpretation only when external API processing is acceptable for the user and question. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qichenx/liuyao-divination) <br>
- [LiuYaoDivining GitHub repository](https://github.com/QiChenX/LiuYaoDivining) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell commands, Python examples, and formatted Chinese divination readings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a question and optional gender input; the standalone script can also return structured Python data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
