## Description:

Installs Terraform CLI on Linux and Windows with Huawei Cloud mirror support for HuaweiCloud provider setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install Terraform, configure HuaweiCloud provider mirrors, check installation status, initialize Terraform, test provider setup, or uninstall local Terraform components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verification docs include a plaintext root SSH credential.

Mitigation: Review the artifact before use and rotate or invalidate the exposed credential if it is real.

Risk: The installer can make broad local system changes, including Terraform binary installation, PATH updates, terraformrc changes, and provider cache writes.

Mitigation: Run it only on machines where those Terraform and PATH changes are acceptable, and avoid sudo or administrator privileges unless necessary.

Risk: The uninstall path can remove Terraform binaries, Terraform CLI configuration, and provider directories.

Mitigation: Back up existing Terraform configuration and provider caches before using --uninstall.

## Reference(s):

- [Verification Method](references/verification-method.md)
- [Verification Result](references/verification-result.md)
- [Test Scenarios](references/test-scenarios.md)
- [HashiCorp Terraform install documentation](https://developer.hashicorp.com/terraform/install)
- [HashiCorp Terraform releases](https://releases.hashicorp.com/terraform/)
- [Huawei Cloud Terraform mirror](https://mirrors.huaweicloud.com/terraform/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and a Python installer script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify Terraform binaries, PATH, terraformrc, and local provider directories when executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
