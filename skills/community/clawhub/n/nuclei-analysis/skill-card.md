## Description:

Intelligently analyzes Nuclei scan results, prioritizes real bugs, reduces noise, and enriches findings with context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyetnighy](https://clawhub.ai/user/nyetnighy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to convert Nuclei scan output into prioritized Markdown reports that highlight actionable findings, likely false positives, business impact context, and reproduction steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown can contain untrusted scan-derived content when Nuclei input comes from third parties or attacker-controlled targets.

Mitigation: Review generated reports before sharing or rendering them in systems that execute scripts or automatically load remote content.

Risk: The analyzer reads local Nuclei output files and writes Markdown reports to user-selected or default output paths.

Mitigation: Run it only on intended local scan files and check the output path before execution to avoid overwriting important files.

## Reference(s):

- [Nuclei Analysis ClawHub release](https://clawhub.ai/nyetnighy/skills/nuclei-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown report with summary tables, prioritized finding sections, attack scenarios, and reproduction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report files under reports/nuclei-analysis when run without an explicit output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
