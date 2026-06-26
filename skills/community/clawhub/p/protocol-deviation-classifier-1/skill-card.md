## Description: <br>
Determines whether a clinical trial incident is a major, critical, or minor protocol deviation and explains the supporting risk factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical operations, quality assurance, and trial documentation teams use this skill to triage protocol deviation descriptions, classify likely severity, and prepare structured rationale for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce high-stakes clinical trial classifications and recommended actions. <br>
Mitigation: Require review by qualified clinical quality, regulatory, or legal staff under the organization's SOPs before decisions are acted on. <br>
Risk: Input records may contain sensitive clinical trial or subject information. <br>
Mitigation: Use deidentified data whenever possible and avoid sharing unnecessary subject, site, or investigator details. <br>
Risk: requirements.txt lists standard-library modules that do not need installation on modern Python. <br>
Mitigation: Run the packaged script in a sandboxed local environment and avoid unnecessary pip installs unless your environment specifically requires them. <br>


## Reference(s): <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/protocol-deviation-classifier-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON classification results, and shell commands for local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include classification, confidence, rationale, risk factors, regulatory basis, and recommended actions when sufficient input is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
