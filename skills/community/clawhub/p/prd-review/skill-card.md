## Description:

自动化审查商业化产品需求文档的逻辑准确性与闭环性，提取界面/功能/商业化设计要点并划分高-中-低优先级，输出设计师友好的标准化梳理文档；当用户需要审查PRD、梳理设计要点、划分设计优先级或快速对接开发时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis0220](https://clawhub.ai/user/hollis0220)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, designers, and product teams use this skill to review commercial PRDs, identify logic gaps, extract design work items, and prioritize UI, interaction, visual, and state design tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided PRD files may contain confidential product, business, or customer information, and the parser prints extracted document text into the agent session.

Mitigation: Provide only PRD content intended for agent review, remove secrets or unnecessary sensitive details before parsing, and prefer pasted excerpts for highly sensitive sections.

## Reference(s):

- [Commercial PRD review checklist and output template](artifact/references/review_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with structured tables and optional local parser command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print extracted PRD document text into the agent session before analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
