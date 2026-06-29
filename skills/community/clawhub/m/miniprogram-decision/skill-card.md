## Description: <br>
微信小程序开发辅助决策助手。用户提供产品名称和方向，综合微信指数、竞品分析、行业数据、商业模式、推广策略、开发技巧等多维度数据，生成专业的可行性决策报告（HTML）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and founders use this skill to evaluate whether a proposed WeChat mini program is worth building. It gathers public market and competitor signals, applies a six-dimension weighted model, and generates a decision-oriented HTML feasibility report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML can include unescaped competitor or web-sourced text. <br>
Mitigation: Treat generated reports as untrusted, review the output path first, and open reports cautiously outside browser profiles with sensitive sessions. <br>
Risk: Public search data, WeChat index estimates, and competitor counts can be incomplete or stale. <br>
Mitigation: Use the report as decision support and verify important market, competitor, and compliance claims before committing product resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/miniprogram-decision) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML report file with supporting text, JSON inputs, and CLI or Python invocation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports include market analysis, competitor review, scoring, development guidance, risk notes, and a final build decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
