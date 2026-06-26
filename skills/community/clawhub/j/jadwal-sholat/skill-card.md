## Description: <br>
Retrieves Indonesian prayer times, including imsak, subuh, dzuhur, ashar, maghrib, and isya, for cities and regencies using api.myquran.com data sourced from Kemenag Bimas Islam. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banghasan](https://clawhub.ai/user/banghasan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Indonesian city or regency identifiers and retrieve prayer schedules for today, a specific date, or a month. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests send the city or regency keyword or ID, date or month, and timezone to api.myquran.com. <br>
Mitigation: Avoid submitting sensitive or unnecessary location details, and review generated API requests before execution. <br>
Risk: Ambiguous location searches can return multiple candidates and the helper may use the first or best-matching result. <br>
Mitigation: Use a specific city or regency name, or search first and call the schedule command with the resolved location ID. <br>


## Reference(s): <br>
- [api.myquran.com API base](https://api.myquran.com/v3) <br>
- [ClawHub skill page](https://clawhub.ai/banghasan/jadwal-sholat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper prints concise schedules or location search results; monthly output previews the first seven days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
