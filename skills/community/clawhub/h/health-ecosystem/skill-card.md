## Description:

Health Ecosystem helps an agent build a personal health-management loop around Huawei Health data, Obsidian notes, scheduled automation, daily logs, weekly reports, and goal tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajawpwinner-del](https://clawhub.ai/user/ajawpwinner-del)

### License/Terms of Use:

MIT

## Use Case:

Individuals and their agents use this skill to collect Huawei wearable health signals, organize them in an Obsidian health vault, and produce daily logs, weekly reports, goal tracking, and health insights. It is intended for personal health organization and review, not clinical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health, biometric, reproductive-health, and account-related data.

Mitigation: Use a private, trusted repository or local-only setup, restrict vault and repository access, and avoid syncing sensitive categories unless the storage destination and access model are acceptable.

Risk: Scheduled automation and Git synchronization can move or update health records without per-run user review.

Mitigation: Review cron schedules, generated files, and Git sync targets before enabling automation, and keep sync destinations private.

Risk: The skill depends on external helper skills and tools whose behavior may change over time.

Mitigation: Verify the publishers and exact versions of xiaoyi-health, obsidian-git-vault, and openclaw cron before installation or release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajawpwinner-del/skills/health-ecosystem)
- [Publisher profile](https://clawhub.ai/user/ajawpwinner-del)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates, conversational guidance, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated health logs, weekly summaries, goal templates, schedule setup guidance, and configuration notes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
