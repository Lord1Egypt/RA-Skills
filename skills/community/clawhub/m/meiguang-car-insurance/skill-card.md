## Description: <br>
Extracts structured fields from car-insurance PDFs for supported Chinese insurers and writes the results to an Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cc19960203cc](https://clawhub.ai/user/cc19960203cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and agents use this skill to extract policy, vehicle, insured-person, premium, tax, and coverage-start data from car-insurance PDFs into a spreadsheet for review and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The source PDFs and generated Excel workbook can contain sensitive insurance, vehicle, and personal data. <br>
Mitigation: Run the skill only when authorized, store inputs and outputs in access-controlled locations, and delete generated files when they are no longer needed. <br>
Risk: Filename fallback and same-car field completion can misattribute extracted fields. <br>
Mitigation: Review the workbook before using it for business decisions or record updates. <br>
Risk: Optimization scripts modify the local extractor code. <br>
Mitigation: Run optimize_patch.py or optimize_v2.py only after reviewing the changes and confirming that code modification is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cc19960203cc/meiguang-car-insurance) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and Python configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The described extractor produces a local Excel workbook from local PDF inputs.] <br>

## Skill Version(s): <br>
5.7.5 (source: release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
