## Description:

Automatically check for and install OpenClaw updates, including scheduled updates, dry-run checks, backups, and rollback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlin87468-maker](https://clawhub.ai/user/zlin87468-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check their installed OpenClaw version, update to the latest available package, create backups before updating, and configure periodic update checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install global OpenClaw packages from mutable npm release channels.

Mitigation: Run dry-run checks first, review the resolved package and version, and require manual approval before installation.

Risk: Cron-based unattended updates can change a local OpenClaw installation without interactive review.

Mitigation: Avoid unattended cron updates unless the operator accepts the supply-chain and local filesystem risks.

Risk: Using sudo or root cron can broaden the impact of a failed or malicious update.

Mitigation: Run the updater without sudo or root cron whenever possible and verify npm permissions before installation.

Risk: The updater falls back from the scoped @openclaw/core package to the unscoped openclaw package.

Mitigation: Review and approve the fallback package behavior before running installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlin87468-maker/skills/linz-openclaw-updater)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run, force-update, cron scheduling, log review, and rollback commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
