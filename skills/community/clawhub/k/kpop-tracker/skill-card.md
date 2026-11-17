## Description:

Tracks K-Pop idol updates for comebacks, albums, concerts, solo activities, merchandise, official YouTube content, and Chinese member Weibo posts using official, media, and Taiwan fan sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryemco](https://clawhub.ai/user/ryemco)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor followed K-Pop artists and summarize recent idol schedules, release news, shopping links, official videos, concerts, and solo activity in Traditional Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores followed artists and reported URLs in local workspace files.

Mitigation: Keep the tracking files in an appropriate workspace, avoid adding sensitive private data, and review or delete the local history when it is no longer needed.

Risk: The skill uses a browser profile to check social, media, and shopping sites.

Mitigation: Review source links before acting on results, and avoid relying on unverified fan or shopping pages for purchases or schedule commitments.

Risk: Automatic twice-daily checks can be created through cron when requested.

Mitigation: Enable scheduled checks only after explicit user consent and remove the cron jobs when ongoing monitoring is no longer wanted.

## Reference(s):

- [Kpop Tracker on ClawHub](https://clawhub.ai/ryemco/skills/kpop-tracker)
- [ryemco ClawHub profile](https://clawhub.ai/user/ryemco)
- [Config Examples](references/config_examples.md)
- [Starship Entertainment](https://www.starshipent.com)
- [Starship Shop](https://shop.starship-ent.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Traditional Chinese Markdown reports with source links, tables, JSON configuration examples, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs six fixed update categories per tracked group and keeps local check history to reduce duplicate alerts.]

## Skill Version(s):

v2.1.0 (source: server release evidence, SKILL.md metadata, CHANGELOG released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
