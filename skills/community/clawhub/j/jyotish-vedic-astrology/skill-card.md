## Description:

印度占星专业解盘系统 guides agents through Jyotish chart calculation, PDF chart interpretation, dasha and transit timing, compatibility analysis, birth-time rectification, and report generation using bundled references and Python tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[732642856](https://clawhub.ai/user/732642856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, astrologers, and agent operators use this skill to produce structured Jyotish readings from birth data, PDF or text charts, or uncertain birth times. It supports calculations, interpretive workflows, timing analysis, compatibility review, Prashna, and HTML-style report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and bridge components may store conversation data or task history across sessions.

Mitigation: Review or disable the Hermes memory and bridge components before installation when persistence is not desired.

Risk: Generated memories and generated skills may introduce unreviewed behavior.

Mitigation: Treat generated memories and generated skills as untrusted user data until manually reviewed.

Risk: Setup and workflow guidance may encourage risky repository or dependency practices.

Mitigation: Avoid direct pushes to a main branch and install dependencies in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/732642856/skills/jyotish-vedic-astrology)
- [README](artifact/README.md)
- [Quick reference guide](artifact/references/quick-reference-guide.md)
- [AI reading workflow prompt](artifact/references/ai-reading-workflow-prompt.md)
- [Mandatory verification gate protocol](artifact/references/mandatory-verification-gate-protocol.md)
- [Prediction boundary protocol](artifact/references/prediction-boundary-protocol.md)
- [PDF chart reading guide](artifact/references/pdf-chart-reading-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text guidance with JSON-like calculation output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled Python scripts, templates, and local reference files for chart calculation, validation, and report generation.]

## Skill Version(s):

6.0.1 (source: server release metadata; artifact frontmatter states 6.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
