## Description:

Helps agents operate Huawei AppGallery Connect through documented connect-api-cli workflows for authentication, app management, package releases and testing, certificates, permissions, and domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hufaguang](https://clawhub.ai/user/hufaguang)

### License/Terms of Use:

MIT-0

## Use Case:

HarmonyOS developers can use the skill's workflows to manage AppGallery Connect apps, releases, test distribution, certificates, access permissions, and domains. It also guides local debug builds and installation on a connected device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is suspicious with medium confidence and incomplete coverage, so it cannot fully establish the skill's behavior.

Mitigation: Review the full skill scope and credential or certificate steps before use, as the scan guidance recommends.

Risk: The documented workflows handle AGC credentials, tokens, passwords, and signing materials.

Mitigation: Keep credentials and passwords out of output and logs, and keep signing files in the documented protected location.

## Reference(s):

- [Command reference](artifact/references/commands.md)
- [Workflows](artifact/references/workflows.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Huawei AppGallery Connect package upload documentation](https://developer.huawei.com/consumer/cn/doc/app/agc-help-upload-api-upload-url-0000002236201294)
- [ClawHub skill release](https://clawhub.ai/hufaguang/skills/hmos-connect-api-cli-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Operational guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow steps and checks for command results and generated artifacts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
