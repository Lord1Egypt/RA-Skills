## Description:

Extract clean, readable markdown content and optional metadata from public web pages using the Jina Reader API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile-xuc](https://clawhub.ai/user/smile-xuc)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to fetch readable markdown and metadata from public URLs for summarization, content analysis, and search-result follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or token-bearing URLs may be sent to Jina's external reader service.

Mitigation: Use the skill for public web pages only; avoid private links, authenticated content, and URLs containing secrets.

Risk: Retrieved page content may be incomplete, blocked, stale, or untrusted.

Mitigation: Validate important outputs against the original source before relying on summaries or downstream analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smile-xuc/skills/haibo-jina-reader)
- [Jina Reader API endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands]

**Output Format:** [Markdown text or JSON with metadata, optionally saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a target URL, output format, timeout, and optional output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
