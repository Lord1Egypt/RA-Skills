## Description:

中文去AI味 Pro helps an agent turn mechanical AI-generated Chinese text into more natural, human-facing prose across Zhihu, Xiaohongshu, WeChat public account, WeChat Moments, and casual styles, with AI-taste scoring and reusable style guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaryn-hs](https://clawhub.ai/user/aaryn-hs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, editors, and writing assistants use this skill to assess Chinese drafts for AI-like writing patterns and generate prompts or guidance for rewriting those drafts in platform-specific Chinese styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A style option can read unintended Markdown files from the user's machine.

Mitigation: Use only the documented style names and do not pass style values from untrusted input.

Risk: Private or sensitive draft text may be included in generated prompts that a user sends to another AI system.

Mitigation: Prefer stdout for sensitive text, review generated prompts before external use, and remove confidential content before publishing or sharing outputs.

Risk: Humanized text may preserve inaccurate, misleading, or inappropriate source content while making it sound more natural.

Mitigation: Review rewritten content for factual accuracy, tone, and publication suitability before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaryn-hs/skills/humanize-zh-pro)
- [Homepage](https://github.com/renyetu/humanize-zh-pro)
- [中文去AI味 - 深度风格指南](references/style-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and plain text, including generated rewrite prompts, AI-taste analysis, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports five documented Chinese writing styles and optional file output from the bundled shell script.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
