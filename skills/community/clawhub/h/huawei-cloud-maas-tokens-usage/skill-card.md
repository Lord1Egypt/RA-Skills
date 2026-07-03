## Description: <br>
Query Huawei Cloud MaaS token usage statistics, including total, prompt, and completion tokens, request counts, and error counts across preset service, my service, or custom endpoint time ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and Huawei Cloud account operators use this skill to query MaaS token consumption, request volume, and errors for billing, usage monitoring, and troubleshooting over selected time ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script disables HTTPS certificate verification while using Huawei Cloud credentials. <br>
Mitigation: Review or patch the helper script to remove verify=False before use, and run it only in trusted network environments. <br>
Risk: The skill requires sensitive Huawei Cloud AK/SK credentials. <br>
Mitigation: Use least-privilege Huawei Cloud keys and provide them only through environment variables or a local credentials file, not through chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-maas-tokens-usage) <br>
- [Huawei Cloud MaaS ShowStatistics API](https://support.huaweicloud.com/api-maas/ShowStatistics.html) <br>
- [Task: Query MaaS Tokens Usage Statistics](references/task-query-tokens-usage.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [IAM Permission Policy](references/iam-policies.md) <br>
- [MaaS Monitoring Metrics Reference](references/maas-metrics.md) <br>
- [Prerequisites Installation Guide](references/cli-installation-guide.md) <br>
- [Verification Steps and Methods](references/verification-method.md) <br>
- [Troubleshooting and Practical Experience](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Markdown] <br>
**Output Format:** [Markdown with shell commands and tabular CLI output; optional raw JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Huawei Cloud AK/SK credentials via environment variables or a local credentials file; reports token, request, error, and period metrics.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
