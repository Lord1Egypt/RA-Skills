## Description:

Convert and publish Markdown articles with AI-assisted writing, formatting, and image generation for WeChat, Zhihu, and Toutiao platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT

## Use Case:

Developers and content publishers use this skill to convert Markdown into platform-ready HTML, create AI-assisted article drafts, generate cover images, and send content to WeChat, Zhihu, or Toutiao draft and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send article content to configured publishing, AI, image-generation, and conversion services.

Mitigation: Use it only with content that may be shared with those services, and review service terms and data handling before using sensitive or unpublished material.

Risk: The skill handles session cookies, API keys, and app secrets for publishing and AI services.

Mitigation: Prefer environment variables or isolated configuration files, avoid passing secrets directly on the command line, use limited-scope accounts where possible, and rotate credentials after testing.

Risk: Publishing workflows may create drafts or publish content on real WeChat, Zhihu, or Toutiao accounts.

Mitigation: Test first with isolated accounts and draft mode, then verify the platform state before running workflows against production accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shixiangyu2/skills/multi-writing-skills-main)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, PDF files, generated images, CLI output, and platform draft or publish results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured AI, image-generation, Markdown-conversion, and publishing services using local credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
