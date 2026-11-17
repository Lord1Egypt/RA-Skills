## Description:

Huawei Cloud CLI Guidance helps developers install, configure, authenticate, and use Huawei Cloud KooCLI for cloud service management and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason7602](https://clawhub.ai/user/jason7602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill for guidance on installing Huawei Cloud KooCLI, configuring authentication, running common cloud management commands, and building simple automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance can involve unpinned downloads and system-wide placement of CLI binaries.

Mitigation: Use pinned, verified KooCLI releases, validate checksums when available, and avoid sudo or system-wide installation unless operationally required.

Risk: Cloud credentials can be exposed through long-lived AK/SK values, command histories, or logs.

Mitigation: Use least-privilege credentials, prefer secure environment or secret-store injection, avoid logging secrets, and rotate credentials after suspected exposure.

Risk: The guidance includes live infrastructure-changing commands, including start, stop, restart, upload, delete, and deployment examples.

Mitigation: Review commands before execution, test in non-production accounts where possible, scope IAM permissions narrowly, and require operator approval for production changes.

Risk: Python examples using shell=True can become unsafe if reused with dynamic or untrusted input.

Mitigation: Use argument-list subprocess calls, validate inputs, and avoid shell=True in reusable automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason7602/skills/hwc-cli-guidance-v2)
- [Artifact installation guide](artifact/reference/installation-guide.md)
- [Artifact command reference](artifact/reference/command-reference.md)
- [Artifact best practices](artifact/reference/best-practices.md)
- [KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI user guide](https://support.huaweicloud.com/ug-hcli/hcli_02_0001.html)
- [KooCLI API reference](https://support.huaweicloud.com/api-hcli/hcli_01_0001.html)
- [Huawei Cloud service documentation](https://support.huaweicloud.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash, PowerShell, Python, YAML, and Groovy code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for KooCLI installation, authentication, common commands, operational examples, and best practices.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
