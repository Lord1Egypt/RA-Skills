## Description:

需求文档生成智能体：输入需求要点，自动生成标准PRD，支持变更追踪与历史PRD检索

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahsh](https://clawhub.ai/user/mahsh)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and cloud phone development teams use the skill to turn rough requirements into structured PRDs, align terminology and format with historical PRDs, and document changes between versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requirement-derived keywords may be sent to the configured Dify service for historical PRD retrieval.

Mitigation: Use a Dify service you trust, and avoid sending sensitive product details unless you understand how that service handles them.

## Reference(s):

- [PRD Generator (Cloud Phone) on ClawHub](https://clawhub.ai/mahsh/skills/prd-generator-cm)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Structured Markdown PRD with tables; optional change summary and change log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-based sections for background, scope, user stories, requirements, acceptance criteria, risks, dependencies, and appendices; can archive the generated PRD.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
