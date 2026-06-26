## Description: <br>
Provides guidance for installing, configuring, and using Huawei Cloud KooCLI to manage Huawei Cloud resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason7602](https://clawhub.ai/user/jason7602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to install KooCLI, configure Huawei Cloud authentication, and generate command examples for common resource-management tasks such as ECS, OBS, RDS, FunctionGraph, monitoring, and CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud access keys, Secret Access Keys, and credentials.csv can expose Huawei Cloud accounts if copied into prompts, scripts, logs, or repositories. <br>
Mitigation: Treat credentials as secrets, prefer CI secret stores or temporary credentials, and use least-privilege IAM permissions. <br>
Risk: Generated KooCLI examples can change live cloud resources, including stopping, restarting, deleting, or deploying resources. <br>
Mitigation: Review profile, region, resource IDs, command flags, and production impact before executing state-changing commands. <br>
Risk: Installing a CLI from an unverified download source can introduce supply-chain risk. <br>
Mitigation: Verify the KooCLI download source before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason7602/hwc-cli-guidance) <br>
- [KooCLI official documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html) <br>
- [Huawei Cloud documentation](https://support.huaweicloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash, PowerShell, Python, and YAML command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include cloud commands that users should review before running against live resources.] <br>

## Skill Version(s): <br>
0.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
