## Description: <br>
Compares proposal documents and produces structured differences, hidden costs, risks, and recommendations for decision workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to compare proposal, procurement, or technical selection options against stated constraints and evaluation criteria. It helps produce reviewable Markdown that separates facts from inferred recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposal comparisons may include incorrect, incomplete, or sensitive information if the input material is flawed or confidential. <br>
Mitigation: Use only proposal files intended for processing, review the generated report before sharing or acting on it, and redact sensitive material when appropriate. <br>
Risk: Recommendations can be mistaken for objective facts when they are based on limited proposal evidence. <br>
Mitigation: Keep factual comparisons separate from inferred advice and list missing information as items to confirm. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/proposal-comparator) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>
- [examples/example-output.md](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report; may include a local python3 command when execution is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports are intended to be reviewed before sharing or acting on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
