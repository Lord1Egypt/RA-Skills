## Description:

Lucky Today is an offline deterministic daily fortune skill that produces bilingual lucky directions, colors, numbers, items, dos and don'ts, couple readings, scenario fortunes, and optional push-ready text without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ClawHub agents use Lucky Today to produce entertainment-oriented daily, weekly, monthly, couple, or scenario fortune readings in Chinese or English. It can also produce concise push-ready fortune text when the host runtime is configured for scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may save birth dates, partner birth dates, or push destination IDs in a plaintext local profile.

Mitigation: Save a profile only after explicit opt-in, avoid storing partner birth dates or push IDs unless needed, restrict local file permissions, and delete the profile when no longer wanted.

Risk: Scheduled push delivery can send fortune text to an unintended channel if the destination is wrong.

Mitigation: Verify the cron schedule and destination before enabling delivery, and keep generated push messages free of profile JSON or hidden runtime details.

Risk: Entertainment fortune output could be mistaken for factual, medical, legal, or financial advice.

Mitigation: Keep the folklore and entertainment disclaimer visible and add a rational-judgment reminder for high-risk topics.

## Reference(s):

- [Lucky Today ClawHub Page](https://clawhub.ai/jiajiaoy/skills/lucky-today)
- [Fortune Rules](references/fortune_rules.md)
- [Output Templates](references/output_templates.md)
- [Scenario Rules](references/scenario_rules.md)
- [Couple Rules](references/couple_rules.md)
- [User Profile Template](references/user_profile_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style fortune text with structured bilingual templates and optional inline shell commands for scheduling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; deterministic for the same profile and query date; intended as folklore and entertainment reference.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, artifact/_meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
