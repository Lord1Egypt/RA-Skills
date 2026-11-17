## Description:

Parallel provides high-accuracy web search and research through the Parallel.ai API, returning source URLs, excerpts, citations, and optional multi-step research modes for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to perform web research, fact-checking, company and person research, structured entity discovery, content extraction, and monitored web tracking with source-backed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, URLs, and task context are sent to Parallel.ai for processing.

Mitigation: Use the skill only with research data that is appropriate to share with Parallel.ai, and avoid submitting sensitive or regulated information unless that use has been approved.

Risk: A bundled fallback API key is present in the search helper and should be treated as compromised.

Mitigation: Set a user-controlled PARALLEL_API_KEY before use and do not rely on bundled credentials.

Risk: Authenticated browsing can pass Browser-Use credentials to an external MCP endpoint.

Mitigation: Provide Browser-Use credentials only through approved secret handling, avoid command-line secrets, and restrict authenticated browsing to approved targets.

Risk: Monitor commands can create webhooks, retrieve events, and delete remote monitors.

Mitigation: Review monitor commands before execution, verify webhook destinations, and require approval before deleting or modifying remote monitoring state.

## Reference(s):

- [Parallel.ai](https://parallel.ai)
- [Parallel API Documentation](https://docs.parallel.ai)
- [Parallel Platform](https://platform.parallel.ai)
- [ClawHub Skill Page](https://clawhub.ai/mvanhorn/skills/parallel)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Markdown text or JSON containing search results, excerpts, citations, task outputs, monitor events, or API run identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARALLEL_API_KEY; some task flows may also use BROWSERUSE_API_KEY for authenticated browsing.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
