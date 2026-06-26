## Description: <br>
Determines whether a specified date, or today by default, is a working day or day off using the isdayoff.ru API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemandigger](https://clawhub.ai/user/freemandigger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and scheduling assistants use this skill to check whether a date is a workday, weekend, or holiday before planning reminders or work-dependent actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the requested date to isdayoff.ru by default and allows a custom endpoint. <br>
Mitigation: Use the default service or another trusted endpoint only; do not point --endpoint at internal services, localhost, or URLs that could expose sensitive network context. <br>
Risk: The result depends on an external API remaining available and preserving compatible response codes. <br>
Mitigation: Treat failures or unknown responses as inconclusive and verify time-sensitive scheduling decisions before acting on them. <br>


## Reference(s): <br>
- [isdayoff.ru API documentation](https://www.isdayoff.ru/docs/) <br>
- [ISDAYOFF reference notes](references/ISDAYOFF.md) <br>
- [ClawHub skill page](https://clawhub.ai/freemandigger/isdayoff-checker) <br>
- [Publisher profile](https://clawhub.ai/user/freemandigger) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status with process exit code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make an outbound network request to isdayoff.ru or a user-specified trusted endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
