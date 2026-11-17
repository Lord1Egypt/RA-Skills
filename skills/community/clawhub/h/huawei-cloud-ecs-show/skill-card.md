## Description:

Queries one Huawei Cloud ECS instance by ID through KooCLI or the Huawei Cloud ECS SDK and returns a text summary, JSON, or an optional Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect a single Huawei Cloud ECS instance for troubleshooting or as a pre-query step for another ECS workflow. They provide an instance ID and can read the result as a detail summary, JSON, or a Markdown export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted region value can send an authenticated request to a server outside Huawei.

Mitigation: Wait for region validation that rejects unknown values before using the SDK fallback with credentials; use read-only credentials and packages verified through Huawei's installation documentation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-ecs-show)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Text detail summary, JSON, or a Markdown document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One ECS instance per request; a local file is written only when --md-file is supplied.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
