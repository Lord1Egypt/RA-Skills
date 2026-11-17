## Description:

基于 Spec Coding 理念的 PRD 影响分析工具，采用渐进式上下文管理，专注于识别客户可见的前端变化，生成可执行的代码级影响规约 (Spec)，并支持通过 Workflow 编排实现自动化实施。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohalo](https://clawhub.ai/user/ohalo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to analyze PRDs, identify backend and frontend impact, and turn requirements into reviewable change specifications before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze sensitive PRDs and codebase context.

Mitigation: Install only when the agent is allowed to access the relevant product requirements and source code.

Risk: Generated change specs may be incomplete or incorrect for permission, database, or API changes.

Mitigation: Review generated specifications before allowing optional code-generation or workflow steps to modify source code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohalo/skills/prd-impact-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown specifications with JSON intermediate representations and code-oriented pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable PRD impact specs, including backend changes, frontend customer-visible changes, risk notes, workflow steps, and implementation checklists.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
