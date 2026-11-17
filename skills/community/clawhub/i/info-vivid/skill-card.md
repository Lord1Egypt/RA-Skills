## Description:

Info Vivid renders structured data into dark-themed visual outputs, including browser-openable SVG/HTML horizontal bar charts and Pillow-based PNG long-form reports with KPI cards, text sections, tables, bar charts, cards, timelines, and footers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[todd-9527](https://clawhub.ai/user/todd-9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to turn structured chart and report data into presentation-ready rankings, monitoring reports, daily reports, and infographic-style summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML chart output generated from untrusted JSON can become executable browser content.

Mitigation: Use only trusted chart and report data until SVG/HTML escaping and color validation are fixed, and avoid opening or publishing generated HTML from untrusted JSON.

Risk: PNG report rendering depends on Pillow and processes user-provided report data.

Mitigation: Pin Pillow in an isolated environment for PNG rendering.

Risk: Generated outputs include WorkBuddy branding and may be copied to an archive path when requested.

Mitigation: Review generated files and archive destinations before sharing outputs or using the archive option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/todd-9527/skills/info-vivid)
- [Screenshot: SVG chart example](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-01-svg-chart.png)
- [Screenshot: longform report example](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-02-longform-report.png)
- [Screenshot: JSON to output example](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-03-json-to-output.png)

## Skill Output:

**Output Type(s):** [files, code, shell commands, configuration, guidance]

**Output Format:** [JSON-driven HTML/SVG chart files and PNG image reports, with Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SVG/HTML chart generation uses the Python standard library; PNG longform reports require Pillow; outputs include WorkBuddy branding and can optionally be copied to an archive path.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
