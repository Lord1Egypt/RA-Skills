## Description: <br>
专为商业大赛评委设计，从人工逐份阅读到AI批量标准化打分的效率跃迁 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Competition judges and review teams use this skill to score business plans consistently across batch or single-project review workflows, including structured scoring, ranking, comments, and follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill combines local scoring with broad online background checks. <br>
Mitigation: Use external checks only with explicit consent and require human review of background, legal-risk, and verification findings before acting on them. <br>
Risk: The security review says the batch script does not actually read submitted PPT, PDF, or Word documents before scoring. <br>
Mitigation: Fix document parsing to read real submission content or fail closed, and review outputs before using them for real competition decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/opc-competition-scoring) <br>
- [README](README.md) <br>
- [打分标准参考表](references/打分标准表.md) <br>
- [常见扣分点清单](references/常见扣分点.md) <br>
- [优秀案例库](references/优秀案例库.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, ranking tables, scoring summaries, Python scripts, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured scores, deduction notes, judge comments, risk flags, and batch review outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
