## Description:

Search the web with Perplexity Sonar API for current information, citations, and web-grounded answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitinzadpe](https://clawhub.ai/user/nitinzadpe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to get current, cited web-search answers from Perplexity Sonar without leaving an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts are sent to Perplexity and may be billed to the user's Perplexity API key.

Mitigation: Use the skill only for prompts intended for external web search, keep secrets and private local data out of search queries, and configure the API key intentionally.

Risk: Web-grounded answers can still reflect incomplete, stale, or low-quality source material.

Mitigation: Review the returned citations and search results before relying on the answer for important decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nitinzadpe/skills/nz-perplexity-search)
- [Perplexity API key settings](https://www.perplexity.ai/settings/api)
- [Perplexity chat completions endpoint](https://api.perplexity.ai/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Citations, Shell commands, Guidance]

**Output Format:** [Markdown report with answer, citations, search results, related questions, and optional usage metadata; raw JSON is available with a flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and PERPLEXITY_API_KEY; queries are sent to Perplexity.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
