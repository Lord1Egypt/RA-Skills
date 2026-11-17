## Description:

Use when you need to manage Multilogin through `xcli`, including Android cloud phones, browser profiles, workspaces, proxies, scripts, tags, files, apps, ADB access, and account settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[multilogincom](https://clawhub.ai/user/multilogincom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media workflow teams use this skill to control Multilogin browser profiles and Android cloud phones through the `xcli` and `mlx-launcher` command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent authority over Multilogin profiles, cloud phones, files, proxies, ADB sessions, account settings, and potentially billed mobile minutes.

Mitigation: Install only when the Multilogin CLI distribution is trusted, review proposed commands before execution, and require explicit confirmation before deletes, transfers, ADB actions, file operations, 2FA changes, or actions that spend mobile minutes.

Risk: The skill includes workflows that may handle account passwords or delegated node access.

Mitigation: Avoid sending passwords in chat or spawned node messages; prefer a pre-authenticated local `xcli` session or another secret-safe login method.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/multilogincom/skills/multilogin)
- [xcli latest version endpoint](https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest)
- [mlx-launcher latest version endpoint](https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `xcli` and `mlx-launcher`; may involve credentials, profile operations, cloud phone minutes, files, proxies, ADB sessions, and account settings.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
