## Description:

将产品需求转化为Coding Agent可执行的需求文档。当用户提到"写PRD"、"产品需求文档"、"用户故事"、"功能说明"，或提供会议记录/功能描述需要整理成开发文档时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyinghan02-cell](https://clawhub.ai/user/xuyinghan02-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and agents use this skill to turn product ideas, meeting notes, user stories, and feature descriptions into structured PRD content for coding agents. It guides the conversation through background clarification, domain identification, user stories, outline confirmation, functional requirements, interaction details, and final document preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate for broad PRD, user-story, feature-description, and meeting-note requests, which may steer general planning conversations into a detailed PRD workflow.

Mitigation: Confirm that the user wants a PRD-style requirements workflow before applying the full staged process.

Risk: The workflow may suggest loading related domain skills when DNS or botnet/security keywords appear.

Mitigation: Load additional domain skills only when the requested product context clearly matches that domain or after the user confirms the domain.

Risk: Opinionated staged requirements output can omit product-specific constraints if the initial problem, goal, or success criteria are incomplete.

Mitigation: Use the skill's background-clarification and outline-confirmation steps before writing detailed functional requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyinghan02-cell/skills/prd-development)
- [Publisher profile](https://clawhub.ai/user/xuyinghan02-cell)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style structured requirements prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user stories, feature outlines, functional specifications, interaction flows, confirmation prompts, and handoff guidance for document generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
