## Description:

Generate structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and incident managers use this skill to draft post-incident reviews from logs, timelines, and incident metadata, including root cause analysis, impact summaries, lessons learned, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can preserve executable markup from incident data or logs.

Mitigation: Use trusted inputs, prefer markdown or JSON output for untrusted incident data, and avoid opening generated HTML reports until user-controlled fields are escaped or sanitized.

## Reference(s):

- [Postmortem Templates & Guidelines](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated reports to stdout or to a requested output file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
