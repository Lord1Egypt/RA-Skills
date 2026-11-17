## Description:

Uses the Tavily API to run AI-enhanced web searches with summary answers, optional images, date filtering, and Chinese or English query workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyher](https://clawhub.ai/user/chyher)

### License/Terms of Use:


## Use Case:

Developers, researchers, and external users use this skill to run Tavily web searches from an agent workflow for current information, technical questions, academic research, and multilingual information gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the configured Tavily API key are sent to Tavily.

Mitigation: Install only when Tavily query sharing is acceptable, and scope the API key to the current session or a locked-down secret store when possible.

Risk: The skill reads TAVILY_API_KEY from broader .env locations than documented, including ~/.env and the current directory.

Mitigation: Review or remove the fallback locations before using the skill in shared, sensitive, or multi-project environments.

Risk: Plaintext API key storage can expose credentials if file permissions are loose.

Mitigation: If using ~/.openclaw/.env, make the file owner-readable only and avoid committing local .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyher/skills/irene-tavily)
- [Tavily homepage](https://tavily.com)
- [Tavily search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON search results, with Markdown setup and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and supports result count, search depth, answer inclusion, image inclusion, date filtering, and language preference options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
