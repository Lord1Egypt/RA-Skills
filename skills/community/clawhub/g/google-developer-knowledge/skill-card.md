## Description:

Retrieve current, source-backed official Google developer documentation for Google Cloud, Firebase, Android, Google AI, Gemini CLI, Flutter, Go, Maps, Web, TensorFlow, and related products. Use for setup, migrations, troubleshooting, architecture, and code examples when current Google documentation matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find and verify current official Google documentation for setup, migrations, troubleshooting, architecture, and code examples. It returns source-backed explanations and identifies retrieval limits or fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to the configured MCP service or Google API and could expose sensitive information.

Mitigation: Use only public product names and minimal non-sensitive context; omit credentials, personal data, and confidential content from queries.

## Reference(s):

- [Google Developer Knowledge corpus reference](https://developers.google.com/knowledge/reference/corpus-reference)
- [Google Developer Knowledge MCP tool catalog](https://developers.google.com/knowledge/reference/mcp)
- [Developer Knowledge REST API fallback](artifact/references/api-fallback.md)
- [Google Developer Knowledge via mcporter](artifact/references/mcporter-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with source citations, code snippets, and retrieval notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cites retrieved document URIs or authoritative document names and describes the retrieval route, verification level, and any fallback used.]

## Skill Version(s):

1.0.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
