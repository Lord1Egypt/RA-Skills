## Description:

Captures poor experiences with Huawei Cloud tools and turns developer feedback into structured requirements or GitCode issue reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill when they encounter errors or poor experiences with Huawei Cloud tools or services. It captures and sanitizes feedback, prepares a structured report for the configured GitCode repository, and can send an optional notification through configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because scanners report broad cloud command access, automatic collection and external sharing of conversation content, and software installation; this does not establish malicious intent.

Mitigation: Review the hooks and settings to understand what conversation and environment information may be collected and sent, check the configured destinations and telemetry, and confirm that you accept the installation and cloud command access. Disable quality reporting with SKILL_QUALITY_REPORT=0 if you do not want it.

Risk: Security scan coverage is incomplete: Skillspector inspected 28 of 29 components and one static analysis was partial, so the scan cannot rule out additional issues.

Mitigation: Review the skill and its configured behavior before use; treat the scan as incomplete evidence rather than assurance that no other issues exist.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-vod-collector)
- [GitCode issue repository configured by the skill](https://gitcode.com/developer-skill/vod-skill.git)
- [AtomGit-GO source repository](https://gitcode.com/weixin_45218422/AtomGit-GO)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)
- [Hook setup](references/hooks-setup.md)
- [Deduplication and notifications](references/dedup-and-notify.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM and network requirements](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown feedback reports and GitCode issue content, with JSON command results and shell commands for workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Feedback is stored as Markdown; report delivery and notification destinations are configured by the user or integrator.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
