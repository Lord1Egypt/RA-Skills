## Description:

A Q&A bot over your own docs with sources and stale-answer checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yysws5566](https://clawhub.ai/user/yysws5566)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can build a question-answering knowledge base from their own documents. The bot answers from stored material with sources and verification dates, checks time-sensitive questions live, and can add newly sourced answers to the local knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad everyday triggers may route unrelated requests into a workflow that retrieves and saves information; the security review is incomplete.

Mitigation: Review the security findings, narrow activation to intended knowledge-base requests, and confirm that local knowledge-base writes fit your use before enabling the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yysws5566/skills/kb-bot)
- [Publisher profile](https://clawhub.ai/user/yysws5566)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown answers with sources and verification dates, plus Markdown knowledge-base files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-sensitive answers are checked live; fast-changing numeric results are not stored as lasting knowledge.]

## Skill Version(s):

1.0.3 (source: skill frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
