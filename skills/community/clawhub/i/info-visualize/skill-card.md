## Description:

Info Visualize turns structured data into dark-themed SVG/HTML bar charts and PNG long-form reports for dashboards, monitoring summaries, daily reports, and rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[todd-9527](https://clawhub.ai/user/todd-9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to convert structured JSON data into shareable visual outputs such as ranking charts, monitoring reports, KPI summaries, and long-form information graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML/SVG chart output can include unescaped input data when rendering untrusted JSON.

Mitigation: Render trusted data only, or review and sanitize JSON before publishing generated HTML/SVG; prefer PNG output for untrusted data.

Risk: The PNG report path depends on Pillow and can optionally copy reports to an archive directory.

Mitigation: Pin Pillow in a virtual environment and use the archive option only for destinations where generated reports are intentionally retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/todd-9527/skills/info-visualize)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [HTML/SVG chart files and PNG report files, with Markdown guidance and Python or shell invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts structured JSON input; SVG/HTML output is browser-viewable and PNG output requires Pillow.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
