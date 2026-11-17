## Description:

医保拒付与申诉核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

财务、出纳或医保对账人员在月结、对账或盘点时使用此技能核对医保拒付与申诉核对表的表内算术、合计、重复行和空缺。它帮助发现可复算的表格问题，但不判断拒付是否应该申诉、是否能申诉成功，也不提交申诉。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and table-reconciliation findings as medical-policy, legal, or reimbursement advice.

Mitigation: Present the skill as a local reconciliation checker only; review denial policy, clinical facts, and appeal decisions with the responsible医保办,病案室, or qualified reviewer.

Risk: The free version omits some paid-version checks, so a clean result does not mean every possible denial or appeal issue was reviewed.

Mitigation: Show executed and withheld checks in outputs and avoid representing omitted checks as performed.

Risk: Incomplete or malformed table input can lead to misleading confidence if treated as a completed check.

Mitigation: Use the documented insufficient-input behavior: report missing columns or unusable material and do not issue a pass/fail conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/medical-insurance-denial-check-free)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese human-readable text or JSON result objects from a local Node.js checker.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on copied table text or JSON input; insufficient input is reported without producing a pass/fail conclusion.]

## Skill Version(s):

1.0.48 (source: server evidence release.version, artifact frontmatter, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
