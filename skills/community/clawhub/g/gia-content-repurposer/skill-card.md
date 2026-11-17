## Description:

Repurposes long-form content such as blog posts, articles, and transcripts into Twitter/X threads, LinkedIn posts, email newsletters, Instagram captions, and short-form summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, founders, and developers use this skill to turn long-form articles, blog posts, transcripts, files, or pasted text into platform-specific social posts, newsletters, captions, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including internal or private-network URLs if supplied.

Mitigation: Use only public, intended URLs and avoid internal, private-network, or confidential sources.

Risk: Fetched, local, or pasted content may be sent to OpenAI or Anthropic for generation.

Mitigation: Process only public or non-confidential material and confirm provider data-handling requirements before use.

Risk: Generated content is saved locally under an output directory.

Mitigation: Choose an appropriate output location and review generated files before sharing or publishing them.

## Reference(s):

- [Platform Character Limits & Best Practices](artifact/references/platform-guides.md)
- [Content Repurposer Pro on ClawHub](https://clawhub.ai/merjua14/skills/gia-content-repurposer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one output per selected format, including Twitter/X threads, LinkedIn posts, newsletters, Instagram captions, and summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
