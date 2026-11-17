## Description:

Ambil jadwal sholat untuk kota/kabupaten di Indonesia dari api.myquran.com, termasuk imsak, subuh, dzuhur, ashar, maghrib, dan isya.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banghasan](https://clawhub.ai/user/banghasan)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find Indonesian city/regency prayer times for today, a specific date, or a monthly preview, and to look up location IDs when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City or regency keywords, location IDs, dates, months, and timezone values may be sent to api.myquran.com.

Mitigation: Avoid entering sensitive location context and review whether sending these query values to the disclosed external API is acceptable for the deployment.

Risk: Monthly helper output can be mistaken for a complete monthly schedule even though it displays only a 7-day preview.

Mitigation: Tell users when monthly output is a preview and fetch specific dates or additional periods when a complete month is required.

## Reference(s):

- [MyQuran API base](https://api.myquran.com/v3)
- [ClawHub skill page](https://clawhub.ai/banghasan/skills/jadwal-sholat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text prayer schedule results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monthly helper output displays only a 7-day preview.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
