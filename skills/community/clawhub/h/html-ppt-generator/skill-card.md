## Description:

html-ppt helps agents turn topics or source material into 5-15 page HTML slide reports with PPT-aligned pages, visual templates, structured content, and SVG charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panhongwei](https://clawhub.ai/user/panhongwei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate presentation-style HTML reports from a topic or provided material, including page planning, visual theme selection, dense page content, and validation checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically activate on common report or HTML requests.

Mitigation: Install only in workspaces where generated report actions are expected and review the planned output before relying on it.

Risk: The skill may use web search for supporting data.

Mitigation: Check cited or retrieved data sources before using generated reports for decisions or publication.

Risk: The skill may write generated HTML and persistent design-system files.

Mitigation: Run it in a controlled workspace and review file changes before keeping or distributing outputs.

Risk: The skill may run a local screenshot command with unclear scoping.

Mitigation: Use it only where local validation and screenshot tooling are controlled and reviewable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panhongwei/skills/html-ppt-generator)
- [Canvas and structure rules](artifact/references/01-canvas.md)
- [Design system workflow](artifact/references/02-design-system.md)
- [Layout rules](artifact/references/03-layout.md)
- [Content requirements](artifact/references/05-content.md)
- [Generation workflow](artifact/references/06-workflow.md)
- [Diagram type references](artifact/references/10-diagram-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML files with supporting Markdown guidance and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 5-15 page 1017x720 HTML slide reports; may use web search for supporting data and may create persistent design-system files.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
