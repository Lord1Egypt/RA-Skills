## Description:

Configure Huawei Cloud OBS static website hosting with Python SDK and a custom domain. Use when the user needs to enable or repair OBS website hosting, set index or error pages, expose an existing bucket for public website access through a custom domain, or connect that domain through Huawei Cloud DNS when Huawei manages the zone. Triggers include OBS static website hosting, website endpoint, index page, error page, public-read bucket website access, custom domain CNAME, Huawei Cloud DNS, setBucketWebsite. 中文触发词包括：OBS 静态网站托管、网站托管、自定义域名解析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and site operators use this skill to configure an existing Huawei Cloud OBS bucket for static website hosting, bind a custom domain, optionally update Huawei Cloud DNS, and verify reachability or troubleshoot common 403 and 404 responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the suggested permissions may be too broad, and bucket or DNS writes can affect live traffic.

Mitigation: Scope permissions to the intended bucket, grant DNS access only when requested, and confirm the bucket, domain, and DNS zone before making changes.

Risk: Cloud credentials or certificate private keys could be exposed through recorded setup commands.

Mitigation: Keep access keys and private keys out of recorded commands; use protected credential sources and certificate IDs where possible.

Risk: Website setup can make bucket content publicly reachable, while DNS changes can redirect a live hostname.

Mitigation: Publish only intended website files, confirm the target bucket and hostname before writes, and verify the resulting site and DNS behavior.

Risk: Static review cannot establish the live account's permissions or the safety of downloaded third-party code.

Mitigation: Check the effective permissions and inspect and verify downloaded installers before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-website-host)
- [OBS Python SDK website configuration notes](references/obs-python-sdk-website.md)
- [Huawei Cloud DNS configuration for OBS static websites](references/hcloud-dns-obs-website.md)
- [Huawei Cloud OBS website host IAM policy](references/iam-policies.md)
- [Website endpoint validation rules](references/verification-method.md)
- [CLI installation and configuration guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Shell commands]

**Output Format:** [Markdown report with verification results, remediation guidance, and shell commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configures only the user-specified bucket; DNS records are changed only when requested. Does not upload or modify bucket objects.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
