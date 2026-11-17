## Description:

Search Google and retrieve AI Overviews, organic search results, multi-turn AI search responses, and optional screenshots using Pangolin APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyu020923](https://clawhub.ai/user/liuyu020923)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to run Google searches through Pangolin, summarize AI Overview content, return organic result links, support follow-up search turns, or provide a search results screenshot URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Pangolin credentials and may store a reusable API key in plaintext at ~/.pangolin_api_key.

Mitigation: Use a restricted Pangolin API key where possible, keep the cache file permissions limited to the current user, remove the cache file when finished, and rotate the key if it may have appeared in logs.

Risk: Search queries and follow-up questions are sent to Pangolin APIs.

Mitigation: Avoid sending sensitive, confidential, or regulated data in search terms unless the deployment has approved Pangolin for that data.

Risk: Collecting account email and password through an agent session can expose credentials in chat or logs.

Mitigation: Prefer an API key over email and password, avoid pasting raw passwords into agent chat, and clear temporary credentials after authentication.

## Reference(s):

- [AI Mode API Reference](references/ai-mode-api.md)
- [AI Overview SERP API Reference](references/ai-overview-serp-api.md)
- [Error Codes and Troubleshooting](references/error-codes.md)
- [Output Schema Reference](references/output-schema.md)
- [AI Mode Example Output](references/examples/ai-mode-example.json)
- [SERP Example Output](references/examples/serp-example.json)
- [Pangolin](https://www.pangolinfo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Natural-language search summaries with source URLs, backed by structured JSON from the Pangolin CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI overview content, organic result links, structured error hints, and screenshot URLs when requested.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
