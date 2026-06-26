## Description: <br>
Provides guidance for installing, configuring, authenticating, and using Huawei Cloud KooCLI for cloud operations and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason7602](https://clawhub.ai/user/jason7602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to learn KooCLI installation, credential configuration, common Huawei Cloud service commands, automation examples, and operational best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KooCLI examples use Huawei Cloud AK/SK credentials and may expose secrets if copied into scripts or logs. <br>
Mitigation: Store credentials as secrets or environment variables, use least-privilege or temporary credentials where possible, and avoid hard-coding AK/SK values. <br>
Risk: Installation examples download CLI binaries and move them into system paths. <br>
Mitigation: Download KooCLI only from official Huawei sources and verify binaries before system-wide installation. <br>
Risk: Delete, restart, and bulk-operation examples can affect live cloud resources. <br>
Mitigation: Test commands in scoped non-production environments and confirm resource identifiers before running them against production. <br>


## Reference(s): <br>
- [KooCLI Official Documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html) <br>
- [KooCLI User Guide](https://support.huaweicloud.com/ug-hcli/hcli_02_0001.html) <br>
- [KooCLI API Reference](https://support.huaweicloud.com/api-hcli/hcli_01_0001.html) <br>
- [Huawei Cloud Service Documentation](https://support.huaweicloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may include cloud administration commands that users should review before execution.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
