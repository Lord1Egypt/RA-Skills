## Description: <br>
Scrapes and collects job leads from major job boards on demand or on a schedule for production, creative, and related roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gullish42069](https://clawhub.ai/user/gullish42069) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect and monitor job leads across supported job boards for production, creative, freelance, and career-search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to third-party job sites and may be affected by site terms, availability, rate limits, or anti-bot protections. <br>
Mitigation: Review the target sites' terms and configure scraping frequency deliberately before enabling scheduled runs. <br>
Risk: Scheduled scraping can repeatedly write local job lead results and logs. <br>
Mitigation: Use the cron examples only when scheduled collection is intended, and periodically review generated output and logs. <br>
Risk: The skill depends on the third-party scrapling package. <br>
Mitigation: Review and pin the dependency in the deployment environment before use. <br>


## Reference(s): <br>
- [Query templates](references/queries.md) <br>
- [ClawHub skill page](https://clawhub.ai/gullish42069/job-lead-radar) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON file plus Markdown guidance with shell and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes scraped job lead records locally to scripts/job_leads.json; results can vary by source availability and anti-bot controls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
