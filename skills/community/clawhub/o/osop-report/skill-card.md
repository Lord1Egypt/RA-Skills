## Description:

Convert .osop and .osoplog.yaml into standalone HTML report with dark mode and expandable nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archie0125](https://clawhub.ai/user/archie0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert OSOP workflow definitions and optional execution logs into a local, self-contained HTML report for review and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OSOP workflow and log files that may contain sensitive workflow details.

Mitigation: Run it only on files intended for report generation and review the resulting HTML before sharing it.

Risk: The skill writes a local HTML report file next to the source file or to the requested output path.

Mitigation: Choose an output location appropriate for the report contents and avoid overwriting important local files.

Risk: The release metadata lists ~/.osop/config.yaml as required configuration, which may contain sensitive settings.

Mitigation: Review why that configuration is needed before installation and avoid exposing its contents in generated reports.

## Reference(s):

- [OSOP](https://osop.ai)
- [ClawHub skill page](https://clawhub.ai/archie0125/skills/osop-report)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Self-contained HTML report file plus a short path message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads .osop and optional .osoplog.yaml inputs; writes a local -report.html file.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
