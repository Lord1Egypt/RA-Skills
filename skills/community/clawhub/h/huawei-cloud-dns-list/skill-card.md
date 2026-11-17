## Description:

Lists Huawei Cloud public or private DNS zones and record sets, with table, JSON, names-only, and Markdown export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and platform engineers use this skill to inspect tenant DNS inventory for operations reviews and retrieve zone IDs or domain names for follow-on tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged for review because environment settings may select a program that runs with the agent’s privileges; scan coverage is partial.

Mitigation: Before installing, verify that DNS_LIST_HCLOUD_BIN and DNS_LIST_HCLOUD_ARGS are controlled by trusted configuration and confirm the permissions granted to the host running the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-dns-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [CLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Files]

**Output Format:** [Tables, JSON arrays, domain-name lists, and UTF-8 Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only DNS inventory; optional Markdown file export]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
