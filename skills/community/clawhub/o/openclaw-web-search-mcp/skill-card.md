## Description:

Provides AI agents with web search, page and PDF extraction, YouTube transcript retrieval, summarization, semantic search, and automated research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nishant-clawit](https://clawhub.ai/user/nishant-clawit)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this MCP skill to let agents search the web, extract web and PDF content, retrieve YouTube transcripts, summarize text, perform semantic search, and run multi-step research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated URLs may allow requests to private or internal destinations.

Mitigation: Run only in a sandbox with restricted network egress and trusted callers until URL validation and private-network blocking are added.

Risk: The YouTube transcript path uses shell command execution and may run local commands if input is unsafe.

Mitigation: Replace shell execution with argument-based process execution, or disable the transcript tool until that fix is made.

Risk: Network extraction can consume excessive time or data without explicit limits.

Mitigation: Add request timeouts, response size limits, dependency updates, and review steps before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nishant-clawit/skills/openclaw-web-search-mcp)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON responses containing search results, extracted content, transcripts, summaries, embeddings, semantic matches, or research findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-dependent outputs; extracted page, PDF, and transcript content may be truncated.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
