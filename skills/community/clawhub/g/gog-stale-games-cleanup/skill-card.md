## Description:

Scan your GOG library for installed games not played in 30+ days, email the list, and add Apple Reminders for each. One-command game cleanup workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit an installed GOG library, identify games that have not been played recently, and create email and Apple Reminders follow-up items for cleanup decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send game names, last-played dates, and install paths by email.

Mitigation: Run with --dry-run first and confirm the Himalaya account and recipient before allowing email delivery.

Risk: Normal execution can create or modify Apple Reminders.

Mitigation: Use normal mode only when reminder creation is intended, and verify the target reminders list.

Risk: Cron integration can cause recurring email and reminder side effects.

Mitigation: Enable the cron example only when recurring monthly cleanup notifications are desired.

## Reference(s):

- [GOG Library schema](references/gog_library_schema.json)
- [Skill release page](https://clawhub.ai/terrycarter1985/skills/gog-stale-games-cleanup)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can trigger email and Apple Reminders side effects unless run with --dry-run.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
