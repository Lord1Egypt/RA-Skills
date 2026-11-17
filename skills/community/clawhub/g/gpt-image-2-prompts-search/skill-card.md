## Description:

Recommends relevant GPT Image 2 image-generation prompts from a curated prompt library and helps adapt selected prompts to the user's content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, and developers use this skill to find image-generation prompt templates, preview sample-image-backed options, and customize prompts for articles, videos, products, social posts, and other visual content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-fetches mutable prompt reference data from GitHub and can update local files silently.

Mitigation: Install only when the publisher is trusted, run in a sandbox where possible, and prefer pinned or verified reference data for higher-assurance use.

Risk: The skill instructs agents to execute shell commands that download media from remote image URLs.

Mitigation: Review generated shell commands before execution and avoid shell-based downloads from untrusted or unexpected URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/gpt-image-2-prompts-search)
- [YouMind GPT Image 2 Prompt Gallery](https://youmind.com/gpt-image-2-prompts)
- [Prompt Reference Data](https://github.com/YouMind-OpenLab/gpt-image-2-prompts-search/tree/main/references)
- [awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with prompt previews, links, sample image references, and optional shell commands for local image handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to three matching prompt recommendations, includes sample images when available, and can produce a customized English prompt after the user selects a template.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
