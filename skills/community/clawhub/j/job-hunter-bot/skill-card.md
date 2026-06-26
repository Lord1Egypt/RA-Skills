## Description: <br>
Builds and deploys an automated job hunting system with a Telegram bot that scrapes LinkedIn jobs, scores candidate fit, and sends job notifications with action buttons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barleviatias](https://clawhub.ai/user/barleviatias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and job seekers use this skill to set up a Telegram-based job alert workflow that searches LinkedIn, stores matches locally, scores roles against a candidate profile, and notifies selected users about relevant openings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores a Telegram bot token, Telegram user IDs, candidate profile details, and a local jobs database. <br>
Mitigation: Keep config.json and jobs.db out of version control, restrict local file permissions, and use environment variables or a secret manager for the Telegram token when extending the deployment. <br>
Risk: The bot and scheduled scraper continue contacting LinkedIn and Telegram until stopped. <br>
Mitigation: Review scheduled jobs and running bot processes during deployment, and stop the cron job or bot process when notifications should no longer run. <br>
Risk: LinkedIn scraping may be brittle or conflict with service terms. <br>
Mitigation: Review LinkedIn terms and test the scraper behavior before operational use; expect selectors or guest API behavior to change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barleviatias/job-hunter-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, Python scripts, and SQL schema snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployable local scripts for a job-search bot; users provide candidate profile data and Telegram configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
