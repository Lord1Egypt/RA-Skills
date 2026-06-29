## Description: <br>
Configure Huawei Cloud OBS static website hosting with Python SDK and a custom domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to enable or repair static website hosting on an existing Huawei Cloud OBS bucket, register a custom domain, configure DNS when Huawei Cloud DNS manages the zone, and verify HTTP/DNS behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can intentionally expose OBS bucket content for public website access. <br>
Mitigation: Use a dedicated public website bucket or tightly scoped prefix, confirm no sensitive content is present, and verify anonymous read only for intended website files. <br>
Risk: The skill uses Huawei Cloud AK/SK credentials to configure OBS website hosting and custom domains. <br>
Mitigation: Use least-privilege temporary or rotated credentials, avoid hardcoding secrets, and report only credential presence rather than credential values. <br>
Risk: DNS CNAME changes can affect production traffic for the custom domain. <br>
Mitigation: Confirm domain ownership, zone, and intended record before making changes; verify CNAME resolution and HTTP behavior before claiming completion. <br>
Risk: The workflow may require downloading Huawei CLI or obsutil installers. <br>
Mitigation: Download installers only from vendor sources and verify them before execution. <br>


## Reference(s): <br>
- [CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Huawei Cloud DNS Configuration for OBS Static Website](references/hcloud-dns-obs-website.md) <br>
- [IAM Policy - Huawei Cloud OBS Website Host](references/iam-policies.md) <br>
- [OBS Python SDK Website Configuration Notes](references/obs-python-sdk-website.md) <br>
- [Validation Rules](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python script invocations, configuration details, and verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled helper scripts for OBS website configuration and endpoint verification; may include DNS handoff details when DNS is managed outside Huawei Cloud.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
