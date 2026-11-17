## Description:

Find the exact moment in video, images or audio by describing it, using Mixpeek. Use when the user wants to search inside their own video library, find a scene or clip by description, get start and end times for a moment, or index media from a URL or object storage so it becomes searchable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esteininger](https://clawhub.ai/user/esteininger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to index authorized video, image, audio, or document content and search it by natural-language description. It helps locate relevant scenes and return timestamps and match scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media and search queries are sent to Mixpeek for cloud processing.

Mitigation: Submit only content you are authorized to process, and review retention and sync settings.

Risk: Overly broad storage access or uncontrolled indexing may expose unintended files or increase processing costs.

Mitigation: Limit storage connections to the intended bucket or prefix and set spending caps before processing.

## Reference(s):

- [Mixpeek Homepage](https://mixpeek.com)
- [Mixpeek Documentation](https://mixpeek.com/docs)
- [Object Storage Integration Guide](https://mixpeek.com/docs/integrations/object-storage/overview)
- [Mixpeek MCP Server Guide](https://mixpeek.com/docs/integrations/developer-tools/mcp-server)

## Skill Output:

**Output Type(s):** [Text, API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search matches may include descriptions, start and end timestamps in seconds, and relevance scores.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
