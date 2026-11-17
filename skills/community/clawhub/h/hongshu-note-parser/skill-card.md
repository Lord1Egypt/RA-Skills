## Description:

Parses a user-provided Xiaohongshu note link to collect the note title, text, images, tags, and engagement data, then helps an agent produce a structured brand-analysis JSON and a self-contained interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and brand-content teams use this skill to inspect Xiaohongshu posts supplied by a user, capture note data and images, and turn agent analysis into reusable visual-strategy reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML generator can embed local file bytes when image references in the analysis JSON point to local paths.

Mitigation: Use only trusted analysis JSON created during the current workflow, constrain readable paths to approved image/output directories, and review generated HTML before sharing.

Risk: The HTML generator can fetch remote image URLs supplied through the analysis JSON.

Mitigation: Run with constrained network access and enforce approved HTTPS hosts, redirect checks, MIME or signature validation, and response size limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/hongshu-note-parser)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [skill.yaml](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [JSON, HTML, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands, structured JSON, and generated self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report can embed downloaded or local images as base64 data and writes collection data, images, and HTML into the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
