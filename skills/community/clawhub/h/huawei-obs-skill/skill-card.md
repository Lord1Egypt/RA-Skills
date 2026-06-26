## Description: <br>
Guides agents through Huawei Cloud OBS Python SDK setup and common object storage tasks, including client initialization, uploads, downloads, bucket management, object management, and security practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IdiosyncraticDragon](https://clawhub.ai/user/IdiosyncraticDragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure the Huawei Cloud OBS Python SDK and draft code for object storage workflows such as upload, download, listing, bucket permissions, lifecycle rules, and encryption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud storage examples can expose or delete data if used with broad credentials or without review. <br>
Mitigation: Use least-privilege OBS credentials, review examples before execution, and add explicit confirmation plus list-before-delete checks before deletion. <br>
Risk: Public-read ACL examples can make bucket contents accessible to unintended users. <br>
Mitigation: Use public-read settings only for buckets intentionally designed to be public, and prefer private access with scoped temporary access mechanisms. <br>
Risk: Lifecycle rules can transition or delete stored objects in ways that conflict with retention or backup requirements. <br>
Mitigation: Validate lifecycle policies against retention, compliance, and backup requirements before applying them. <br>


## Reference(s): <br>
- [Bucket Operations Guide](references/bucket_operations.md) <br>
- [Object Operations Guide](references/object_operations.md) <br>
- [Advanced Features Guide](references/advanced_features.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for cloud storage actions that may mutate or expose data when copied into automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
