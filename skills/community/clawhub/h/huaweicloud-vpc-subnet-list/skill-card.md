## Description:

Queries the subnet list for a specified Huawei Cloud VPC in a selected Region and returns a concise list of subnet names and IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inventory Huawei Cloud network resources and inspect the subnets under a specific VPC before follow-on automation or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted region value can influence the Huawei Cloud endpoint host used for signed requests.

Mitigation: Use only trusted config files and region overrides; fix region validation before automated or shared use.

Risk: Huawei Cloud AK/SK credentials are required for execution.

Mitigation: Store credentials only in the ignored local config.json and restrict them to the documented read-only IAM permissions.

## Reference(s):

- [IAM permission statement](iam-policies.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with concise Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local config.json with Huawei Cloud AK/SK credentials, region, and optional project_id.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
