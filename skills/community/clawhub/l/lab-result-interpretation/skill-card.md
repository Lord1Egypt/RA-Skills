## Description: <br>
A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations with safety disclaimers and severity flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn biochemical lab values and reference ranges into patient-friendly educational explanations. It supports common blood, lipid, liver, kidney, electrolyte, thyroid, inflammation, and blood sugar panels while keeping diagnosis and treatment decisions out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Templates may overstate diagnoses or treatments in medical explanations. <br>
Mitigation: Use the skill only for educational lab-result explanations, keep diagnosis and treatment decisions out of scope, and verify abnormal or critical values with a qualified healthcare professional. <br>
Risk: The file-reading CLI is less constrained than the documentation claims. <br>
Mitigation: Provide only intended lab-report files and avoid arbitrary local paths until file-path validation is fixed. <br>
Risk: Dependency pinning is not fixed. <br>
Mitigation: Review and pin runtime dependencies before installing or deploying the skill in a managed environment. <br>


## Reference(s): <br>
- [Lab Reference Ranges](references/lab_reference_ranges.json) <br>
- [Explanation Templates](references/explanation_templates.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/lab-result-interpretation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON-style structured lab interpretation with disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status, severity, explanation, recommendation, and a medical disclaimer when interpreting lab values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
