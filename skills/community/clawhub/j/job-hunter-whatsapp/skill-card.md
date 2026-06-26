## Description: <br>
Automates job search, job-description parsing, resume customization, application tracking, and WhatsApp or messaging updates using configured job APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielvivek2006](https://clawhub.ai/user/danielvivek2006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to find roles from job APIs, parse actual job descriptions, tailor resumes from verified user experience, track application status, and send concise job-hunt updates through WhatsApp or another messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive resume, job-search, API key, application tracker, and messaging data. <br>
Mitigation: Install only in a private workspace and keep resume, config, tracker, and API key files out of Git and shared folders. <br>
Risk: Resume tailoring can introduce inaccurate or overstated experience if not reviewed. <br>
Mitigation: Review tailored resumes before use and include only verified user experience and facts drawn from the actual job description. <br>
Risk: Automated cron or WhatsApp updates may expose job-search details to an unintended recipient or on an unintended schedule. <br>
Mitigation: Enable scheduled or messaging updates only after confirming the schedule, recipient, and fields included. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielvivek2006/job-hunter-whatsapp) <br>
- [Job APIs Reference](references/apis.md) <br>
- [Adzuna Developer](https://developer.adzuna.com) <br>
- [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) <br>
- [Jobicy Remote Jobs API](https://jobicy.com/api/v2/remote-jobs) <br>
- [RemoteOK API](https://remoteok.com/api) <br>
- [Remotive Jobs API](https://remotive.com/api/remote-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and tracker files, shell commands, and optional script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses actual job-description data only; stores resumes, API keys, configuration, and application tracking data in local workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
