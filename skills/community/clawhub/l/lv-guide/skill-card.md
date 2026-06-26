## Description: <br>
Little Donkey Smart Calendar Assistant helps users view calendars online and responds to calendar-related prompts such as today's calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javaxujunxuan](https://clawhub.ai/user/javaxujunxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this calendar assistant to ask for dates, current time, lunar-calendar conversion, holiday checks, countdowns, and simple schedule or reminder handling through natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact has noisy repeated metadata and an overbroad calendar trigger, which may make activation and user expectations unclear. <br>
Mitigation: Clean up repeated metadata and narrow the trigger to explicit calendar, date, holiday, countdown, or schedule-management requests before broad deployment. <br>
Risk: The skill describes schedule management, but security guidance says persistence behavior is not clearly disclosed. <br>
Mitigation: Clarify whether schedule or reminder handling is conversational only or writes to persistent storage, and avoid sensitive calendar details until that behavior is documented. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, credential access, private calendar access, or command execution is identified in the security evidence.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
