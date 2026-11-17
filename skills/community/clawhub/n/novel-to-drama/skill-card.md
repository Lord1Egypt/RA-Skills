## Description:

将小说片段、章节或梗概改成可排练的中文短剧剧本，同时输出 Markdown 与 JSON，包含场次、人物动作、对白、冲突升级和结尾钩子。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and short-drama planners use this skill to adapt source material they are entitled to use into rehearsal-ready Chinese scenes, or to review a draft against its source. It returns structured scripts and flags details that need confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adapting or sharing unpublished material without authorization, or material the user is not comfortable sharing with their model provider.

Mitigation: Use only source material the user is entitled to adapt and is comfortable sharing with the model provider.

Risk: Structured output may preserve factual errors or contain weak creative choices; the local script checks structure, not accuracy or quality.

Mitigation: Review every scene against the source text, and treat gaps and creative additions as items for human confirmation.

Risk: Uploading unpublished work to the optional promotional service may expose it under that service's data practices.

Mitigation: Review the service's data handling before uploading unpublished material; keep this optional step separate from script drafting.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/xxjrq/novel-to-drama)
- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/novel-to-drama)
- [Adaptation and review guide](https://github.com/xxjrq/novel-to-drama/blob/main/references/adaptation-review.md)
- [Gitee source mirror](https://gitee.com/xxjrq/novel-to-drama)
- [SkillHub listing](https://skillhub.cn/skills/user_068e9c11/novel-to-drama)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese short-drama script in Markdown and JSON, with review notes and unresolved source questions where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scene-based output with goals, actions, dialogue, conflict, turns, props, and concrete ending hooks.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
