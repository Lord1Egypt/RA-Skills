## Description:

Generate structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata, including root cause analysis, impact assessment, timeline reconstruction, lessons learned, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and incident response teams use this skill to draft post-incident reviews from logs, timeline JSON, and incident metadata, then refine the output into a blame-free report. It can also check existing reports for blameful language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports can execute script hidden in incident data or logs.

Mitigation: Use trusted inputs for HTML reports, or prefer Markdown and JSON output for untrusted logs and incident JSON until HTML escaping or sanitization is added.

## Reference(s):

- [Postmortem Templates & Guidelines](artifact/references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/incident-postmortem-generator)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, guidance]

**Output Format:** [Markdown, HTML, JSON, or plain text from a Python command-line generator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a file path or print to stdout; P0/P1 incidents and parsed fatal or error log events influence process exit codes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
