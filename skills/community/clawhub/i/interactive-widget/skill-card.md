## Description:

Create shareable interactive web pages for dashboards, charts, forms, simulations, and other browser-based UI through the duoduo-widget CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuaner](https://clawhub.ai/user/kuaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a response needs a durable, shareable browser interface, such as a dashboard, form, chart, visualization, sortable table, Canvas animation, or parameter picker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Widget content and form submissions may be sent to a persistent remote service and become durable or shareable.

Mitigation: Avoid secrets, credentials, regulated personal data, and confidential business records unless access controls and retention have been separately verified.

Risk: Untrusted text inserted into generated HTML can create unsafe or misleading widget content.

Mitigation: Escape untrusted text before inserting it into HTML and review generated widgets before sharing or finalizing them.

Risk: Mutable third-party CDN scripts can change after a widget is created.

Mitigation: Avoid mutable CDN dependencies for sensitive pages or pin and review external script sources before use.

## Reference(s):

- [Interactive Widget ClawHub release](https://clawhub.ai/kuaner/skills/interactive-widget)
- [Widget HTML Templates](artifact/references/html_patterns.md)
- [Default widget service endpoint](https://aidgets.dev)
- [Chart.js browser bundle example](https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON patch examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable, shareable widget URLs and can request structured user submissions through the widget service.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
