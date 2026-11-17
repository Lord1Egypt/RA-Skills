## Description:

Ambil jadwal sholat (imsak, subuh, dzuhur, ashar, maghrib, isya) untuk kota/kabupaten di Indonesia dari API Muslim api.myquran.com (sumber Kemenag Bimas Islam).

This skill is ready for commercial/non-commercial use.

## Publisher:

[banghasan](https://clawhub.ai/user/banghasan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up Indonesian prayer schedules by city or regency name, location ID, date, month, and timezone. It supports location search plus daily, dated, and monthly prayer-time lookups through api.myquran.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prayer-time lookup inputs such as city or location ID, date or month, and timezone are sent to api.myquran.com.

Mitigation: Install only when that external API use is acceptable for the intended environment and avoid submitting sensitive location context.

Risk: Monthly lookup output is a seven-day preview rather than a complete month.

Mitigation: Treat monthly results as a preview and request specific dates when complete daily values are needed.

Risk: Location search can return multiple Indonesian city or regency candidates and may select the first match when no exact match is found.

Mitigation: Use a more specific location keyword or a known location ID when precision matters.

## Reference(s):

- [api.myquran.com v3 API](https://api.myquran.com/v3)
- [ClawHub skill page](https://clawhub.ai/banghasan/skills/jadwal-sholat-banghasan)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text prayer-time results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Indonesian-language output; monthly results are presented as a seven-day preview in the helper script.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
