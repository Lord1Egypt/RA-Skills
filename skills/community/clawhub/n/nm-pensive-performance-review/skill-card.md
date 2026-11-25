## Description:

Detects time and space complexity hotspots via AST scan

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before performance-sensitive merges or when investigating code that feels slow. It scans source for likely time and space complexity hotspots and returns findings with severity and suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because its reported behaviors do not fully match its stated static complexity analysis purpose, and it instructs users to run project benchmarks and install a third-party tool.

Mitigation: Consider the security verdict carefully and inspect benchmark and installation commands before running them.

Risk: The security scan was partial: referenced paths were missing, so its evidence is incomplete.

Mitigation: Review the complete release contents and any referenced files before relying on the scan or using the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-performance-review)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [kuva visualization project](https://github.com/Psy-Fer/kuva)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown performance review with severity-ranked findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python AST analysis is always available; multi-language and call-graph analysis require optional integrations.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
