## Description:

Guides the creation of a new Kunpeng ECS instance on Huawei Cloud and installation of Kunpeng DevKit with WebUI access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to provision a new Huawei Cloud Kunpeng ECS instance, install Kunpeng DevKit in WebUI mode, and verify access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud key deletion may prevent recovery or affect resources outside this installation.

Mitigation: Run KMS cleanup only after successful verification and only for a key proven to have been created for this workflow.

Risk: Unverified SSH host keys could expose the root password to an impersonated host.

Mitigation: Verify the SSH host key before connecting or sending the password.

Risk: Open SSH and WebUI ingress may expose the instance publicly.

Mitigation: Limit ports 22 and 8086 to a trusted source CIDR and obtain approval before changing security-group rules.

Risk: Remote installation packages may contain untrusted code.

Mitigation: Install only from a trusted, pinned source and verify package authenticity before execution.

Risk: Broad cloud privileges could amplify the impact of unintended changes.

Mitigation: Use a least-privilege Huawei Cloud identity scoped to the required resources.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-devkit-webui-create)
- [Prerequisites](artifact/references/prerequisites.md)
- [DevKit installation workflow](artifact/references/devkit-installation-workflow.md)
- [Security design](artifact/references/security-design.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command examples and installation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification steps and the WebUI access endpoint.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
