## Description:

URL content extraction via Parallel API. Extracts clean markdown from webpages, articles, PDFs, and JS-heavy sites. Use for reading specific URLs with LLM-ready output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract clean, LLM-ready content from specific URLs, including webpages, articles, PDFs, and JavaScript-heavy sites. It is suited for answering user requests that require reading a known page after search or source selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs and extracted page content may be sent to Parallel's third-party service.

Mitigation: Use the skill only for sources where third-party extraction is appropriate; avoid internal, authenticated, confidential, or legally restricted pages unless approval is confirmed.

Risk: The workflow depends on an installed and authenticated parallel-cli.

Mitigation: Check parallel-cli availability before use and direct users to the Parallel CLI integration guide when installation or authentication fails.

## Reference(s):

- [Parallel Homepage](https://parallel.ai)
- [Parallel API Docs](https://docs.parallel.ai)
- [Parallel Extract API Reference](https://docs.parallel.ai/api-reference/extract)
- [Parallel CLI Integration Guide](https://docs.parallel.ai/integrations/cli)
- [ClawHub Skill Page](https://clawhub.ai/normallygaussian/skills/parallel-extract)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; extracted page content may be returned as JSON or clean Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports focused extraction objectives, excerpts, full content, publish dates when available, and output-size limits.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
