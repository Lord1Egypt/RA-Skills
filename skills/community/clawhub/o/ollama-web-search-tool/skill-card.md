## Description:

Uses the Ollama Web Search API to search the web and fetch webpage content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnydou](https://clawhub.ai/user/sunnydou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run Ollama-backed web search queries and fetch webpage content from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and fetched URLs are sent to Ollama.

Mitigation: Avoid submitting secrets, internal-only URLs, or confidential queries through this skill.

Risk: The Ollama API key may be visible in curl process arguments while requests are running.

Mitigation: Use a narrowly scoped or easily rotatable Ollama API key where available, and consider updating the script to pass authorization without exposing the token in process arguments.

## Reference(s):

- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search)
- [Ollama API Keys](https://ollama.com/settings/keys)
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands)
- [OpenClaw Web Tools](https://docs.openclaw.ai/tools/web)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text with search results, fetched page excerpts, URLs, and inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped by the requested max_results value from 1 to 10; fetched content is truncated for terminal display.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
