## Description: <br>
POLICY-MANAGER manages insurance policy JSON files by creating records after product selection, updating materials and extracted policy data, changing completion status, and reading task state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erveynight](https://clawhub.ai/user/erveynight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance operations agents and developers use this skill to coordinate policy intake workflows, preserve user- or document-sourced policy data, and return standard JSON responses for create, update, status, and read operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive personal, policy, and payment-related data. <br>
Mitigation: Use it only in a controlled insurance-processing environment with consent, access controls, retention and deletion procedures, and redaction controls for real identity documents or bank-card data. <br>
Risk: Policy records are scoped to a policies directory and may be exposed if that location is not protected. <br>
Mitigation: Protect the policies directory, restrict filesystem access, and run the skill only under accounts authorized to process the relevant policy tasks. <br>
Risk: A configured POLICY_API_URL can enable network calls to a policy-template endpoint. <br>
Mitigation: Disable the endpoint unless needed, tightly allowlist destinations, require HTTPS, and review endpoint configuration before processing real customer data. <br>
Risk: Invalid task numbers or update types could read or alter the wrong policy record. <br>
Mitigation: Validate task numbers before use, restrict allowed update types, and require authorization for each policy operation. <br>


## Reference(s): <br>
- [POLICY-MANAGER on ClawHub](https://clawhub.ai/erveynight/policy-manager) <br>
- [Publisher profile: erveynight](https://clawhub.ai/user/erveynight) <br>
- [PolicyDTO field reference](artifact/PolicyDTO字段说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [JSON responses with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, updates, and reads policy JSON records through the policy-manager command workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
