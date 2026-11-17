## Description:

Conduct deep research using Perplexity Agent API with web search, reasoning, and multi-model analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hushenglang](https://clawhub.ai/user/hushenglang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run current-information research, market analysis, trend analysis, investment research, and multi-model comparisons through the Perplexity Agent API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and supplied context are sent to an external Perplexity API.

Mitigation: Do not use the skill with secrets, regulated data, proprietary source, or precise location unless that use has been approved.

Risk: The skill requires a Perplexity API key.

Mitigation: Store PERPLEXITY_API_KEY in the environment or an untracked .env file and keep it out of version control.

Risk: Dependencies are specified with lower bounds rather than locked versions.

Mitigation: Pin and lock dependencies before production deployment.

## Reference(s):

- [Perplexity API](https://www.perplexity.ai/api)
- [Perplexity Client API Reference](reference.md)
- [ClawHub Skill Page](https://clawhub.ai/hushenglang/skills/perplexity-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional Python and shell command snippets; API helper methods return dictionaries containing answer, tokens, cost, and model or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports web search, streaming responses, model comparison, token and cost reporting, and configurable max token limits.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
