## Description: <br>
Generates management-readable insight briefs from reports and charts, separating findings, interpretation, recommended actions, data gaps, and risk alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operators, and managers use this skill to turn chart conclusions, data summaries, and context into reviewable Markdown briefs for weekly updates, business analysis, and report summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated brief may contain incorrect, overstated, or decision-impacting interpretations. <br>
Mitigation: Review generated briefs before using them for business decisions, and preserve the skill's distinction between facts, inferences, and recommended actions. <br>
Risk: The local script reads provided files and can create or overwrite the selected output file. <br>
Mitigation: Provide only files intended for processing and choose the output path carefully; use dry-run or stdout when reviewing behavior. <br>
Risk: Sensitive or personal data in reports may be included in generated summaries. <br>
Mitigation: Desensitize sensitive inputs before processing and keep generated briefs within the intended review workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/insight-brief-generator) <br>
- [README.md](README.md) <br>
- [resources/spec.json](resources/spec.json) <br>
- [resources/template.md](resources/template.md) <br>
- [examples/example-input.md](examples/example-input.md) <br>
- [examples/example-output.md](examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown briefs; optional JSON when the local script is run with JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write to stdout or a chosen output file; uses local input files and does not fetch facts from the network.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
