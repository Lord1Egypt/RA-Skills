## Description: <br>
Queries Huawei Cloud identity and access management resources (IAM) via read-only Python SDK, including users, groups, policies, agencies, AK/SK, MFA devices, login and password policies, security compliance, and account quotas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to query Huawei Cloud IAM identity, permission, credential-status, MFA, security-policy, compliance, and quota data without creating, modifying, or deleting resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Huawei Cloud IAM read access and can print IAM user, policy, MFA, and access-key metadata. <br>
Mitigation: Use temporary, least-privilege credentials and treat all query output as sensitive. <br>
Risk: The setup path creates a virtual environment and installs packages, while security evidence calls out TLS verification and dependency pinning for manual review. <br>
Mitigation: Review the setup path before installation and use controlled hosts until dependency pinning and TLS verification are acceptable for the environment. <br>


## Reference(s): <br>
- [IAM Python Script Usage Guide](artifact/references/iam/guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/huawei-cloud-iam-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON query results from the packaged scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query outputs may include sensitive IAM metadata and should be handled as confidential.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
