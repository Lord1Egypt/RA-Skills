## Description: <br>
Calculate and display the number of days remaining until China's National Day on October 1st, returning today's date and a readable message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gysmax](https://clawhub.ai/user/gysmax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent to answer countdown questions for China's National Day or October 1st. The skill guides the agent to return today's date, the target National Day date, the non-negative number of days remaining, and a readable message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A future version could request permissions, credentials, network access, local file access, or execution that are not needed for this countdown task. <br>
Mitigation: Re-review and rescan any future version that asks for those capabilities before installation or use. <br>
Risk: Date-dependent answers can be wrong if the agent uses a stale or incorrect current date. <br>
Mitigation: Use the current date at response time and, when the date is after October 1st, calculate against the next year's National Day. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gysmax/national-day-countdown) <br>
- [Publisher profile](https://clawhub.ai/user/gysmax) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text or Markdown response with dates and a countdown value] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials, network access, local file access, or shell execution are expected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
