## Description: <br>
Jadwal Sholat helps agents retrieve Indonesian prayer times, including imsak, subuh, dzuhur, ashar, maghrib, and isya, for a requested city or regency from api.myquran.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banghasan](https://clawhub.ai/user/banghasan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up Indonesian prayer schedules for a city or regency for today, a specific date, or a month. <br>

### Deployment Geography for Use: <br>
Global, for Indonesian city and regency prayer-time lookups. <br>

## Known Risks and Mitigations: <br>
Risk: Location, date or month, and timezone query values are sent to api.myquran.com. <br>
Mitigation: Use only the location and date information needed for the prayer-time lookup, and do not enter unrelated private information as a location search term. <br>
Risk: Prayer-time accuracy depends on the availability and response data of the public api.myquran.com service. <br>
Mitigation: Review returned locations and times before relying on them, especially when a search term can match multiple Indonesian cities or regencies. <br>


## Reference(s): <br>
- [api.myquran.com v3 API](https://api.myquran.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text with Markdown shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials are required. Location, date or month, and timezone values are used to query the public api.myquran.com service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
