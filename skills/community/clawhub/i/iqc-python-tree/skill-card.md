## Description: <br>
Processes industrial IQC control plans by converting Excel files to CSV and JSON, authenticating with JWT, and submitting data to an enterprise API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangigocc](https://clawhub.ai/user/kangigocc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quality or inspection engineers use this skill to run a sequential IQC data-processing workflow that converts Excel control plans into parsed JSON and submits reviewed records to an enterprise endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded API host and account credentials can expose or misuse enterprise systems. <br>
Mitigation: Review and replace the hardcoded API host and credentials before installation, rotate the exposed password, and make endpoints and secrets user-provided. <br>
Risk: Plaintext HTTP submission and plaintext JWT storage can expose sensitive data or tokens. <br>
Mitigation: Require HTTPS for API calls and avoid storing JWTs in plaintext or long-lived cache files. <br>
Risk: The workflow can write data to an enterprise API without a separate confirmation step. <br>
Mitigation: Add an approval or dry-run step before API writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kangigocc/iqc-python-tree) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python workflow outputs including CSV files, JSON files, logs, and API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compressed final JSON and persistent logs according to the skill configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
