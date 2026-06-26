## Description: <br>
印度占星（Jyotish）专业解盘与推运系统，支持出生信息、PDF or text chart input, chart analysis, Dasha and transit timing, birth-time rectification, compatibility analysis, Prashna, and HTML report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[732642856](https://clawhub.ai/user/732642856) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and practitioners use this skill to generate structured Jyotish chart readings, timing analysis, relationship analysis, birth-time rectification, and report output from birth data or chart documents. Developers may also use its Python CLI commands for astrology calculations and validation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store and reuse personal chart details and interaction history locally. <br>
Mitigation: Avoid providing unnecessary personal data, run in a controlled environment, and disable or remove the Hermes memory and learning components before routine use. <br>
Risk: Runtime package installation and broad web lookups can increase execution and data-exposure risk. <br>
Mitigation: Review commands before execution, pin and install dependencies separately, and restrict network access to sources needed for the specific reading. <br>
Risk: Maintainer-style GitHub push instructions and auto-generated skill behavior go beyond ordinary chart reading. <br>
Mitigation: Do not run repository-push or generated-skill workflows unless intentionally maintaining the project, and review generated files before use. <br>
Risk: Astrology interpretations and predictions may be incorrect, culturally variable, or overconfident. <br>
Mitigation: Use the bundled external verification gates and confidence labels, and present readings as interpretive guidance rather than factual certainty. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/732642856/jyotish-vedic-astrology) <br>
- [README](artifact/README.md) <br>
- [Quick reference guide](artifact/references/quick-reference-guide.md) <br>
- [AI reading workflow prompt](artifact/references/ai-reading-workflow-prompt.md) <br>
- [Mandatory verification gate protocol](artifact/references/mandatory-verification-gate-protocol.md) <br>
- [Prediction boundary protocol](artifact/references/prediction-boundary-protocol.md) <br>
- [PDF chart reading guide](artifact/references/pdf-chart-reading-guide.md) <br>
- [Transit actionable output guide](artifact/references/transit-actionable-output-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples; Python CLI outputs may include JSON, Markdown, or HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request personal birth data, chart files, dates, locations, event history, and user intent before producing readings or timing windows.] <br>

## Skill Version(s): <br>
6.0.1 (source: server release evidence; artifact frontmatter says 6.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
