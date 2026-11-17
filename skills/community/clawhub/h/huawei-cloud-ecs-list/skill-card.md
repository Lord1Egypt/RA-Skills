## Description:

Lists Huawei Cloud ECS instances in a selected region, with filters and table, JSON, or compact name-and-ID output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to review regional ECS inventory, filter instances, and obtain server IDs for read-only operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SDK fallback reads credential environment variables, despite the documentation's wording.

Mitigation: Use credentials limited to ECS listing, keep secrets out of chat, and configure them in the trusted local environment.

Risk: Printed ECS inventory can contain sensitive infrastructure details.

Mitigation: Restrict access to the output and share it only through authorized workflows.

Risk: The bundled installer and live authenticated behavior were not verified.

Mitigation: Use Huawei's current official KooCLI guide, leave ECS_LIST_HCLOUD_BIN and ECS_LIST_HCLOUD_ARGS unset, and choose a recognized region.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-ecs-list)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credential guide](references/cli-installation-guide.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Plain-text inventory table or JSON instance array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Printed to stdout; no file is written.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
