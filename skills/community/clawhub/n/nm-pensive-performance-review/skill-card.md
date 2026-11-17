## Description:

Detects time and space complexity hotspots via AST scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to review code for likely time and space complexity hotspots before performance-sensitive merges or when investigating code that feels slow. It returns severity-ranked findings and suggestions for further verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious with medium confidence, citing a mismatch between its code-analysis purpose and some described capabilities.

Mitigation: Review the full skill and its execution steps, and confirm its described behavior matches your intended use before installing.

Risk: The workflow instructs users to run project code and install a visualization tool, and the scanner assessment is incomplete because linked local references were missing.

Mitigation: Use it with trusted project files, inspect commands and dependencies before running them, and review the missing references before relying on the assessment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-pensive-performance-review)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [Kuva visualization project](https://github.com/Psy-Fer/kuva)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown performance review with severity-ranked findings and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include file and line locations, severity, category, and suggested actions; tier coverage may be reported.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
