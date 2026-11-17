## Description:

Manage and diagnose Huawei Cloud WAF and AAD protection with hcloud CLI guidance for queries, rule management, CNAME onboarding checks, rule-order analysis, and Anti-DDoS coverage review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud security engineers, and operations teams use this skill to inspect Huawei Cloud WAF and AAD posture, diagnose CNAME and protection coverage issues, and prepare WAF rule changes with confirmation gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide WAF rule changes or deletions that may affect production traffic.

Mitigation: Use least-privilege credentials, preview every create or delete command, and require explicit user confirmation before write actions.

Risk: The helper script can persistently alter command lookup by adding the CLI directory to PATH and creating a symlink in a writable PATH directory.

Mitigation: Inspect or remove the PATH and symlink behavior before installation if persistent command lookup changes are not acceptable.

Risk: Quality reporting may send execution metadata through skill-quality-cli.

Mitigation: Disable quality reporting with SKILL_QUALITY_REPORT=0 when telemetry is not appropriate for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-waf-aad-rule-management)
- [KooCLI official installation documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI installation and configuration guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Related commands and context](references/related-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostics may be auto-run; rule creation and deletion require preview and user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
