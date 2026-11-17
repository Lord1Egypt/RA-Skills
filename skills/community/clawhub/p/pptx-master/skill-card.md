## Description:

Pptx Master is an AI-assisted presentation workflow that converts PDF, DOCX, URL, Markdown, and other source content into editable PPTX decks using SVG page generation, templates, quality checks, and export tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and presentation creators use this skill to turn documents, web pages, Markdown, or topic briefs into professional editable slide decks for financial analysis, technical reports, business presentations, and similar communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact update behavior may change local code or dependencies.

Mitigation: Inspect update changes before running scripts/update_repo.py, prefer the --skip-pip option, and use the skill in a contained project environment.

Risk: Network conversion and image-provider features may send content or credentials to external services.

Mitigation: Use scoped, low-quota API keys; avoid untrusted custom provider base URLs; and do not process sensitive web pages unless the environment and endpoint are trusted.

Risk: One web conversion path disables certificate verification for sensitive HTTPS pages.

Mitigation: Avoid converting sensitive HTTPS content with that path unless the source and network environment have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/pptx-master)
- [PPT Master Skill Definition](SKILL.md)
- [PPT Master Toolset](scripts/README.md)
- [Strategist Role](references/strategist.md)
- [Executor Base Role](references/executor-base.md)
- [Image Generator Role](references/image-generator.md)
- [Template Designer Role](references/template-designer.md)
- [SVG Best Practices](SVG_BEST_PRACTICES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated SVG/PPTX workflow files, and configuration-oriented project artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project directories, converted Markdown sources, SVG slides, images, speaker notes, and PPTX exports during normal use.]

## Skill Version(s):

1.2.3 (source: server release evidence and CHANGELOG, released 2026-05-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
