## Description:

Analyzes a user's Markdown articles to build a writing-style profile, drafts new articles in that style, and formats them as WeChat-ready HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weikion](https://clawhub.ai/user/weikion)

### License/Terms of Use:

Apache 2.0

## Use Case:

External writers use the skill to analyze their Markdown samples, maintain a reusable style profile, draft articles in that style, and format them for WeChat publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad “my style” activation phrase may trigger for loosely related requests.

Mitigation: Use explicit style-analysis or style-writing requests, and narrow the activation wording if unrelated activations occur.

Risk: The skill's file read/write scope is not clearly declared.

Mitigation: Review and limit file access to the article library, style profile, selected template, and user-approved output location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weikion/skills/my-style-writer)
- [Style profile reference](references/style-profile.md)
- [WorkBuddy](https://www.workbuddy.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML]

**Output Format:** [Markdown style profile and formatted HTML article files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Markdown samples and an HTML template; style quality depends on the available samples.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
