## Description: <br>
Search and monitor LinkedIn job listings with city-based filters, hourly cron support, and smart deduplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yashsuman15](https://clawhub.ai/user/yashsuman15) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Job seekers and their agents use this skill to search LinkedIn job listings, manage recurring search profiles, and receive deduplicated job results for selected roles, filters, and cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs LinkedIn job scraping and can make repeated network checks when monitoring is enabled. <br>
Mitigation: Run only user-requested searches, keep page counts and delays conservative, and confirm before enabling recurring monitoring. <br>
Risk: Saved searches and seen job IDs are stored in local files. <br>
Mitigation: Avoid storing sensitive search terms and review or remove local profile and history files when they are no longer needed. <br>
Risk: Profile removal, history clearing, and schedule creation can change the user's monitoring state. <br>
Mitigation: Confirm with the user before creating schedules, removing profiles, or clearing job history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yashsuman15/linkedin-jobs) <br>
- [ClawHub skill homepage](https://clawhub.ai/skills/linkedin-jobs) <br>
- [LinkedIn Jobs](https://linkedin.com/jobs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON job listings and Markdown-formatted job notifications, with shell commands for search setup and monitoring.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local search profile and seen-job tracking files when monitoring is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
