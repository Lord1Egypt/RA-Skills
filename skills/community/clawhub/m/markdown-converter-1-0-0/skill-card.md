## Description:

Convert documents and files to Markdown using markitdown for LLM processing or text analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert common document, data, media, archive, and web inputs into Markdown for LLM processing or text analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to fetch and run the current markitdown package at use time.

Mitigation: For sensitive or controlled workflows, use a pinned and reviewed markitdown version in a restricted environment.

Risk: Optional plugin, URL, audio, and Azure Document Intelligence modes may involve untrusted extensions or external processing.

Mitigation: Use plugins only after review, and treat URL, audio, and Azure-backed conversions as external-processing paths for data-handling decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangyingzhuangk/skills/markdown-converter-1-0-0)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; converted content is Markdown text or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write converted Markdown to stdout or an output file; optional Azure Document Intelligence and plugin modes may change processing behavior.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
