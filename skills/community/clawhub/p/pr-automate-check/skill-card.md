## Description: <br>
Automates pull request review, service health validation, and optional Discord notification for GitHub pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured pre-merge pull request check that gathers a diff, captures CI metadata, records health status, and optionally posts a Discord summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script may operate on the wrong repository because it extracts only the pull request number before calling the authenticated GitHub CLI. <br>
Mitigation: Use the skill only from the intended repository and GitHub account until the full owner, repo, and pull request URL are validated and passed explicitly to `gh`. <br>
Risk: Discord webhook notifications can disclose pull request links and health summaries to the configured channel. <br>
Mitigation: Provide Discord webhooks only for channels approved to receive pull request and service health information. <br>
Risk: Cron or webhook automation can repeatedly run the script with repository context mistakes. <br>
Mitigation: Avoid unattended cron or webhook use until repository validation is added and reviewed. <br>


## Reference(s): <br>
- [PR Automate Check on ClawHub](https://clawhub.ai/terrycarter1985/pr-automate-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command usage and JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an authenticated GitHub CLI session and may optionally send a Discord webhook notification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
