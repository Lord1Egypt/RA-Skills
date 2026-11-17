## Description:

Her-Agent development dashboard that displays self-awareness, emotional state, knowledge graph, learning progress, and evolution status in a local web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenqin1688](https://clawhub.ai/user/wenqin1688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to view a local Her-Agent progress dashboard for learning notes, diary-derived reflections, knowledge-map status, emotional state, and evolution progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the dashboard for live agent telemetry even though the evidence describes it as mostly a static or local snapshot.

Mitigation: Present the dashboard as a local status view and validate important status claims against the underlying OpenClaw workspace files.

Risk: The updater reads local diary and learning-note markdown paths from the OpenClaw workspace.

Mitigation: Review the local files read by the updater before use and avoid placing sensitive content in those paths unless it is intended for dashboard display.

Risk: The dashboard loads D3 from an external CDN.

Mitigation: Vendor or integrity-pin the D3 dependency before deployment in controlled or higher-trust environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenqin1688/skills/her-agent-dashboard)
- [Publisher profile](https://clawhub.ai/user/wenqin1688)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance plus local HTML dashboard files and Python-generated status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard is Chinese-language and local to the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
