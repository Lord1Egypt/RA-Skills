## Description:

Helps developers inspect installed Huawei Cloud Python SDK packages, client classes, API methods, request parameters, and SDK class details with keyword search and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jupiter-19](https://clawhub.ai/user/jupiter-19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly locate Huawei Cloud Python SDK services, clients, API methods, request parameters, and model class fields while preparing SDK-based automation or integration code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper command can load arbitrary local Python modules from user-provided class values.

Mitigation: Run the skill in a dedicated virtual environment, use trusted and pinned Huawei SDK packages, and avoid passing arbitrary dotted class names from untrusted text.

Risk: SDK lookup results depend on the packages installed in the local Python environment.

Mitigation: Install only the intended Huawei Cloud SDK packages from a trusted index and verify package versions before relying on generated method or parameter guidance.

## Reference(s):

- [Huawei Cloud SDK Python v3](https://github.com/huaweicloud/huaweicloud-sdk-python-v3)
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/apiexplorer/overview)
- [Credential Reference](references/knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on locally installed Huawei Cloud SDK packages and the selected service, client, method, or class query.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
