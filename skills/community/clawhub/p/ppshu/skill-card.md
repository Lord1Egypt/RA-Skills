## Description:

Ppshu Github helps agents create self-contained local HTML visualizations, interactive prototypes, flowcharts, and diff reports, saved in a .ppshu gallery for preview and reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppshux](https://clawhub.ai/user/ppshux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and technical users use this skill when they want an agent to turn concepts, flows, architecture, charts, UI ideas, or file comparisons into local interactive HTML artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local HTML artifacts into the current project.

Mitigation: Use a dedicated output directory when possible and review generated files before keeping or sharing them.

Risk: Generated reports and galleries are active local web pages and may carry injection risk when built from untrusted inputs.

Mitigation: Avoid opening reports made from untrusted files, and prefer a patched version that escapes embedded JSON and gallery href attributes.

Risk: Mermaid rendering uses permissive security settings in the bundled flowchart template.

Mitigation: Review Mermaid content before opening generated pages and prefer stricter Mermaid security settings for untrusted diagrams.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppshux/skills/ppshu)
- [README](artifact/README.md)
- [HTML cookbook](artifact/references/html_cookbook.md)
- [Mermaid flowchart template](artifact/references/mermaid_flowchart_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML, SVG, Canvas, JavaScript, and Mermaid artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML files are saved under the current project's .ppshu directory with numbered filenames and an index gallery.]

## Skill Version(s):

1.5.0 (source: server release metadata and artifact manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
