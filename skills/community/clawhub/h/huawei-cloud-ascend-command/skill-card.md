## Description:

Translates natural-language requests into npu-smi and ascend-dmi operations for local or SSH-connected Huawei Ascend NPUs, covering device monitoring, configuration, firmware, vNPU virtualization, certificates, and FLOPS testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NPU administrators use the skill to inspect Ascend device health and metrics, manage supported configuration and firmware tasks, operate vNPU and certificate functions, and run FLOPS checks on local or SSH-connected hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH identity verification and password handling need review before remote use.

Mitigation: Verify the SSH server identity, use safer password input, and keep credentials out of conversation and logs.

Risk: Device configuration, firmware, and virtualization writes can change live hardware state.

Mitigation: Confirm the exact operation and NPU/chip target, use consistent write confirmation, and check device state before retrying a failed write.

Risk: Unsafe device permissions or persistent SSH service changes can expose the host.

Mitigation: Avoid the world-writable device workaround and review persistent SSH service changes separately.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ascend-command)
- [Ascend official documentation](https://www.hiascend.com/document)
- [npu-smi command reference](https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/260RC1/re/npu/npusmi_007.html)
- [Command mapping](references/command-mapping.md)
- [Firmware upgrade guide](references/firmware-upgrade.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Human-readable status or error text, with an optional JSON result envelope.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs supported local or remote device operations; read-only queries return results, while sensitive writes require confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
