## Description:

Captures Huawei Cloud developer feedback, sanitizes and deduplicates reports, and helps prepare and deliver them to a configured GitCode repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Huawei Cloud tools can capture errors, corrections, and dissatisfaction as structured feedback, then review and submit useful reports to a configured GitCode project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing broad cloud-command access, automatic feedback collection and delivery, and installation of supporting tools. The scan was incomplete, and the verdict does not establish malicious intent.

Mitigation: Use the workflow only when needed and review its commands, reporting behavior, and configured destinations before installation. Set SKILL_QUALITY_REPORT=0 to opt out of quality reporting.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-vod-collector)
- [CLI installation guide](references/cli-installation-guide.md)
- [Deduplication and notifications](references/dedup-and-notify.md)
- [IAM policies and security notes](references/iam-policies.md)
- [Hooks setup](references/hooks-setup.md)
- [OpenClaw integration](references/openclaw-integration.md)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)
- [AtomGit-GO source](https://gitcode.com/weixin_45218422/AtomGit-GO)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown feedback reports with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Feedback is stored as project-local Markdown; issue delivery uses the configured destination and authentication.]

## Skill Version(s):

1.0.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
