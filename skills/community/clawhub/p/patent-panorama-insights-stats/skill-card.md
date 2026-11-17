## Description:

Generates patent panorama statistics, branch-organized core patent indexes, value-signal files, chart data, and a self-contained statistics dashboard from validated Patent Panorama search outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts and agents use this skill after the Patent Panorama search step to aggregate landscape statistics, applicant and technology views, branch-level core patent indexes, and value signals for downstream tagging and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an unpinned executable package and mutable GitHub branch.

Mitigation: Review or replace the install path before deployment; prefer a pinned skills package version and an immutable commit or signed release.

Risk: The skill depends on authorized PatSnap MCP services and writes local patent-analysis output files.

Mitigation: Confirm the agent environment is authorized for the required PatSnap MCP services and review generated local files before using them in downstream tagging or reporting.

Risk: Patent value, legal-status, family-breadth, and citation signals can be mistaken for legal conclusions.

Mitigation: Treat these outputs as analysis signals only and require legal or domain review before relying on them for FTO, infringement, SEP, validity, novelty, or inventiveness decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-panorama-insights-stats)
- [Open Platform marketplace listing](https://open.zhihuiya.com/marketplace/skill-hub/patent-panorama-insights-stats)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, CSV, HTML, and manifest file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces panorama_stats.json, assignee_normalization.json, patent_index.core.json/.csv, value_signals.json, chart_data.json, panorama_stats_report.html, and an extended report_manifest.json when required inputs and authorized MCP services are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
