## Description:

见自己引导用户通过低压的自我探索问答梳理经历、价值观和成长线索，并生成“AI眼中的你”分析报告及第一人称公众号风格文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for guided self-reflection, life review, and personal narrative drafting. It helps an agent ask reflective questions, summarize user-provided material, and prepare a report and first-person article based on the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transform sensitive personal disclosures into reports and public-style article drafts.

Mitigation: Ask for fresh user confirmation before generating or sharing reports or articles, and avoid including private details unless the user explicitly approves them.

Risk: A user stop request may conflict with the artifact behavior that continues into report generation.

Mitigation: Treat any request to stop as stopping all further processing unless the user separately asks for a summary.

Risk: The workflow asks for or may infer age and gender, which can create inaccurate or sensitive profiling.

Mitigation: Use neutral language when demographic details are unavailable, ask only when needed, and do not infer gender or age from unrelated context.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational responses, structured analysis report, and first-person article draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reflective questions, personal analysis, public-style article text, and image prompt guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
