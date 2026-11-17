## Description:

Queries Chinese almanac information for a requested date, including Gregorian and lunar dates, heavenly stems and earthly branches, five elements, and recommended or avoided activities, using the tiax.cn almanac API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettersao](https://clawhub.ai/user/bettersao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Chinese almanac details for today, tomorrow, or a specified date when planning events such as weddings, openings, moving, renovation, or memorial activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Date lookups are sent to the third-party tiax.cn service, which may reveal query timing and requested dates.

Mitigation: Avoid using the skill for offline-only workflows or when requested dates should not be shared with that service.

Risk: Responses are in Chinese and may be misunderstood by users who cannot review the returned almanac fields.

Mitigation: Have a Chinese-reading user or downstream translation step review results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettersao/skills/huangli-almanac)
- [tiax.cn almanac API](https://api.tiax.cn/almanac/)
- [tiax.cn API homepage](https://api.tiax.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with almanac fields and optional shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to tiax.cn; documented command-line usage requires curl and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
