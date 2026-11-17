## Description:

Collects and organizes a personal knowledge base from URLs, X/Twitter and WeChat links, screenshots, tags, and searchable saved entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and personal knowledge-base users use this skill to save URLs and screenshots, tag and index extracted content, search saved entries, and prepare digest candidate lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full submitted URLs may be sent to r.jina.ai during extraction, including private or token-bearing URLs.

Mitigation: Redact or avoid ingesting private, signed, invite, password-reset, and token-bearing URLs before running URL ingestion.

Risk: Saved links, screenshots, extracted text, metadata, and notes are written persistently to the configured KB.

Mitigation: Review content for secrets before ingestion and restrict access to the KB_ROOT storage location.

Risk: The WeChat macOS node path is an advanced manual action that may execute reviewed commands on a connected machine.

Mitigation: Require explicit user approval and inspect the exact command before using any node-side fetch workflow.

Risk: WeChat article fetching can be blocked by verification, producing placeholder entries instead of full content.

Mitigation: Use the backlog output to review blocked items and refill them later from trusted screenshots or copied article text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/knowledge-base-collector)
- [r.jina.ai extraction endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated KB entries use Markdown, JSON, JSONL, and copied image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent knowledge-base entries under KB_ROOT or the default OpenClaw KB path.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
