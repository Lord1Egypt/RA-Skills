## Description:

Use when creating forest plots for meta-analyses, visualizing effect sizes across studies, or generating publication-ready meta-analysis figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to generate publication-ready meta-analysis forest plots with confidence intervals, heterogeneity metrics, and fixed-effect or random-effects summaries from CSV or JSON study data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned scientific Python dependencies may change behavior across installations or introduce dependency risk.

Mitigation: Install with a locked dependency set for numpy, scipy, matplotlib, and pandas before operational use.

Risk: README-style examples reference a script or module name that differs from the shipped artifact.

Mitigation: Run artifact/scripts/main.py directly or update imports and command examples to match the installed file layout.

Risk: Statistical conclusions depend on user-provided study data and the script's model assumptions.

Mitigation: Review input data, confidence intervals, and fixed-effect or random-effects model selection before using generated plots in publications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/meta-analysis-forest-plotter)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts may include PNG, PDF, SVG, or TIFF forest plots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads CSV or JSON study data and can emit console summaries alongside plot files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
