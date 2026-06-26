## Description: <br>
Format and convert dates, times, and durations; compute timezones, relative time, and weekday or month names in the user's local language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when an agent needs to format dates and times, convert timezones, calculate relative dates or durations, or present weekday and month names in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A hardcoded Europe/Oslo display rule can cause incorrect times if applied to logs, audits, incidents, schedules, or deadlines for users in other timezones. <br>
Mitigation: Preserve the original timezone, clearly label any conversion, and only use Europe/Oslo when that default matches the user's intended locale. <br>


## Reference(s): <br>
- [Locale Reference Table](references/locales.md) <br>
- [ClawHub skill page](https://clawhub.ai/tommot2/locale-dates) <br>
- [Publisher profile](https://clawhub.ai/user/tommot2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text date, time, duration, and timezone guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no shell execution, subprocesses, file modification, persistence, or external dependencies.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence and skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
