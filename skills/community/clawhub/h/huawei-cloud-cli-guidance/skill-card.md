## Description:

Guides users through installing and configuring Huawei Cloud KooCLI, constructing commands, and troubleshooting common errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this guidance to install KooCLI, configure authentication, form Huawei Cloud service commands, and troubleshoot common errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide has conflicting execution boundaries and includes unsafe root logins and potentially destructive cleanup guidance.

Mitigation: Keep it advisory until its execution rules are consistent. Use least-privilege credentials and verified SSH host keys, obtain separate approval for resource changes, and confirm backups and exact disks before cleanup; preserve profiles unless explicitly purging them.

Risk: Installation examples retrieve external installers and container images, and diagnostic output can contain sensitive information.

Mitigation: Verify installer and container provenance before execution, and redact diagnostic logs before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cli-guidance)
- [Getting Started](references/getting-started.md)
- [Credential Security Best Practices](references/credential-security.md)
- [Installation Guide](references/installation-guide.md)
- [KooCLI Error Troubleshooting and FAQ](references/cli-troubleshooting.md)
- [IAM Policies](references/iam-policies.md)
- [OBS Operations](references/obsutil-operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command and configuration examples; review execution boundaries before use.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
