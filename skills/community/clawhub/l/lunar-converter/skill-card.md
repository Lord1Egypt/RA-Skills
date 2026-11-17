## Description:

Converts dates between the Chinese lunar calendar and the Gregorian calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jincan0412](https://clawhub.ai/user/jincan0412)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to answer Chinese lunar-to-Gregorian or Gregorian-to-lunar date conversion requests, including birthdays, traditional festival dates, and historical date lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion script depends on the local lunardate Python library being available.

Mitigation: Confirm lunardate is installed in the agent runtime before relying on the skill.

Risk: The skill documents support for dates from 1900 through 2100.

Mitigation: Keep user requests within the documented date range or disclose when a requested date is outside the supported range.

Risk: The skill documentation and command responses are primarily in Chinese.

Mitigation: Translate or explain outputs when the consuming workflow or user expects another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jincan0412/skills/lunar-converter)
- [Publisher profile](https://clawhub.ai/user/jincan0412)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script emits JSON result strings and expects numeric year, month, and day arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
