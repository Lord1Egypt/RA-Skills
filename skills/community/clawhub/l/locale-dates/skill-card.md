## Description:

Locale Dates helps an agent format and convert dates, times, durations, time zones, relative time, and localized weekday or month names without external tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer date, time, duration, time-zone conversion, and locale-specific formatting requests in the user's language. It is useful for user-facing assistants that need clear, localized date and time output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone and daylight-saving calculations can be wrong when the user's location, target timezone, or date is ambiguous.

Mitigation: Ask for or state the timezone, spell out ambiguous dates, and verify critical calculations before relying on the result.

Risk: The skill may rely on existing user preference context for locale choices.

Mitigation: Confirm the desired locale or use ISO 8601 when the user's preferred format is unknown.

## Reference(s):

- [Locale Reference Table](references/locales.md)
- [Locale Dates on ClawHub](https://clawhub.ai/tommot2/skills/locale-dates)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown answers with localized date and time values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no files, shell commands, dependencies, persistence, or external tool calls are produced by the skill.]

## Skill Version(s):

3.1.0 (source: release evidence and changelog, released 2026-04-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
