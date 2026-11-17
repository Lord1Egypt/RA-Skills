## Description:

High-accuracy web search and research via Parallel.ai API. Optimized for AI agents with rich excerpts and citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pntrivedy](https://clawhub.ai/user/pntrivedy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to perform Parallel.ai-backed web research, fact-checking, and company or person research with citations and structured excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact embeds and silently falls back to a plaintext Parallel.ai API key.

Mitigation: Remove and revoke the embedded key, and require users to provide their own PARALLEL_API_KEY before use.

Risk: Queries are sent to Parallel.ai, a third-party service.

Mitigation: Disclose third-party data handling clearly and avoid submitting secrets, private prompts, or proprietary data unless approved for that service.

Risk: The Python dependency is not pinned in the setup instructions.

Mitigation: Pin and review the parallel-web dependency version before deployment.

## Reference(s):

- [Parallel.ai Documentation](https://docs.parallel.ai)
- [Parallel.ai Platform](https://platform.parallel.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown search summaries or JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs, titles, excerpts, publish dates when available, search IDs, and API usage stats.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
