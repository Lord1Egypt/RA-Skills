## Description:

A personal brand planning assistant that analyzes a proposed IP across competitor landscape, audience, brand positioning, content strategy, platform strategy, monetization, and risk to produce an interactive HTML decision report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to evaluate and plan a personal brand or creator IP from an initial name and positioning idea. It gathers public web signals, scores seven planning dimensions, and turns the analysis into a standalone HTML report with recommendations and a 12-month roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unnecessary Bash access increases execution risk for a skill whose core workflow is web research and report generation.

Mitigation: Review requested tools before installation and prefer a release that removes Bash unless a concrete command requirement is documented.

Risk: Generated HTML files load remote JavaScript and use filenames derived from user input.

Mitigation: Sanitize output filenames, confine writes to a report directory, and vendor or integrity-pin Chart.js before using generated reports in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/personal-ip-planner)
- [Chart.js 4.4.0 CDN](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, code, guidance, files]

**Output Format:** [Standalone HTML report with embedded CSS and JavaScript, plus concise follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes a radar chart, competitor matrix, seven-dimension scoring, risk analysis, and a 12-month action roadmap.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
