## Description:

Provides installation guidance, authentication setup, command examples, and best practices for using Huawei Cloud KooCLI to manage Huawei Cloud services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason7602](https://clawhub.ai/user/jason7602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to install and configure Huawei Cloud KooCLI, run common ECS, OBS, RDS, FunctionGraph, CES, and AOM commands, and adapt examples for automation, migration, monitoring, and CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through Huawei Cloud AK/SK examples or copied configuration commands.

Mitigation: Use secret managers or protected environment variables, prefer temporary credentials, and avoid placing real AK/SK values in files, logs, shell history, or shared snippets.

Risk: Privileged installer commands and downloaded CLI binaries may create supply-chain or local system risk.

Mitigation: Download KooCLI only from trusted Huawei Cloud sources, verify binaries before installation, and run privileged installation steps only in controlled environments.

Risk: Examples include destructive or state-changing cloud operations such as stopping, rebooting, deleting, uploading, deploying, and alarm creation.

Mitigation: Run commands first against confirmed non-production resources, verify resource IDs and regions, use least-privileged IAM policies, and require change approval for production actions.

Risk: Python examples use shell command execution patterns that can become unsafe when command strings include untrusted input.

Mitigation: Avoid copying shell=True examples directly; prefer argument arrays, input validation, and explicit error handling when adapting automation scripts.

## Reference(s):

- [KooCLI Official Documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI User Guide](https://support.huaweicloud.com/ug-hcli/hcli_02_0001.html)
- [KooCLI API Reference](https://support.huaweicloud.com/api-hcli/hcli_01_0001.html)
- [Huawei Cloud Service Documentation](https://support.huaweicloud.com/)
- [ClawHub Skill Page](https://clawhub.ai/jason7602/skills/hwc-cli-guidance)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with bash, PowerShell, Python, YAML, and Groovy examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for cloud resource management and automation workflows; users must review commands before execution.]

## Skill Version(s):

0.0.14 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
