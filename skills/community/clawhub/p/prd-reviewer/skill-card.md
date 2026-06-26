## Description: <br>
Reviews product requirement documents against a 10-point PRD rubric and produces module scores, deductions, and a review conclusion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flamemyself](https://clawhub.ai/user/flamemyself) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, reviewers, and developers use this skill to score PRDs against a structured checklist and generate a review report with module scores, source-grounded deductions, strengths, gaps, and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The example document extraction step can leave PRD text in a local plaintext temporary file. <br>
Mitigation: Use the skill only on PRDs the user is allowed to process, prefer a private temporary path for confidential documents, and delete extracted plaintext after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flamemyself/prd-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown scoring report with optional inline bash extraction command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to PRD content; example extraction writes plaintext to /tmp/prd.txt.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
