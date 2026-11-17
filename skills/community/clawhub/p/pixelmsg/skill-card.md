## Description:

pixelmsg renders HTML templates into pixel-perfect PNG image cards with Playwright so agents can deliver rich visual messages instead of plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarence-g](https://clawhub.ai/user/clarence-g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use pixelmsg to convert structured response content into styled HTML cards and render them as PNG images for chat, reports, dashboards, notifications, and data summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Templates can load mutable third-party CDN code during rendering.

Mitigation: Review template dependencies before use, vendor required resources locally where practical, or render with network egress blocked or allowlisted.

Risk: Active HTML rendering with unrestricted network access may expose sensitive, private, or attacker-supplied content.

Mitigation: Avoid rendering sensitive or untrusted content until network access is constrained and templates have been reviewed.

Risk: Generated image paths and workspace writes can collide or modify the installed skill directory if reused carelessly.

Mitigation: Use unique workspace output filenames and keep generated templates and screenshots in the project workspace rather than editing the installed skill package.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/clarence-g/skills/pixelmsg)
- [README](README.md)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with an absolute output path and optional standalone MEDIA delivery line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright screenshots of the #app element; supports viewport, selector, output directory, filename, URL parameter, full-page, and device-scale options.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
