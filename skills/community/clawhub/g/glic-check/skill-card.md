## Description:

Systematic quality check for code, skills, configurations, and documents using GLIC or UGLIC review dimensions with cited findings and severity tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and skill authors use this agent skill to run structured GLIC or UGLIC reviews over scoped code, skill, configuration, or documentation changes. It produces cited quality findings with ERR, WARN, and INFO severity labels before asking whether fixes should be applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-scoped files and may surface suggested fixes or review conclusions that are incomplete or incorrect.

Mitigation: Use explicit review targets and inspect findings or proposed fixes before approving changes.

Risk: The optional pre-scan helper surfaces likely patterns rather than final findings.

Mitigation: Treat helper output as review input and rely on the full GLIC or UGLIC checklist with cited locations for final severity decisions.

## Reference(s):

- [GLIC / UGLIC Dimension Checklists](artifact/references/dimensions.md)
- [GLIC / UGLIC Report Format](artifact/references/output-format.md)
- [GLIC / UGLIC Check Examples](artifact/references/examples.md)
- [build-better-skills repository](https://github.com/Songhonglei/build-better-skills)
- [build-better-skills stages](https://github.com/Songhonglei/build-better-skills#stages)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown report with cited findings, severity tags, a summary table, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite file or section locations, separate must-fix from should-fix items, and ask for approval before applying fixes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
