## Description:

Uses the Tavily API to return compact web search results with titles, URLs, snippets, and optional short answer summaries for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lym20220107](https://clawhub.ai/user/lym20220107)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill when web search is requested and Brave web_search is unavailable or undesired. It returns small result sets from Tavily so agents can cite URLs, inspect snippets, or include a short answer summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a Tavily API key and can read it from TAVILY_API_KEY or ~/.openclaw/.env.

Mitigation: Provide the key through the environment or a secret manager when possible, and restrict access to any local .env file that contains the key.

Risk: Search queries and the Tavily API key are sent to Tavily during normal operation.

Mitigation: Use the skill only for queries appropriate to send to Tavily, and avoid submitting confidential or regulated data unless approved for that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lym20220107/skills/lym-tavily-search)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown search results with title, URL, snippet, and optional answer fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count is clamped to 1-10; images and raw page content are not requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
