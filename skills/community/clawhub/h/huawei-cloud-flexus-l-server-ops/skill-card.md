## Description: <br>
Helps agents operate Huawei Cloud Flexus L servers by querying instances and traffic packages, starting, stopping, rebooting, resetting passwords, and updating server metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill for daily Huawei Cloud Flexus L operations, including inventory checks, lifecycle management, password resets, metadata changes, and traffic monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform state-changing Huawei Cloud Flexus L operations, including stop, reboot, password reset, and metadata changes. <br>
Mitigation: Install only for accounts where this operational control is intended, require user confirmation for disruptive actions, and verify the target is a Flexus L instance before execution. <br>
Risk: Credential examples and command parameters may expose AK/SK, tokens, or passwords through command-line history, logs, or conversation output. <br>
Mitigation: Use temporary least-privilege credentials from environment variables, avoid passing secrets as command-line arguments, and do not run credential-printing verification commands. <br>
Risk: One cloud client disables TLS certificate verification. <br>
Mitigation: Fix or explicitly review the disabled TLS verification before using the skill in a sensitive Huawei Cloud account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-flexus-l-server-ops) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Huawei Cloud Flexus Application Server L documentation](https://support.huaweicloud.com/intl/zh-cn/flexusl_faq/faq_01_0003.html) <br>
- [Huawei Cloud PyPI mirror](https://repo.huaweicloud.com/repository/pypi/simple) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and operational status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Huawei Cloud SDK-backed scripts when the agent runtime supports skill action execution and credentials are configured.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
