## Description:

This skill helps civil and commercial litigators analyze cases, construct claims and defenses, audit litigation documents, rehearse trial strategy, and predict likely judgment paths through a six-phase workflow based on the Nine-Step Method of Elements Trial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangongshilv](https://clawhub.ai/user/jiangongshilv)

### License/Terms of Use:

MIT-0

## Use Case:

External lawyers and legal teams use this skill to structure Chinese civil and commercial case intake, claim-basis analysis, offense-defense reasoning, document consistency checks, trial preparation, and strategy review. It is intended as a legal workflow and drafting aid, not a substitute for professional judgment or jurisdiction-specific review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process client identities, communications, evidence, litigation strategy, and other confidential case details.

Mitigation: Redact unnecessary sensitive data, limit inputs to the facts needed for the task, and handle generated work products under the user's legal confidentiality controls.

Risk: The legal workflow is aimed at Chinese civil and commercial matters and may be inappropriate for other legal systems or case types.

Mitigation: Confirm the matter fits Chinese civil or commercial legal work before using the outputs in case strategy or drafting.

Risk: The bundled DOCX exporter runs local Python code and depends on python-docx.

Mitigation: Run the exporter only on specific working folders, preferably in a virtual environment with a reviewed pinned python-docx dependency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangongshilv/skills/lawyer-case-strategist)
- [九步法理论体系详解](references/九步法理论体系详解.md)
- [六阶段详细操作规范](references/六阶段详细操作规范.md)
- [请求权抗辩基础备考表](references/请求权抗辩基础备考表.md)
- [借贷合同纠纷全流程运用解析](references/借贷合同纠纷全流程运用解析.md)
- [裁判文书八个一致深度解析](references/裁判文书八个一致深度解析.md)
- [法官释明与心证公开信号解读](references/法官释明与心证公开信号解读.md)
- [法官释明与价值观深度解析](references/法官释明与价值观深度解析.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown legal work products, checklists, strategy notes, and optional DOCX export commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable Markdown templates for intake, claim-basis analysis, offense-defense mapping, document audit, trial preparation, and judgment prediction.]

## Skill Version(s):

3.0.0 (source: server release evidence; skill frontmatter lists 3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
