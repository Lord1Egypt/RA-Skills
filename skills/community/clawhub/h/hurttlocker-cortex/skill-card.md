## Description:

Cortex provides local-first agent memory with Ebbinghaus decay, hybrid BM25 and semantic search, MCP tools, file import, fact extraction, and confidence tracking over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hurttlocker](https://clawhub.ai/user/hurttlocker)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Cortex to add persistent local memory, searchable imported knowledge, and MCP-accessible memory tools to OpenClaw-style multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance can download and execute unverified release binaries.

Mitigation: Prefer Homebrew or a pinned, verified release before running setup scripts.

Risk: Connector sync, scheduled sync, LLM enrichment, and local HTTP/SSE serving can persist or expose broad sensitive data.

Mitigation: Scope sources, review imported data, choose the SQLite database location deliberately, and enable these features only after review.

Risk: The wrapper reimport command deletes the configured Cortex database before rebuilding it.

Mitigation: Treat reimport as destructive and avoid setting CORTEX_DB outside the intended Cortex data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hurttlocker/skills/hurttlocker-cortex)
- [Cortex project homepage](https://github.com/hurttlocker/cortex)
- [Cortex releases](https://github.com/hurttlocker/cortex/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-formatted Cortex CLI results through wrapper commands.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
