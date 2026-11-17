## Description:

An 8-step SEO content production workflow for newsletters and blogs that coordinates SERP analysis, outlining, drafting, AI-pattern screening, quality checks, SEO validation, formatting, and paste-ready publishing output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micphigoo](https://clawhub.ai/user/micphigoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and newsletter publishers use this skill to produce long-form newsletter or blog articles from a project slug, primary keyword, publish date, and article path. It guides the agent through SEO research, drafting, validation, formatting, and creation of a paste-ready publishing document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated article content, SEO metadata, or source claims may be inaccurate, incomplete, or unsuitable for publication.

Mitigation: Review the final article and paste-ready Markdown manually, and enforce the skill's quality, source integrity, SEO validation, and AI-pattern checks before publishing.

Risk: The workflow reads project files and writes a paste-ready Markdown output in the user's workspace.

Mitigation: Run it only in the intended project with an explicit project slug, article path, keyword, and publish date, then inspect the generated file before using it in a publishing platform.

## Reference(s):

- [Writing Style Guide](references/writing-style.md)
- [ClawHub Skill Page](https://clawhub.ai/micphigoo/skills/newsletter-seo-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated article and paste-ready Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project slug, primary keyword, publish date, and article path; reports quality gate, SEO validation, and AI-pattern screening results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
