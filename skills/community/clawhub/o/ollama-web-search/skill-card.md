## Description:

Web search via Ollama API. Returns relevant results from Ollama web search for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cndaqiang](https://clawhub.ai/user/cndaqiang)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to retrieve web search results from Ollama's web_search API for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Ollama through an outbound API request.

Mitigation: Avoid confidential queries unless the user's Ollama account and data handling expectations permit that use.

Risk: The skill requires an Ollama API key.

Mitigation: Provide OLLAMA_API_KEY through a managed environment or secrets mechanism and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cndaqiang/skills/ollama-web-search)
- [Skill homepage](https://github.com/QAA-Tools/skills)
- [Ollama web_search API endpoint](https://ollama.com/api/web_search)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [JSON returned from a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and OLLAMA_API_KEY; max_results is clamped from 1 to 10.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
