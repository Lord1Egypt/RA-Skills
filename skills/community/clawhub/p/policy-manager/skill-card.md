## Description:

POLICY-MANAGER creates, reads, and updates insurance policy JSON files for selected products, uploaded materials, extracted policy data, and completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erveynight](https://clawhub.ai/user/erveynight)

### License/Terms of Use:

MIT-0

## Use Case:

External users and insurance operations teams use this skill to coordinate policy-file creation, uploaded-material tracking, policy data mapping, status updates, and policy reads during an insurance application workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive insurance records may be created, read, or updated without strong file boundaries or implemented authorization checks.

Mitigation: Run the skill in a controlled environment with trusted callers, limited filesystem access, task number validation, authorization checks, update allowlists, schema validation, and safe writes.

Risk: Network and storage behavior is under-disclosed, including optional remote policy-template access through POLICY_API_URL.

Mitigation: Require explicit opt-in and privacy notices for remote policy-template calls, and document where policy records and uploaded-material metadata are stored before using real customer data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erveynight/skills/policy-manager)
- [PolicyDTO field reference](artifact/PolicyDTO字段说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses policy task identifiers, insurance/product codes, uploaded-material metadata, policy data JSON, and status JSON as workflow inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
