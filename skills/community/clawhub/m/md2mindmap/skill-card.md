## Description:

Md2mindmap converts Markdown documents into interactive mind maps with HTML output and optional PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukimgit](https://clawhub.ai/user/sukimgit)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, instructors, knowledge workers, writers, and developers use this skill to turn Markdown outlines, lists, and tables into visual mind maps for review, planning, presentations, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML fetches and executes third-party browser code from unpkg.com by default.

Mitigation: Use an isolated environment for conversion, avoid sensitive Markdown unless dependencies are bundled locally or network access is blocked, and review generated HTML before sharing.

Risk: PDF export depends on Playwright and Chromium installed from the local environment.

Mitigation: Install and pin dependencies from trusted sources, keep the browser runtime updated, and run PDF generation with least-privilege file access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukimgit/skills/md2mindmap)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [HTML files and optional PDF files, with concise text status or troubleshooting guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is interactive and uses browser-side Markmap libraries; PDF export requires Playwright and Chromium.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
