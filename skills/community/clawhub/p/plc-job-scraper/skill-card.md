## Description: <br>
Automaticky vyhledává PLC, automation a SCADA pracovní nabídky z LinkedIn, Indeed a dalších job boardů. Ideální pro PLC programátory a automation inženýry hledající nové projekty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjmore66](https://clawhub.ai/user/cjmore66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
PLC programmers, automation engineers, and job-seeking agents use this skill to configure searches for PLC, automation, and SCADA roles, run job-board scraping workflows, and export matching listings for review or follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes scraping job boards and mentions proxy rotation for rate-limit bypass. <br>
Mitigation: Respect job-board terms, rate limits, and robots or access restrictions; avoid using proxy rotation to bypass controls. <br>
Risk: The workflow references an external Apify actor plus export and notification scripts. <br>
Mitigation: Verify the actor and any export or notification scripts before running them, especially before connecting Google Sheets or Telegram. <br>
Risk: Cron examples can create unattended recurring scraping. <br>
Mitigation: Enable scheduled runs only when daily automated scraping is intended and monitored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjmore66/plc-job-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [Markdown with bash examples and JSON/CSV result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Job listing fields include title, company, location, salary when available, description, URL, posting date, job type, and required skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
