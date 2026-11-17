## Description:

Checks whether a specified date, or today by default, is a workday or non-working day using the public isdayoff.ru API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freemandigger](https://clawhub.ai/user/freemandigger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer whether a date is a working day, weekend, or day off before scheduling reminders, automation, or other date-sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can make outbound HTTP(S) requests to caller-specified endpoints via --endpoint.

Mitigation: Use the default isdayoff.ru endpoint, avoid passing untrusted endpoint values, and consider allowlisting or removing endpoint overrides before automated agent use.

## Reference(s):

- [isdayoff.ru API documentation](https://www.isdayoff.ru/docs/)
- [ISDAYOFF API notes](references/ISDAYOFF.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status with optional Markdown shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script exits with status 0 for workdays, 1 for non-working days, and nonzero error codes for invalid input or API failures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
