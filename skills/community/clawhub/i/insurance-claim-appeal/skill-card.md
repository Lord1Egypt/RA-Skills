## Description:

保险理赔纠纷维权辅助分析工具，帮助保险顾问拆解健康险拒赔理由、匹配相关法律依据、规划申诉路径，并生成申诉函、投诉书和证据清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baozhiyin](https://clawhub.ai/user/baozhiyin)

### License/Terms of Use:

MIT-0

## Use Case:

External insurance consultants and claim-support agents use this skill to analyze denied Chinese health insurance claims, organize supporting evidence, and draft appeal or regulator complaint materials. It is positioned as insurance consulting support, not legal representation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may process identity, contact, policy, and medical details while preparing claim appeal materials.

Mitigation: Redact unnecessary ID digits, contact details, unrelated medical history, and policy identifiers before sharing documents; provide only materials needed for the specific dispute.

Risk: Draft appeal or complaint materials could be mistaken for formal legal advice or guaranteed claim outcomes.

Mitigation: Treat outputs as insurance consulting support, avoid outcome guarantees, and consult a licensed lawyer before making litigation or arbitration decisions.

Risk: Incorrect or incomplete policy terms, medical records, or rejection notices can produce misleading analysis.

Mitigation: Base conclusions on the actual policy, rejection notice, and medical evidence supplied by the user, and mark missing materials for follow-up before submission.

Risk: Submitting sensitive claim materials through informal channels can expose personal or medical information.

Mitigation: Use official secure insurer, regulator, mediation, or legal channels for submission and retain delivery or receipt records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baozhiyin/skills/insurance-claim-appeal)
- [理赔维权路径与操作流程](references/appeal_paths.md)
- [合规边界与免责声明](references/compliance.md)
- [保险理赔维权核心法条与依据](references/legal_basis.md)
- [常见拒赔场景与应对策略](references/rejection_scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown analysis, evidence checklists, and appeal or complaint letter drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include a case summary, rejection analysis, prioritized appeal paths, evidence checklist, draft documents when requested, and a compliance notice.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
