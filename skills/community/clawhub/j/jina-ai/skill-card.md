## Description:

Web reading and searching via Jina AI APIs. Fetch clean markdown from URLs (r.jina.ai), web search (s.jina.ai), or deep multi-step research (DeepSearch).

This skill is ready for commercial/non-commercial use.

## Publisher:

[adhishthite](https://clawhub.ai/user/adhishthite)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to fetch web pages as markdown, run Jina-powered web search, and perform multi-step research through Jina AI APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, research prompts, and the Jina API key are sent to Jina AI endpoints.

Mitigation: Use the skill only for data you intend to share with Jina AI, and avoid secrets, private documents, internal-only URLs, or authenticated content unless external processing is intended.

Risk: Web reading, search, and deep research outputs can include incomplete, outdated, or misleading third-party content.

Mitigation: Review the returned content and sources before relying on the output for decisions or publishing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adhishthite/skills/jina-ai)
- [Jina AI](https://jina.ai/)
- [Jina Reader](https://jina.ai/reader)
- [Jina Search API docs](https://s.jina.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON from Jina APIs, with shell command and configuration guidance for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JINA_API_KEY; sends user-provided URLs, search queries, and research prompts to Jina AI endpoints.]

## Skill Version(s):

1.0.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
