## Description: <br>
Huawei Cloud Ascend Command helps agents translate natural-language requests into local or SSH-based Huawei Ascend NPU administration commands for device queries, monitoring, configuration, firmware, virtualization, certificates, and compute tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to inspect and administer Huawei Ascend NPU hosts through npu-smi and ascend-dmi operations. It supports routine device health checks and high-impact administrative workflows such as ECC, fan, firmware, vNPU, certificate, reset, and raw npu-smi actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote high-impact NPU administration can affect device configuration, firmware, certificates, virtualization, resets, and raw npu-smi behavior. <br>
Mitigation: Install only where Ascend NPU administration is intended; prefer read-only use, least-privilege accounts, explicit device IDs, and manual review before high-impact operations. <br>
Risk: Credential handling and SSH remote execution can expose or misuse privileged access. <br>
Mitigation: Prefer SSH keys and least-privilege accounts, avoid command-line passwords where possible, and do not ask users to share passwords in conversation. <br>
Risk: Troubleshooting guidance includes a broad device permission workaround that is unsafe on shared or production systems. <br>
Mitigation: Do not apply chmod 666 to NPU device nodes on shared or production hosts; use scoped group membership or administrator-approved permissions instead. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huaweiclouddev/huawei-cloud-ascend-command) <br>
- [Publisher profile](https://clawhub.ai/user/huaweiclouddev) <br>
- [Huawei Ascend official documentation](https://www.hiascend.com/document) <br>
- [npu-smi command reference](https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/260RC1/re/npu/npusmi_007.html) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Verification steps](references/verification-method.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Device queries reference](references/device-queries.md) <br>
- [Configuration management reference](references/configuration.md) <br>
- [Firmware upgrade reference](references/firmware-upgrade.md) <br>
- [Virtualization management reference](references/virtualization.md) <br>
- [Certificate management reference](references/certificate-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text and JSON-style command results with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit local or SSH npu-smi and ascend-dmi operations; sensitive operations require explicit review and confirmation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata, created 2026-06-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
