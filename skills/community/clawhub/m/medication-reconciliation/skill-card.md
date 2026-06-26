## Description: <br>
Compare patient pre-admission medication lists with inpatient orders to automatically identify omitted or duplicated medications and improve medication safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical staff, pharmacists, and care-team reviewers use this skill to compare structured pre-admission medication lists against inpatient orders and produce reconciliation reports that flag omissions, duplicates, dose changes, and critical medication warnings. It supports review workflows and does not replace qualified clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medication and patient-context data that may be PHI. <br>
Mitigation: Use only de-identified or authorized inputs, follow organizational privacy rules, and treat generated reports as sensitive clinical data. <br>
Risk: Generated reconciliation findings can be incomplete or clinically inappropriate if used as final care decisions. <br>
Mitigation: Require qualified pharmacist, physician, or clinical staff review before any medication decision. <br>
Risk: Reports written to shared or insecure folders could expose sensitive medication information. <br>
Mitigation: Write outputs only to approved local or controlled storage locations. <br>
Risk: Critical drug-class matching uses a hardcoded list and may not fit every clinical context. <br>
Mitigation: Review critical warnings manually and adapt the workflow or configuration before use in specialized settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/medication-reconciliation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON reconciliation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured report sections include continued, discontinued, new medications, duplicates, warnings, and documented dose-change handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
